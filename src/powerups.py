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
import random

if TYPE_CHECKING:
    from .level import Level
    from .entities import Student

# Hilfsfunktion zum sicheren Laden von Bildern
def load_scaled(path: str, size: int) -> pygame.Surface | None:
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (size, size))
    except FileNotFoundError:
        # Gibt None zurück, damit wir wissen, dass das Bild fehlt
        # und wir stattdessen ein farbiges Rechteck zeichnen können.
        print(f"Asset-Warnung: {path} nicht gefunden.")
        return None

class PowerUpType(Enum):
    PIZZA = auto()    # Schutzschild
    PARTY = auto()    # Zeit-Modifikation (Risiko)
    CHATGPT = auto()  # ECTS Boost

class PowerUp:
    """
    Repräsentiert ein einsammelbares Item.
    Kapselt Rendering (View) und Effekt-Logik (Model).
    """
    def __init__(self, grid_x: int, grid_y: int, tile_size: int, ptype: PowerUpType):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.ptype = ptype
        
        self.sprite = None
        
        # Asset-Zuordnung: Hier werden die Dateinamen definiert
        if self.ptype == PowerUpType.PIZZA:
            self.sprite = load_scaled("assets/sprites/pizza.png", tile_size)
        elif self.ptype == PowerUpType.PARTY:
            self.sprite = load_scaled("assets/sprites/party.png", tile_size)
        elif self.ptype == PowerUpType.CHATGPT:
            self.sprite = load_scaled("assets/sprites/chatgpt.png", tile_size)

    # --------------------------------------------------------
    # Zeichnen (View-Ebene)
    # --------------------------------------------------------
    def draw(self, screen: pygame.Surface, offset_x: int, offset_y: int) -> None:
        px = offset_x + self.grid_x * self.tile_size
        py = offset_y + self.grid_y * self.tile_size

        # PRIORITÄT A: Wenn das Sprite erfolgreich geladen wurde -> Zeichnen
        if self.sprite is not None:
            screen.blit(self.sprite, (px, py))
            return

        # PRIORITÄT B: Fallback (falls Bilddatei fehlt) -> Farbiges Rechteck
        # Das garantiert, dass das Spiel spielbar bleibt, auch ohne Assets.
        margin = self.tile_size // 6
        
        if self.ptype == PowerUpType.PARTY:
            color = (180, 80, 200) # Lila
        elif self.ptype == PowerUpType.CHATGPT:
            color = (80, 220, 180) # Türkis
        elif self.ptype == PowerUpType.PIZZA:
            color = (255, 100, 100) # Rot
        else:
            color = (255, 255, 0) # Gelb (Unbekannt)

        rect = pygame.Rect(
            px + margin,
            py + margin,
            self.tile_size - 2 * margin,
            self.tile_size - 2 * margin,
        )
        pygame.draw.rect(screen, color, rect)

    # --------------------------------------------------------
    # Logik anwenden (Business Logic)
    # --------------------------------------------------------
    def apply_to(self, level: "Level", student: "Student") -> str:
        """
        Wendet den Effekt polymorph auf Level oder Student an.
        Returns: Feedback-Text für das HUD.
        """
        
        # Pizza: Setzt den Status im Studenten-Objekt
        if self.ptype == PowerUpType.PIZZA:
            student.has_pizza_shield = True
            return "Pizza: Ein Treffer vom Prof wird ignoriert! 🍕"

        # Party: Manipuliert die globale Level-Zeit
        if self.ptype == PowerUpType.PARTY:
            delta = random.choice([-10.0, +10.0])
            new_time = max(5.0, level.timer.time_left + delta)
            level.timer.time_left = new_time

            if delta > 0:
                return "Party gut geplant: +10s BAföG-Zeit! 🎉"
            else:
                return "Party eskaliert: -10s BAföG-Zeit... 😵"

        # ChatGPT: Manipuliert den Score
        if self.ptype == PowerUpType.CHATGPT:
            level.collected_ects += 1
            return "ChatGPT hilft bei der Klausur: +1 ECTS! 🤖"

        return ""
