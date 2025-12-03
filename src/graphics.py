# graphics.py
# ----------------------------------------------------------
# Mini-Hilfsklasse zum Laden und Zeichnen von Bildern.
# So müssen wir nicht überall pygame.image.load schreiben.
# ----------------------------------------------------------

import pygame


class Sprite:
    def __init__(self, path: str, width: int, height: int):
        # Bild laden und direkt auf die gewünschte Größe skalieren
        img = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(img, (width, height))

    def draw(self, surface: pygame.Surface, x: int, y: int) -> None:
        surface.blit(self.image, (x, y))
