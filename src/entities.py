# entities.py
# hier ist der Spieler (Student) definiert

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.level import Level
    from src.enemy import ProfessorEnemy #Hier den Prof importieren.


class Student:
    # repräsentiert den Spieler im Grid
    def __init__(self, grid_x: int, grid_y: int, tile_size: int, sprite: pygame.Surface):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.sprite = sprite

        # falls wir in einen Professor reinlaufen und der eine Frage hat
        self.pending_question = None      # kommt üblicherweise aus config.Question
        self.pending_professor: Optional["ProfessorEnemy"] = None

        # Status von PowerUps (z.B. Pizza-Schild)
        self.has_pizza_shield: bool = False

    @property
    def pos(self) -> tuple[int, int]:
        # aktuelle Position im Grid
        return self.grid_x, self.grid_y

    def reset(self, grid_x: int, grid_y: int) -> None:
        # Student auf Startposition zurücksetzen (z.B. bei Restart)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pending_question = None
        self.pending_professor = None

    def move(self, dx: int, dy: int, level: "Level") -> Optional["ProfessorEnemy"]:
        """
        bewegt den Studenten um ein Feld
        dx, dy ∈ {-1, 0, 1}
        das Level kümmert sich dann um:
        - Graben
        - ECTS
        - PowerUps
        - Professoren
        """

        # wenn das Level schon vorbei ist, machen wir nichts mehr
        if level.is_finished:
            return None

        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        # nicht aus dem Spielfeld rauslaufen
        if not level.in_bounds(new_x, new_y):
            return None

        # wenn da noch Erde ist, dann wird automatisch gegraben
        if level.tiles[new_x][new_y].is_solid:
            level.dig(new_x, new_y)

        # Position aktualisieren
        self.grid_x = new_x
        self.grid_y = new_y

        # Level fragen, was auf dem neuen Feld liegt
        # (ECTS, PowerUp, Professor)
        prof = level.on_player_enter_tile(new_x, new_y, self)

        # falls wir einen Professor getroffen haben, merken wir uns das
        if prof is not None:
            self.pending_professor = prof
            self.pending_question = prof.get_question()

        return prof

    def draw(self, screen: pygame.Surface, offset_x: int, offset_y: int) -> None:
        # Student an die richtige Stelle im Fenster zeichnen
        px = offset_x + self.grid_x * self.tile_size
        py = offset_y + self.grid_y * self.tile_size
        screen.blit(self.sprite, (px, py))
