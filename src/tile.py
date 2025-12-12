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
    SOLID = auto()  # Blockierend (z.B. Bücherstapel, Erde)
    EMPTY = auto()  # Begehbar (Tunnel, Boden)


# ==============================================================================
# TILE KLASSE (Datenstruktur)
# ==============================================================================
# Diese Klasse repräsentiert ein einzelnes Quadrat auf dem Spielfeld.
# Sie kapselt den Zustand (Blockiert vs. Frei) und die Logik für Veränderungen.
class Tile:
    def __init__(self, ttype: TileType):
        """
        Initialisiert das Feld.
        Args:
            ttype: Der Typ des Feldes (TileType.SOLID oder TileType.EMPTY).
        """
        self.type = ttype

    @property
    def is_solid(self) -> bool:
        """
        Getter-Property: Prüft, ob das Feld ein Hindernis ist.
        WICHTIG: Wird von level.py für die Kollisionsabfrage benötigt!
        """
        return self.type == TileType.SOLID

    @property
    def is_empty(self) -> bool:
        """
        Getter-Property: Prüft, ob das Feld begehbar ist.
        """
        return self.type == TileType.EMPTY

    def dig(self) -> None:
        """
        Zustandsübergang: Verwandelt ein festes Feld (SOLID) in einen Tunnel (EMPTY).
        Wird aufgerufen, wenn der Student gegen ein grabbares Hindernis läuft.
        """
        self.type = TileType.EMPTY
