# game.py
# Hauptsteuerung fürs Spiel: GameLoop, States, Rendering, Frage-Logik

from __future__ import annotations

import sys
from enum import Enum, auto
import pygame

from .pausemenu import PauseMenu
from .sound import SoundManager
from .HUD import Mutebutton
from .ui import draw_buff_timer_top_right

# ------------------------------------------------------------------------------
# GenAI-Kennzeichnung
# Tool: ChatGPT (OpenAI)
# Prompt (Auszug):
#   "Ich brauche Hilfe beim Strukturieren einer pygame-basierten GameLoop,
#    besonders bei:
#       1) der Organisation einer State-Machine (RUNNING, MENU, QUESTION, etc.),
#       2) dem Zusammenspiel von Level, Spieler und Professor-Objekten,
#       3) dem Entkoppeln der Frage-/Antwort-Logik,
#       4) dem Fehlerzähler für den Spieler.
#
#    Bitte erkläre mir, wie man diese Teile sinnvoll trennt und kommentiert,
#    ohne meine vorhandene Architektur umzubauen."
# ------------------------------------------------------------------------------

# Konfigurationswerte (Fallbacks wenn config.py fehlt)
try:
    from src.config import (
        GRID_COLS, GRID_ROWS,
        GRID_MARGIN_X_TILES, GRID_MARGIN_Y_TILES,
        REQUIRED_ECTS,
    )
except ImportError:
    GRID_COLS = 12
    GRID_ROWS = 8
    GRID_MARGIN_X_TILES = 2
    GRID_MARGIN_Y_TILES = 2
    REQUIRED_ECTS = 5

# Sprite-Fallback
try:
    from src.graphics import Sprite
except ImportError:
    # Nur falls graphics.py fehlt – einfache farbige Box
    class Sprite:
        def __init__(self, path: str, w: int, h: int):
            self.surface = pygame.Surface((w, h))
            self.surface.fill((120, 120, 120))

        def draw(self, screen: pygame.Surface, x: int, y: int):
            screen.blit(self.surface, (x, y))


from src.entities import Student
from src.level import Level
from src.tile import TileType


# ------------------------------------------------------------------------------
# GameStates – hiermit weiß das Spiel immer, was gerade passieren soll
# ------------------------------------------------------------------------------
class GameState(Enum):
    MENU = auto()          # Titelbildschirm
    RUNNING = auto()       # Spiel läuft
    QUESTION = auto()      # Spieler muss eine Quizfrage beantworten
    GAME_OVER = auto()     
    LEVEL_COMPLETE = auto()
    PAUSED = auto()


