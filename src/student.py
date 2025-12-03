# ============================================================
# student.py – Unsere Spielfigur
# Kann: bewegen, graben, sammeln, Fragen beantworten
# ============================================================

from .graphics import Sprite

class Student:

    def __init__(self, gx, gy, tile_size):
        self.gx = gx
        self.gy = gy
        self.tile_size = tile_size

        self.sprite = Sprite("assets/sprites/student.png", tile_size)

        # PowerUps
        self.has_pizza_shield = False

    @property
    def pos(self):
        return self.gx, self.gy

    def move(self, dx, dy, level):
        """Bewegt den Spieler einen Schritt UND gräbt automatisch."""

        nx = self.gx + dx
        ny = self.gy + dy

        if not level.in_bounds(nx, ny):
            return

        # block freigraben
        tile = level.tiles[nx][ny]
        tile.dig()

        # bewegen
        self.gx, self.gy = nx, ny

        # pickups / fragen prüfen
        level.check_collect(nx, ny)
        level.check_question(nx, ny)
        level.check_enemy_collision(nx, ny)

    def draw(self, surf, ox, oy):
        px = ox + self.gx * self.tile_size
        py = oy + self.gy * self.tile_size
        self.sprite.draw(surf, px, py)
