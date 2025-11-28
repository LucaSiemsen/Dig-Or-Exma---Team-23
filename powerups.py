# ============================================================
# powerups.py – kleine Helferlein im Studentenleben
# ------------------------------------------------------------
# PowerUps im Spiel:
#   - Pizza   : Ein Treffer vom Prof wird einmal ignoriert
#   - Party   : Zeitbuff oder -debuff (random ±10s)
#   - ChatGPT : gibt dir sofort 1 ECTS
#
# Wichtig: Die eigentliche Wirkung findet hier statt. Das
# Level ruft nur apply_to(level, student) auf und bekommt
# einen kleinen Text zurück, den wir im HUD anzeigen.
# ============================================================

from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from .level import Level
    from .entities import Student


class PowerUpType(Enum):
    PIZZA = auto()
    PARTY = auto()
    CHATGPT = auto()


class PowerUp:
    def __init__(self, grid_x: int, grid_y: int, tile_size: int, ptype: PowerUpType):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.ptype = ptype

    # --------------------------------------------------------
    # Zeichnen
    # --------------------------------------------------------
    def draw(self, screen: pygame.Surface, offset_x: int, offset_y: int) -> None:
        px = offset_x + self.grid_x * self.tile_size
        py = offset_y + self.grid_y * self.tile_size
        margin = self.tile_size // 6

        if self.ptype == PowerUpType.PIZZA:
            color = (255, 160, 90)   # orange
        elif self.ptype == PowerUpType.PARTY:
            color = (180, 80, 200)   # lila
        else:  # CHATGPT
            color = (80, 220, 180)   # türkis

        rect = pygame.Rect(
            px + margin,
            py + margin,
            self.tile_size - 2 * margin,
            self.tile_size - 2 * margin,
        )
        pygame.draw.rect(screen, color, rect)

    # --------------------------------------------------------
    # Wirkung
    # --------------------------------------------------------
    def apply_to(self, level: "Level", student: "Student") -> str:
        """
        Wird vom Level aufgerufen, wenn der Student auf dem Feld landet.
        Gibt einen kurzen Text zurück, den wir im HUD anzeigen können.
        """

        if self.ptype == PowerUpType.PIZZA:
            student.has_pizza_shield = True
            return "Pizza: Ein Treffer vom Prof wird ignoriert. 🍕"

        if self.ptype == PowerUpType.PARTY:
            # Party kann gut oder schlecht sein
            import random

            delta = random.choice([-10.0, +10.0])
            # Zeit clampen, damit es nicht negativ wird
            level.timer.time_left = max(
                5.0, min(level.timer.duration, level.timer.time_left + delta)
            )
            if delta > 0:
                return "Party gut geplant: +10s BAföG-Zeit! 🎉"
            else:
                return "Party etwas eskaliert: -10s BAföG-Zeit… 😵"

        if self.ptype == PowerUpType.CHATGPT:
            level.collected_ects += 1
            # Level prüft selbst, ob genug ECTS erreicht wurden
            return "ChatGPT hilft dir bei der Klausur: +1 ECTS. 🤖"

        # Fallback
        return ""