# ------------------------------------------------------------------------------
# Hauptklasse Game – enthält die komplette Steuerung
# ------------------------------------------------------------------------------
class Game:
    def __init__(self):
        pygame.init()

        # Vollbild – wir nutzen die nativen Monitorwerte
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        self.width, self.height = info.current_w, info.current_h

        pygame.display.set_caption("Dig Or Exma - Team 23")
        self.clock = pygame.time.Clock()

        # Kachelgröße dynamisch berechnen – damit es unabhängig von Auflösung gleich aussieht
        max_tile_w = self.width // (GRID_COLS + 2 * GRID_MARGIN_X_TILES)
        max_tile_h = self.height // (GRID_ROWS + 2 * GRID_MARGIN_Y_TILES)
        self.tile_size = min(max_tile_w, max_tile_h)

        # Spielfeld zentrieren
        self.grid_offset_x = (self.width - GRID_COLS * self.tile_size) // 2
        self.grid_offset_y = (self.height - GRID_ROWS * self.tile_size) // 2

                # Hintergrund laden
        try:
            bg = pygame.image.load("assets/sprites/Gamepad_Hintergrund.png").convert()
            self.background = pygame.transform.scale(bg, (self.width, self.height))
        except:
            self.background = pygame.Surface((self.width, self.height))
            self.background.fill((20, 20, 30))

        # ----------------------------------------------------------
        # Spielfeld-Kasten aus der UI-Grafik berechnen
        # (Original-UI: 320x240)
        # ----------------------------------------------------------
        UI_W, UI_H = 320, 240
        sx = self.width / UI_W
        sy = self.height / UI_H

        # Weißer Kasten im Originalbild (manuell gemessen)
        BOX_X, BOX_Y = 40, 40
        BOX_W, BOX_H = 240, 120

        self.board_rect = pygame.Rect(
            int(BOX_X * sx),
            int(BOX_Y * sy),
            int(BOX_W * sx),
            int(BOX_H * sy),
        )

        # Tilegröße so berechnen, dass das Grid reinpasst
        self.tile_size = min(
            self.board_rect.w // GRID_COLS,
            self.board_rect.h // GRID_ROWS
        )

        # Grid innerhalb des Kastens zentrieren
        grid_w = GRID_COLS * self.tile_size
        grid_h = GRID_ROWS * self.tile_size
        self.grid_offset_x = self.board_rect.x + (self.board_rect.w - grid_w) // 2
        self.grid_offset_y = self.board_rect.y + (self.board_rect.h - grid_h) // 2

        # Boden, Tunnelblöcke sowie nun auch Blöcke für die oberste Reihe
        self.block_solid = Sprite("assets/sprites/block.png",
                                  self.tile_size, self.tile_size)
        self.block_empty = Sprite("assets/sprites/floor.png",
                                  self.tile_size, self.tile_size)
        self.block_grass = Sprite("assets/sprites/grass.png",
                                  self.tile_size, self.tile_size)

        # Soundverwaltung
        self.sound_manager = SoundManager()
        self.sound_manager.play_song(1)

        # Mute-Button oben rechts
        button_size = 50
        padding = 30
        self.mute_button = Mutebutton(
            self.width - button_size - padding,
            self.height - button_size - padding,
            button_size,
            self.sound_manager
        )

        # Schriften
        self.font_small = pygame.font.SysFont(None, 26)
        self.font_big = pygame.font.SysFont(None, 48)
        self.font_title = pygame.font.SysFont(None, 64)

        # State + Variablen
        self.state = GameState.MENU
        self.level: Level | None = None
        self.student: Student | None = None

        # Daten für Fragen
        self.active_prof = None
        self.active_question = None
        self.last_question_feedback = None
        self.mistakes = 0   # Spieler darf 2 Fehler machen

        # Level & Student erstellen
        self._create_level_and_student()

        # Pause-Menü vorbereiten
        self.pause_menu = PauseMenu(
            self.width, self.height, self.font_title,
            self.font_small, self.sound_manager
        )

    # ------------------------------------------------------------------------------
    # Neues Level erstellen + Student spawnen
    # ------------------------------------------------------------------------------
    def _create_level_and_student(self):
        self.level = Level(self.tile_size, level_index=0)

        # Startkoordinaten – momentan fest, könnte man später zufällig machen
        start_x, start_y = 1, 1

        # Student-Grafik
        student_img = pygame.image.load("assets/sprites/student.png").convert_alpha()
        student_img = pygame.transform.scale(student_img, (self.tile_size, self.tile_size))

        self.student = Student(start_x, start_y, self.tile_size, student_img)

        # Startfeld ausgraben, damit der Spieler nicht feststeckt
        self.level.tiles[start_x][start_y].dig()

    # ------------------------------------------------------------------------------
    # Neustartoption
    # ------------------------------------------------------------------------------
    def restart(self):
        self._create_level_and_student()
        self.state = GameState.RUNNING
        self.last_question_feedback = None
        self.mistakes = 0
        self.sound_manager.gameover_sound.stop()
        self.sound_manager.play_song(0) 
    # ------------------------------------------------------------------------------
    # Haupt-GameLoop
    # ------------------------------------------------------------------------------
    def run(self):
        running = True

        while running:
            # dt = Zeit seit letztem Frame in Sekunden
            dt = self.clock.tick(60) / 1000.0

            # Eingaben abfragen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    self.handle_key(event.key)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click(event.pos)

            # Nur updaten, wenn wir uns im RUNNING-State befinden
            if self.state == GameState.RUNNING:
                self.level.update(dt)
                self.student.update_animation(dt)
                self.student.update_buffs(dt)
                self.check_prof_collision()

                # Übergang in neue States
                if self.level.is_game_over:
                    self.state = GameState.GAME_OVER
                    self.sound_manager.pause_music()
                    self.sound_manager.game_over_music()    
                elif self.level.is_won:
                    self.state = GameState.LEVEL_COMPLETE

            # Immer zeichnen
            self.draw()

        pygame.quit()
        sys.exit()

    # ------------------------------------------------------------------------------
    # Tastatursteuerung – abhängig vom aktuellen State
    # ------------------------------------------------------------------------------
    def handle_key(self, key):

        # SHIFT → Pause toggeln
        if key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
            if self.state == GameState.RUNNING:
                self.state = GameState.PAUSED
            elif self.state == GameState.PAUSED:
                self.state = GameState.RUNNING
            return

        # Pause-Menü
        if self.state == GameState.PAUSED:
            if key == pygame.K_r:
                self.restart()
            elif key == pygame.K_ESCAPE:
                self.state = GameState.MENU
            return

        # Menü
        if self.state == GameState.MENU:
            if key in (pygame.K_SPACE, pygame.K_RETURN):
                self.restart()
            return

        # Spiel läuft
        if self.state == GameState.RUNNING:
            assert self.level and self.student

            if key == pygame.K_r:
                self.restart()
                return

            dx = dy = 0
            if key == pygame.K_UP:    dy = -1
            if key == pygame.K_DOWN:  dy = 1
            if key == pygame.K_LEFT:  dx = -1
            if key == pygame.K_RIGHT: dx = 1

            if dx or dy:
                self.sound_manager.play_footsteps()
                prof = self.student.move(dx, dy, self.level)
                if prof is not None:
                    self.open_question(prof)
            return

        # Frage beantworten
        if self.state == GameState.QUESTION:
            if key in (pygame.K_1, pygame.K_2, pygame.K_3):
                answer_index = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2}[key]
                self.resolve_question(answer_index)
            return

        # GameOver/LevelComplete
        if key == pygame.K_r:
            self.restart()
        elif key in (pygame.K_SPACE, pygame.K_RETURN):
            self.state = GameState.MENU

    # ------------------------------------------------------------------------------
    # Klick auf Buttons
    # ------------------------------------------------------------------------------
    def handle_mouse_click(self, pos):
        self.mute_button.handle_click(pos)

        if self.state == GameState.PAUSED:
            action = self.pause_menu.handle_click(pos)
            if action == "resume":
                self.state = GameState.RUNNING
            elif action == "menu":
                self.state = GameState.MENU
                self._create_level_and_student()

    # ------------------------------------------------------------------------------
    # Kollision Spieler ↔ Professor erkennen → Frage starten
    # ------------------------------------------------------------------------------
    def check_prof_collision(self):
        if not self.level or not self.student:
            return

        for prof in self.level.professors:
            if (prof.grid_x, prof.grid_y) == (self.student.grid_x, self.student.grid_y):
                self.open_question(prof)
                return

    # ------------------------------------------------------------------------------
    # Frage öffnen
    # ------------------------------------------------------------------------------
    def open_question(self, prof):
        """
        Frage wird über level.get_question_for_prof(prof) geladen.
        Dieser Mechanismus kommt aus der alten Struktur,
        funktioniert aber weiterhin sauber.
        """
        question = self.level.get_question_for_prof(prof)
        if question is None:
            return

        self.active_prof = prof
        self.active_question = question

        self.last_question_feedback = None
        self.state = GameState.QUESTION
        self.sound_manager.play_hitsound()
        self.sound_manager.pause_music()

    # ------------------------------------------------------------------------------
    # Frage beantworten
    # ------------------------------------------------------------------------------
    def resolve_question(self, given_index):
        """
        Dieser Teil war am umfangreichsten:
        - Antwort prüfen
        - ECTS vergeben
        - Fehler zählen
        - Level beenden
        """

        q = self.active_question
        prof = self.active_prof

        if q is None:
            self.state = GameState.RUNNING
            return

        # Richtige Antwort
        if given_index == q.correct:
            self.level.collected_ects += 2
            self.last_question_feedback = "Richtige Antwort! +2 ECTS. " + q.explanation
            self.level.remove_professor(prof)

        # Falsche Antwort
        else:
            self.mistakes += 1
            self.last_question_feedback = (
                f"Falsch beantwortet ({self.mistakes}/2). " + q.explanation
            )

            # Nach zwei Fehlern → Game Over
            if self.mistakes >= 2:
                self.level.is_game_over = True
                self.state = GameState.GAME_OVER
                self.sound_manager.stop_hitsound()
                self.sound_manager.pause_music()
                self.sound_manager.game_over_music()
                return

            # Zeitstrafe
            self.level.timer.time_left = max(5.0, self.level.timer.time_left - 10.0)

        # Frage abschließen
        self.active_prof = None
        self.active_question = None
        self.sound_manager.stop_hitsound()
        self.sound_manager.unpause_music()

        # Siegbedingung prüfen
        if self.level.collected_ects >= REQUIRED_ECTS and not self.level.is_game_over:
            self.level.is_won = True
            self.state = GameState.LEVEL_COMPLETE
        else:
            self.state = GameState.RUNNING

    # ------------------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------------------
    def draw(self):
        self.screen.blit(self.background, (0, 0))

        if self.state == GameState.MENU:
            self.draw_menu()

        elif self.state == GameState.PAUSED:
            self.draw_game()
            self.pause_menu.draw(self.screen)

        else:
            self.draw_game()

        pygame.display.flip()

    # ------------------------------------------------------------------------------
    # Menü zeichnen
    # ------------------------------------------------------------------------------
    def draw_menu(self):
        cx = self.width // 2
        cy = self.height // 2

        title = self.font_title.render("Dig Or Exma", True, (255, 255, 255))
        subtitle = self.font_small.render(
            "Ein Student, fünf ECTS und ein gnadenloser BAföG-Timer.",
            True, (230, 230, 230)
        )
        hint = self.font_small.render(
            "SPACE/ENTER: Starten   |   ESC: Beenden",
            True, (230, 230, 230)
        )

        self.screen.blit(title, title.get_rect(center=(cx, cy - 80)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(cx, cy - 30)))
        self.screen.blit(hint, hint.get_rect(center=(cx, cy + 40)))

    # ------------------------------------------------------------------------------
    # Spielfeld zeichnen
    # ------------------------------------------------------------------------------
    def draw_game(self):
        assert self.level and self.student

        # Tiles zeichnen
        for x in range(self.level.cols):
            for y in range(self.level.rows):
                tile = self.level.tiles[x][y]
                px = self.grid_offset_x + x * self.tile_size
                py = self.grid_offset_y + y * self.tile_size

                # --- Darunter befindet sich die Schleife ---
                if tile.type == TileType.GRASS:
                    self.block_grass.draw(self.screen, px, py)
                elif tile.is_solid:
                    self.block_solid.draw(self.screen, px, py)
                else:
                    self.block_empty.draw(self.screen, px, py)
                # -----------------------------

        # ECTS-Objekte
        for ects in self.level.ects_items:
            ects.draw(self.screen, self.grid_offset_x, self.grid_offset_y)


        # PowerUps
        for p in self.level.powerups:
            p.draw(self.screen, self.grid_offset_x, self.grid_offset_y)


        # Professoren
        for prof in self.level.professors:
            prof.draw(self.screen, self.grid_offset_x, self.grid_offset_y)

        # Spieler
        self.student.draw(self.screen, self.grid_offset_x, self.grid_offset_y)

        # HUD
        self.draw_hud()

        # Overlays
        if self.state == GameState.QUESTION:
            self.draw_question_overlay()

        elif self.state == GameState.GAME_OVER:
            self.draw_center_message(
                "Game Over",
                self.level.game_over_reason,
                "R: Neustart   |   ENTER: Menü",
                (255, 120, 120)
            )

        elif self.state == GameState.LEVEL_COMPLETE:
            self.draw_center_message(
                "Level geschafft!",
                "Du hast genug ECTS gesammelt!",
                "R: Neustart   |   ENTER: Menü",
                (120, 255, 120)
            )

    # ------------------------------------------------------------------------------
    # HUD (Zeit, ECTS, Feedback)
    # ------------------------------------------------------------------------------
    def draw_hud(self):
        hud = self.font_small.render(
            f"Zeit: {int(self.level.timer.time_left)}s   "
            f"ECTS: {self.level.collected_ects}/{REQUIRED_ECTS}",
            True, (255, 255, 255)
        )
        self.screen.blit(hud, (20, 20))

        controls = self.font_small.render(
            "Pfeiltasten: bewegen/graben   |   SHIFT: Pause   |   R: Neustart",
            True, (255, 255, 255)
        )
        self.screen.blit(controls, (20, 50))

        if self.last_question_feedback:
            msg = self.font_small.render(
                self.last_question_feedback,
                True, (200, 255, 200)
            )
            self.screen.blit(msg, (20, self.height - 40))

        self.mute_button.draw(self.screen)
        draw_buff_timer_top_right(self.screen, self.font_small, self.student)
    # ------------------------------------------------------------------------------
    # Frage-Overlay
    # ------------------------------------------------------------------------------
    def draw_question_overlay(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        q = self.active_question
        cx = self.width // 2
        cy = self.height // 2 - 80

        lines = [q.text] + [f"{i+1}) {ans}" for i, ans in enumerate(q.answers)]
        lines.append("Antwort mit 1 / 2 / 3")

        for i, text in enumerate(lines):
            surf = self.font_small.render(text, True, (255, 255, 255))
            self.screen.blit(surf, surf.get_rect(center=(cx, cy + i * 30)))

    # ------------------------------------------------------------------------------
    # Zentrierte Meldung (Game Over / Level Complete)
    # ------------------------------------------------------------------------------
    def draw_center_message(self, title, line1, line2, color_title):
        cx = self.width // 2
        cy = self.height // 2

        surf_title = self.font_big.render(title, True, color_title)
        surf_line1 = self.font_small.render(line1, True, (255, 255, 255))
        surf_line2 = self.font_small.render(line2, True, (255, 255, 255))

        self.screen.blit(surf_title, surf_title.get_rect(center=(cx, cy - 40)))
        self.screen.blit(surf_line1, surf_line1.get_rect(center=(cx, cy)))
        self.screen.blit(surf_line2, surf_line2.get_rect(center=(cx, cy + 30)))


# ------------------------------------------------------------------------------
# Direkter Start
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    game = Game()
    game.run()
