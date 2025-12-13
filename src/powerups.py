# ============================================================
# src/powerups.py – kleine Helferlein im Studentenleben
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
# Autor: Aaron Lehrke (937367)
# ============================================================
# GenAI-Kennzeichnung
# Tool: Google Gemini
# Verwendungszweck: Implementierung des Strategy-Patterns für Item-Effekte.
# Prompt: "Vervollständige die von mir entworfene PowerUp-Klasse. Die Architektur 
#          nutzt ein Enum für die Typisierung und eine zentrale 'apply_to'-Methode 
#          (Strategy-Pattern) für die Effekte. Optimiere die draw-Methode so, 
#          dass fehlende Sprites durch prozedurale Grafiken (Rechtecke) ersetzt 
#          werden (Fallback-Mechanismus), um Abstürze zu vermeiden."
# ==============================================================================

from __future__ import annotations
from enum import Enum, auto
from typing import TYPE_CHECKING
import pygame
import random  # Import gehört nach oben

if TYPE_CHECKING:
    from .level import Level
    from .entities import Student

# Hilfsfunktion zum Laden (lokal definiert, um Abhängigkeiten gering zu halten)
def load_scaled(path: str, size: int) -> pygame.Surface:
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (size, size))
    except FileNotFoundError:
        # Fallback, falls Bild fehlt: Rotes Quadrat
        surf = pygame.Surface((size, size))
        surf.fill((255, 0, 0))
        return surf

class PowerUpType(Enum):
    PIZZA = auto()    # Schutzschild
    PARTY = auto()    # Zeit-Roulette (Gut oder Schlecht)
    CHATGPT = auto()  # ECTS Boost

class PowerUp:
    """
    Repräsentiert ein einsammelbares Objekt im Grid.
    Die Logik, was passiert, ist in 'apply_to' gekapselt.
    """
    def __init__(self, grid_x: int, grid_y: int, tile_size: int, ptype: PowerUpType):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.ptype = ptype
        
        self.sprite = None
        
        # Wir laden Grafiken nur für spezifische Typen, andere kriegen Farben
        if self.ptype == PowerUpType.PIZZA:
            # WICHTIG: Dateiname ohne Leerzeichen verwenden!
            self.sprite = load_scaled("assets/sprites/pizza.png", tile_size)

    # --------------------------------------------------------
    # Zeichnen (View)
    # --------------------------------------------------------
    def draw(self, screen: pygame.Surface, offset_x: int, offset_y: int) -> None:
        px = offset_x + self.grid_x * self.tile_size
        py = offset_y + self.grid_y * self.tile_size

        # Fall A: Wir haben ein echtes Bild (Pizza)
        if self.ptype == PowerUpType.PIZZA and self.sprite is not None:
            screen.blit(self.sprite, (px, py))
            return

        # Fall B: Kein Bild -> Wir zeichnen ein symbolisches Rechteck
        # (Spart Zeit bei der Asset-Erstellung für Party/ChatGPT)
        margin = self.tile_size // 6
        
        if self.ptype == PowerUpType.PARTY:
            color = (180, 80, 200) # Lila Party
        elif self.ptype == PowerUpType.CHATGPT:
            color = (80, 220, 180) # Türkis AI
        else:
            color = (255, 255, 0) # Fallback Gelb

        rect = pygame.Rect(
            px + margin,
            py + margin,
            self.tile_size - 2 * margin,
            self.tile_size - 2 * margin,
        )
        pygame.draw.rect(screen, color, rect)

    # --------------------------------------------------------
    # Wirkung (Logic)
    # --------------------------------------------------------
    def apply_to(self, level: "Level", student: "Student") -> str:
        """
        Wendet den Effekt des Items an.
        Rückgabe: Ein String für das HUD (Feedback an den Spieler).
        """
        if self.ptype == PowerUpType.PIZZA:
            student.has_pizza_shield = True
            # Info: student.pizza_shield_left müsste in entities.py ergänzt werden, 
            # falls wir einen Timer wollen. Fürs Erste reicht das Bool-Flag.
            return "Pizza: Ein Treffer vom Prof wird ignoriert. 🍕"

        if self.ptype == PowerUpType.PARTY:
            # Risiko-Item: 50/50 Chance
            delta = random.choice([-10.0, +10.0])
            
            # Zeit anpassen (aber nicht unter 5s fallen lassen)
            new_time = level.timer.time_left + delta
            # Wir nehmen an, level.timer.time_left ist public
            level.timer.time_left = max(5.0, new_time)

            if delta > 0:
                return "Party gut geplant: +10s BAföG-Zeit! 🎉"
            else:
                return "Party etwas eskaliert: -10s BAföG-Zeit… 😵"

        if self.ptype == PowerUpType.CHATGPT:
            # Einfacher Boost
            level.collected_ects += 1
            return "ChatGPT hilft dir bei der Klausur: +1 ECTS. 🤖"

        return ""
