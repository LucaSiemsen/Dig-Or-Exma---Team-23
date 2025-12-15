# game.py
# Hauptsteuerung fürs Spiel: GameLoop, States, Rendering, Frage-Logik

from __future__ import annotations
import sys
from enum import Enum, auto
import pygame
from .pausemenu import PauseMenu
from .sound import SoundManager
from .ui import Mutebutton

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
        LEVELS
    )
except ImportError:
    GRID_COLS = 15
    GRID_ROWS = 9
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
from src.anim_scene_builder import Animator_Scenes
from src.mainmenu import MainMenu

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

        self.running=True

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
            bg = pygame.image.load("assets/sprites/Gamepad.png").convert_alpha()
            
            #ratio bild abfrage
            bg_w, bg_h=bg.get_size()
            bg_ratio=bg_w/bg_h
            #ratio screen abfrage
            screen_w, screen_h=self.screen.get_size()
            screen_ratio=screen_w/screen_h
            if screen_ratio>bg_ratio:
                new_h=screen_h
                new_w=int(screen_h*bg_ratio)
            else:
                new_w=screen_w
                new_h=int(screen_w/bg_ratio)
            background_scaled = pygame.transform.scale(bg, (new_w,new_h))
            self.background_rect=background_scaled.get_rect(center=self.screen.get_rect().center)
            self.background=background_scaled

        
        except:
            self.background = pygame.Surface((self.width, self.height))
            self.background.fill((20, 20, 30))

        # ----------------------------------------------------------
        # Spielfeld-Kasten aus der UI-Grafik berechnen
        # (Original-UI: 320x240)
        #hier wird Mitte berechnet
        # ----------------------------------------------------------
        UI_W, UI_H = 320, 180
        #sx und sy sind nicht mehr abhängig vom screen sondern
        #vom background
        sx = self.background_rect.width / UI_W
        sy = self.background_rect.height / UI_H

        # Weißer Kasten im Originalbild (manuell gemessen)
        BOX_X, BOX_Y = 80, 44
        BOX_W, BOX_H = 160, 96

        #Abgängikeit vom Background und dem Abstand vom Rand
        #als Einstiegsecke oben links im "Gamepadbildschirm"
        self.board_rect = pygame.Rect(
            int(self.background_rect.left + BOX_X * sx),
            int(self.background_rect.top +BOX_Y * sy),
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
        
        # Buff-Icons vorladen Pizza-Schild
        self.buff_icon_size = 35
        self.buff_icon_pizza = pygame.image.load("assets/sprites/pizza.png").convert_alpha()
        self.buff_icon_pizza = pygame.transform.scale(
        self.buff_icon_pizza, (self.buff_icon_size, self.buff_icon_size)
)

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
        
        # Godmode 
        self.godmode=False
        
        # Level & Student erstellen
        self.current_level_index = 0
        self._create_level_and_student()

        # Pause-Menü vorbereiten
        self.pause_menu = PauseMenu(
            self.width, self.height, self.font_title,
            self.font_small, self.sound_manager
        )
        # --------------------------------------------------
        # Automatischer Level-Übergang (Semester-Wechsel)
        # --------------------------------------------------
        self.current_level_index = 0     # Start bei Semester 1
        self.level_complete_timer = 0.0  # zählt Zeit nach Levelende
        self.LEVEL_COMPLETE_DELAY = 2.0  # Sekunden bis nächstes Semester


        #Animationsobjekte deklarieren 
        self.game_over_animation=Animator_Scenes(self.screen.get_width(),self.screen.get_height(),
                                                 250,1)
        self.animationslist=self.game_over_animation.load_from_spritesheet("assets\sprites\GAME OVER Scene.png",315,180,self.background)
        self.hauptmenu=MainMenu(self.screen,self.background,self.background_rect,self.font_small,"")
    # ------------------------------------------------------------------------------
    # Neues Level erstellen + Student spawnen
    # ------------------------------------------------------------------------------
    def _create_level_and_student(self):
        self.level = Level(self.tile_size, level_index=self.current_level_index, sound_manager=self.sound_manager,godmode=self.godmode)

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
        if self.state == GameState.MENU:
            self.current_level_index = 0
        self._create_level_and_student()
        self.state = GameState.RUNNING
        self.game_over_animation.start()

        self.last_question_feedback = None
        self.mistakes = 0
        self.sound_manager.gameover_sound.stop()
        self.sound_manager.play_song(0) 
    # ------------------------------------------------------------------------------
    # Haupt-GameLoop
    # ------------------------------------------------------------------------------
    def run(self):

        while self.running:
            # dt = Zeit seit letztem Frame in Sekunden
            dt = self.clock.tick(60) / 1000.0

            # Eingaben abfragen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
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
            if key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                answer_index = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3}[key]
                self.resolve_question(answer_index)
            return

        # -----------------------------
        # GameOver / LevelComplete
        # -----------------------------
        if self.state == GameState.LEVEL_COMPLETE:
            # N = nächstes Semester/Level starten
            if key == pygame.K_n:
                self._go_to_next_level()
                return

            # R = aktuelles Semester neu starten
            if key == pygame.K_r:
                self.restart()
                return

            # ESC oder ENTER optional: zurück ins Menü
            if key in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.state = GameState.MENU
                return


        if self.state == GameState.GAME_OVER:
            # R = Neustart
            if key == pygame.K_r:
                self.restart()
                return

            # ENTER/ESC = Menü
            if key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.state = GameState.MENU
                return



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
                self.sound_manager.play_song(1)

    # ------------------------------------------------------------------------------
    # Kollision Spieler ↔ Professor erkennen → Frage starten
    # ------------------------------------------------------------------------------
    def check_prof_collision(self):
        if not self.level or not self.student:
            return

        for prof in self.level.professors:
            if (prof.grid_x, prof.grid_y) == (self.student.grid_x, self.student.grid_y):
                
                # A) Hat der Student ein Pizza-Schild?
                if self.student.has_pizza_shield:
                    self.student.has_pizza_shield = False  # Schild verbrauchen
                    self.level.last_powerup_message = "Pizza-Schild hat dich gerettet! 🍕"
                    self.level.remove_professor(prof)      # Prof entfernen, damit er nicht nochmal trifft
                    self.sound_manager.play_hitsound()     # Optional: Sound abspielen
                    return                                 # WICHTIG: Hier abbrechen, KEINE Frage starten!

                # B) Kein Schild -> Frage starten
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
    #GEN AI Kennzeichnung: Dieser Code wurde mit Unterstützung von KI-Technologie generiert.
    #Tools: OPENAI CHATGPT & Google Gemini
    #Verwendungszweck: Fehlersuche beim hitsound der mehrfach abgespielt wird, Code aber abgewandelt.
    #Prompt:Mein hitsound wird mehrfach abgespielt nach jeder Prof Frage, wie fixe ich das am besten
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
        if given_index == q.correct or self.godmode:
            self.level.collected_ects += 1
            
            #Standardannahme (für Profs)
            is_defeated = True  
            
            if prof is not None and hasattr(prof, "hp"):
                prof.hp -= 1
                if prof.hp > 0:
                    is_defeated = False #Hat noch Leben -> NICHT besiegt

            #Feedback für den Spieler
            if is_defeated:
                feedback = f"Richtige Antwort! +1 ECTS. {q.explanation} (Prof besiegt!)"
                self.sound_manager.stop_hitsound()
                self.sound_manager.unpause_music()
                self.level.remove_professor(prof)
            else:
                feedback = f"Richtige Antwort! +1 ECTS. {q.explanation} (Noch {prof.hp} HP)"

            self.last_question_feedback = feedback


        # 2 Falsche Antwort
        else:
            self.mistakes += 1
            if self.mistakes == 1:
                self.sound_manager.wrong_answer_sound()
                
            self.last_question_feedback = f"Falsch beantwortet ({self.mistakes}/2). {q.explanation}"
            
            if self.mistakes >= 2:
                self.level.is_game_over = True
                self.state = GameState.GAME_OVER
                self.sound_manager.stop_hitsound()
                self.sound_manager.pause_music()
                self.sound_manager.game_over_music()
                return
            
        #Zeitstrafe
        self.level.timer.time_left = max(5.0, self.level.timer.time_left - 10.0)

        #Frage abschließen
        self.active_prof = None
        self.active_question = None

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
        self.screen.blit(self.background, self.background_rect)

        if self.state == GameState.MENU:
            hauptmenu_status=self.hauptmenu.run()
            if hauptmenu_status["auswahl"]=="START":
                self.state=GameState.RUNNING
            elif hauptmenu_status["auswahl"]=="QUIT":
                self.running=False
            if hauptmenu_status["godmode"]==True:
                self.godmode=True
            self.restart()
                
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
            self.game_over_animation.draw(self.screen, self.background_rect)
            if (self.game_over_animation.update() == False):
                self.draw_center_message(
                    "Game Over",
                    self.level.game_over_reason,
                    "R: Neustart   |   ENTER: Menü",
                    (255, 120, 120)
                )
        elif self.state == GameState.LEVEL_COMPLETE:
            self.draw_center_message(
                "Semester geschafft!",
                "Du hast genug ECTS gesammelt!",
                "R: Neustart   |   ENTER: Menü    N: Nächstes Semester",
                (120, 255, 120)
            )

    # ------------------------------------------------------------------------------
    # HUD (Zeit, ECTS, Semester, Controls, Feedback)
    # ------------------------------------------------------------------------------
    def draw_hud(self):
        assert self.level # Sicherstellen, dass Level existiert

        # --- 1. TRANSPARENTE HINTERGRUND-OBERFLÄCHE ERSTELLEN ---
        # Definieren der Maße der Box
        box_width = 500
        box_height = 90
        
        # Erstellen einer neuen Oberfläche mit Alpha-Kanal (SRCALPHA)
        hud_bg_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        
        # Definieren der transparenten Farbe (Dunkelgrau: 30, 30, 30, mit Alpha: 180)
        # Alpha 180 von 255 ist ca. 70% Deckkraft
        TRANSPARENT_BLACK = (30, 30, 30, 180) 
        
        # Rechteck auf die neue, transparente Oberfläche zeichnen (beginnend bei 0, 0)
        hud_bg_rect_local = hud_bg_surface.get_rect()
        pygame.draw.rect(hud_bg_surface, TRANSPARENT_BLACK, hud_bg_rect_local) 
        
        # Optional: Weißer Rand (opaker Rand, da auf der HUD-Surface)
        pygame.draw.rect(hud_bg_surface, (255, 255, 255), hud_bg_rect_local, 1)

        # 2. Die transparente Oberfläche auf den Bildschirm blitten
        hud_start_x, hud_start_y = 10, 10
        self.screen.blit(hud_bg_surface, (hud_start_x, hud_start_y))
        # ---------------------------------------------------------

        # --- KORRIGIERTE ZEIT-FORMATIERUNG ---
        time_remaining = max(0.0, self.level.timer.time_left)
        minutes = int(time_remaining // 60)
        seconds = int(time_remaining % 60)
        # Zehntelsekunden anzeigen (für flüssige Aktualisierung)
        tenths = int((time_remaining * 10) % 10) 
        time_string = f"{minutes:02d}:{seconds:02d}.{tenths:01d}"
        # --------------------------------------

        # 1) Erste HUD-Zeile: Zeit + ECTS
        hud_line1 = self.font_small.render(
            f"Zeit: {time_string}   " # <--- Jetzt mit dynamischer Anzeige
            f"ECTS: {self.level.collected_ects}/{self.level.required_ects}",
            True, (255, 255, 255)
        )
        self.screen.blit(hud_line1, (20, 20)) # Text startet bei (20, 20)

        # 2) Zweite HUD-Zeile: Semester (aka Level)
        hud_line2 = self.font_small.render(
            f"Semester: {self.current_level_index + 1}/7",
            True, (255, 255, 255)
        )
        self.screen.blit(hud_line2, (20, 45)) # bisschen unter die erste Zeile

        # 3) Controls (eine Zeile tiefer)
        controls = self.font_small.render(
            "Pfeiltasten: bewegen/graben  |  SHIFT: Pause  |  R: Neustart",
            True, (255, 255, 255)
        )
        self.screen.blit(controls, (20, 70))

        # 4) Feedback unten (z.B. nach Fragen)
        if self.last_question_feedback:
            # ... (dieser Teil war nicht das Problem)
            msg = self.font_small.render(
                self.last_question_feedback,
                True, (200, 255, 200)
            )
            self.screen.blit(msg, (20, self.height - 40))

        elif self.level and self.level.last_powerup_message:
            msg = self.font_small.render(
                self.level.last_powerup_message,
                True, (255, 255, 100) # Gelb für Items
            )
            self.screen.blit(msg, (20, self.height - 40))

        # 5) Buttons / UI
        self.mute_button.draw(self.screen)
        self.draw_buff_timer_top_right()

        #Funktion für das Pizza-Schild Timer oben rechts
    def draw_buff_timer_top_right(self):
        if self.student is None:
            return

        if self.student.has_pizza_shield and self.student.pizza_shield_left > 0:
            secs = int(self.student.pizza_shield_left)
            text_surf = self.font_small.render(f"Schild: {secs}s", True, (255, 255, 255))

            
            gap = 10
            x = self.width - 460
            y = self.board_rect.top - 40
            size = self.buff_icon_size 

            #Icon zeichnen 
            self.screen.blit(self.buff_icon_pizza, (x, y))

            #Text daneben zeichnen
            text_rect = text_surf.get_rect()
            text_rect.left = x + size + gap
            text_rect.centery = y + size // 2   
            self.screen.blit(text_surf, text_rect)

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
    # Nächstes Level Funktion:
    # ------------------------------------------------------------------------------
    def _go_to_next_level(self):
        self.current_level_index += 1

        # wenn es kein weiteres Level gibt -> zurück ins Menü 
        if self.current_level_index >= len(LEVELS):
            self.current_level_index = 0   # <-- Reset, damit neues Spiel wieder bei Semester 1 startet
            self.state = GameState.MENU
            return


        # Reset pro Semester
        self.mistakes = 0
        self.active_prof = None
        self.active_question = None
        self.last_question_feedback = None

        # neues Level laden
        self._create_level_and_student()

        # weiter spielen
        self.state = GameState.RUNNING

# ------------------------------------------------------------------------------
# Direkter Start
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    game = Game()
    game.run()