# ============================================================
# tile.py – Repräsentiert ein Feld im Grid (Erde / Tunnel)
# ============================================================

from enum import Enum, auto

class TileType(Enum):
    SOLID = auto()
    EMPTY = auto()


class Tile:
    """Ein Feld im Spielfeld."""

    def __init__(self, ttype: TileType):
        self.type = ttype

    @property
    def passable(self):
        """Spieler und Gegner können nur durch EMPTY laufen."""
        return self.type == TileType.EMPTY

    def dig(self):
        """Erde entfernen → zu Tunnel."""
        self.type = TileType.EMPTY
