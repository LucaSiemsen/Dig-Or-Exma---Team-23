# enemy.py
# ==========================================
# ProfessorEnemy – läuft im Tunnel rum und
# kann dem Spieler eine Frage stellen.
# ==========================================

import random
import pygame
from .graphics import Sprite


class ProfessorEnemy:
    def __init__(self, grid_x: int, grid_y: int, tile_size: int,
                 sprite: Sprite, questions: list[dict]):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.sprite = sprite
        # Liste von Fragen (kommt aus questions.py oder config.py)
        self.questions = questions

        # kleiner Timer, damit der Prof nicht in jedem Frame rennt
        self._move_cooldown = random.uniform(0.4, 0.9)

    def update(self, dt: float, level: "Level") -> None:
        """
        Zufällige Bewegung des Professors über das gesamte Spielfeld.
        Wichtig: Profs ignorieren Blöcke – sie „schweben“ quasi über den Kacheln.
        Nur die Spielfeldgrenzen werden beachtet.
        """
        # Cooldown runterzählen
        self._move_cooldown -= dt

        # Wenn noch Pause ist oder das Level vorbei ist, nichts tun
        if self._move_cooldown > 0 or level.is_game_over or level.is_won:
            return

        # Nächste Wartezeit bis zur nächsten Bewegung
        self._move_cooldown = random.uniform(0.4, 0.9)

        # zufällige Reihenfolge von Richtungen
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx = self.grid_x + dx
            ny = self.grid_y + dy

            # Nur prüfen, ob die Position im Spielfeld liegt
            if not level.in_bounds(nx, ny):
                continue

            # Blöcke sind Professoren egal -> einfach setzen
            self.grid_x = nx
            self.grid_y = ny
            break


    def draw(self, screen: pygame.Surface, offset_x: int, offset_y: int) -> None:
        """Professor an seiner Grid-Position zeichnen."""
        px = offset_x + self.grid_x * self.tile_size
        py = offset_y + self.grid_y * self.tile_size
        self.sprite.draw(screen, px, py)

    def get_question(self) -> dict:
        """
        Gibt eine zufällige Frage aus seiner Fragenliste zurück.
        Struktur: {"prof_name": ..., "question": ..., "answers": [...], "correct": int}
        """
        return random.choice(self.questions)
