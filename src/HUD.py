import pygame

class Mutebutton:
     def __init__(self, x, y, size, sound_manager):
        self.rect = pygame.Rect(x, y, size, size)
        self.sound_manager = sound_manager
        img_mute = pygame.image.load("assets/sprites/mute.png").convert_alpha()
        img_unmute = pygame.image.load("assets/sprites/unmute.png").convert_alpha()
        self.img_mute = pygame.transform.scale(img_mute, (size, size))
        self.img_unmute = pygame.transform.scale(img_unmute, (size, size))
    
     def draw(self, screen):
        img = self.img_mute if self.sound_manager.is_muted else self.img_unmute
        screen.blit(img, self.rect.topleft)
    
     def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.sound_manager.toggle_mute()