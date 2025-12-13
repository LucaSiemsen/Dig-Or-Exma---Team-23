# src/tile.py
# ==============================================================================
# GenAI-Kennzeichnung
# Tool: Google Gemini
# Verwendungszweck: Implementierung der Datenstruktur gemäß Architekturvorgabe.
# Prompt: "Implementiere die 'Tile'-Klasse als atomare Einheit des Spielfeld-Grids.
#          Nutze Python Enums für Typsicherheit der Zustände (SOLID/EMPTY) zur 
#          Vermeidung von Magic Numbers und stelle eine kapselnde Methode für 
#          Zustandsübergänge (z.B. 'dig') bereit, die sich in die bestehende 
#          Level-Logik integriert."
# ==============================================================================
# Verantwortlich: Aaron Lehrke (937367)
# ==============================================================================

from enum import Enum, auto

# ==============================================================================
# TILE TYPE (Zustands-Definition)
# ==============================================================================
# Wir nutzen eine Enumeration (Enum) statt einfacher Zahlen (0, 1), 
# um den Code lesbarer und wartbarer zu machen.
class TileType(Enum):
    SOLID = auto()  # Blockierend (Stein oder etwas mauerartiges)
    EMPTY = auto()  # Begehbar (Tunnel, Boden)
    GRASS = auto()  # Oberste Reihe mit Blöcken, die oberhalb Grass auf dem Sprite haben


# ==============================================================================
# TILE KLASSE (Datenstruktur)
# ==============================================================================
# Diese Klasse repräsentiert ein einzelnes Quadrat auf dem Spielfeld.
# Sie zeigt den Zustand (Blockiert vs. Frei) und die Logik für Veränderungen.
class Tile:
    def __init__(self, ttype: TileType):
        self.type = ttype

    @property
    def is_solid(self) -> bool:
        """
        Gras ist auch fest! Deshalb geben wir True zurück,
        wenn es SOLID *oder* GRASS ist.
        """
        return self.type == TileType.SOLID or self.type == TileType.GRASS

    @property
    def is_empty(self) -> bool:
        return self.type == TileType.EMPTY

    def dig(self) -> None:
        """Egal ob Gras oder Erde: Nach dem Graben ist es leer."""
        self.type = TileType.EMPTY
