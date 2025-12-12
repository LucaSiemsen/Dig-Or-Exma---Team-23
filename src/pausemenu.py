#pausemenu.py
import pygame
from .ui import VolumeSlider

class PauseMenu:
    def __init__(self, width: int, height: int, font_title: pygame.font.Font, font_small: pygame.font.Font, sound_manager):
        self.width = width
        self.height = height
        self.font_title = font_title
        self.font_small = font_small
        self.sound_manager = sound_manager #Referenz auf SoundManager (für Lautstärke)
        self.overlay = pygame.Surface((self.width, self.height))
        self.overlay.set_alpha(180)
        self.overlay.fill((0, 0, 0))
        button_width, button_height = 320, 50
        center_x, center_y = width // 2, height // 2

        self.button_resume = pygame.Rect(center_x - button_width//2, center_y - 10,  button_width, button_height)
        self.button_menu   = pygame.Rect(center_x - button_width//2, center_y + 60,  button_width, button_height)

        self.color_normal = (220, 220, 220) #Farbe für normale Buttons
        self.color_hover  = (255, 255, 255) #Farbe für Button-Hover-Effekt

        #Lautstärke-Slider anlegen und über dem Button platzieren
        slider_w, slider_h = 280, 18
        slider_x = center_x - slider_w // 2
        slider_y = center_y - 70
        self.volume_slider = VolumeSlider(slider_x, slider_y, slider_w, slider_h, self.sound_manager, self.font_small)


    #slider klickbar machen
    def handle_click(self, pos): 
        if self.volume_slider.handle_click(pos):
            return None
        if self.button_resume.collidepoint(pos):
            return "resume" #Signal an Game: Spiel fortsetzen (Code dazu in Game.py)
        if self.button_menu.collidepoint(pos):
            return "menu" #Signal an Game: zurück ins Hauptmenü
        return None #Klick war auf nichts relevantes

    #zeichnet das komplette Pause-Menü
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.overlay, (0, 0))

        
        center_x = self.width // 2
        center_y = self.height // 2

        title_surface = self.font_title.render("PAUSE", True, (255, 255, 100))
        screen.blit(title_surface, title_surface.get_rect(center=(center_x, center_y - 120)))

        self.volume_slider.draw(screen)

        mouse_pos = pygame.mouse.get_pos() #aktuelle Mausposition holen
        color_res = self.color_hover if self.button_resume.collidepoint(mouse_pos) else self.color_normal
        color_menu = self.color_hover if self.button_menu.collidepoint(mouse_pos) else self.color_normal

        pygame.draw.rect(screen, color_res, self.button_resume, border_radius=15)
        pygame.draw.rect(screen, color_menu, self.button_menu, border_radius=15)
        resume_text_surface = self.font_small.render("Weiter", True, (20, 20, 20))
        menu_text_surface   = self.font_small.render("Hauptmenü", True, (20, 20, 20))
        
        screen.blit(resume_text_surface, resume_text_surface.get_rect(center=self.button_resume.center))
        screen.blit(menu_text_surface,   menu_text_surface.get_rect(center=self.button_menu.center))

        hint = self.font_small.render("Tastatur: SHIFT (Weiter) | R (Neustart)", True, (200, 200, 200))
        screen.blit(hint, hint.get_rect(center=(center_x, center_y + 140)))