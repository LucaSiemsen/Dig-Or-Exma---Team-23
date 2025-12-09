import pygame

class Mutebutton:
    def __init__(self, x, y, size, sound_manager):
        self.rect = pygame.Rect(x, y, size, size)
        self.sound_manager = sound_manager

        img_mute = pygame.image.load("assets/sprites/mute.png").convert_alpha()
        img_unmute = pygame.image.load("assets/sprites/unmute.png").convert_alpha()

        icon_size = 32  
        self.img_mute = pygame.transform.scale(img_mute, (icon_size, icon_size))
        self.img_unmute = pygame.transform.scale(img_unmute, (icon_size, icon_size))

    def draw(self, screen):
        img = self.img_mute if self.sound_manager.is_muted else self.img_unmute
        screen.blit(img, (self.rect.x, self.rect.y))  # <<< oben links (nicht zentriert)

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.sound_manager.toggle_mute()