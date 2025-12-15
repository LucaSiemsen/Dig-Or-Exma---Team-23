# ============================================================
# ui.py – UI-Fenster für Professorfragen
# ============================================================

import pygame
from .questions import questions
from .config import WHITE

class QuestionUI:

    def __init__(self, font_big, font_small):
        self.font_big = font_big
        self.font_small = font_small

        self.active = False
        self.qid = None
        self.selected = 0

    def open(self, qid):
        self.active = True
        self.qid = qid
        self.selected = 0

    def close(self):
        self.active = False
        self.qid = None

    def update(self, event):
        if not self.active:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % 4
            if event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % 4
            if event.key == pygame.K_RETURN:
                q = questions[self.qid]
                if self.selected == q["correct"]:
                    return True
                return False

        return None

    def draw(self, surf):
        if not self.active:
            return

        q = questions[self.qid]
        cx = surf.get_width() // 2

        title = self.font_big.render(q["prof_name"], True, WHITE)
        surf.blit(title, title.get_rect(center=(cx, 150)))

        question = self.font_small.render(q["question"], True, WHITE)
        surf.blit(question, question.get_rect(center=(cx, 220)))

        for i, ans in enumerate(q["answers"]):
            color = (255,200,50) if i == self.selected else WHITE
            line = self.font_small.render(ans, True, color)
            surf.blit(line, line.get_rect(center=(cx, 300 + i*40)))


#Autor: Dimitri Homutov (935939)
#GEN AI Kennzeichnung: Dieser Code wurde mit Unterstützung von KI-Technologie generiert.
#Tool: Google Gemini
#Prompt "Ich möchte die Möglichkeit haben, die Musik leiser und lauter zu machen über quasi eine art audio slider. Wie mache ich das??"
class VolumeSlider:
    def __init__(self, x, y, width, height, sound_manager, font):
        self.rect = pygame.Rect(x, y, width, height) 
        self.sound_manager = sound_manager
        self.font = font 

        self.num_blocks = 10 #Legt fest, dass der Slider aus 10 Blöcken besteht (visuelle Segmente).
        self.gap = 4 #Abstand in Pixeln zwischen Blocks.

        # Farben
        self.col_empty = (80, 80, 80) 
        self.col_fill  = (100, 200, 100) 
        self.col_text  = (200, 200, 200) 
        self.col_hover = (255, 255, 255) 

        #Texte
        self.title = "Musik-Lautstärke" 
        self.button_minus = "[-]"
        self.button_plus  = "[+]"

        self.title_label = self.font.render(self.title, True, (220, 220, 220)) #hier sagen wir mit welchen Werten der Titel gerendert werden soll (aufgemalt)

        #Button Hitboxen erstellen, Minus Button (Links)
        button_size = 28 
        minus_x = self.rect.left - 15 - button_size
        minus_y = self.rect.centery - button_size // 2
        self.rect_minus = pygame.Rect(minus_x, minus_y, button_size, button_size)

        #Plus Button (Rechts)
        plus_x = self.rect.right + 15
        plus_y = self.rect.centery - button_size // 2
        self.rect_plus = pygame.Rect(plus_x, plus_y, button_size, button_size)

        #Hier wird ausgerechnet, wie breit jeder einzelne Block in deinem Slider sein muss, damit 10 Blöcke plus die Zwischenräume in die Gesamtbreite passen.
        total_gap = (self.num_blocks - 1) * self.gap
        self.block_width = (self.rect.width - total_gap) // self.num_blocks

    def _draw_button(self, screen, rect, text):
        mouse_pos = pygame.mouse.get_pos() #aktuelle Mausposition abfragen
        col = self.col_hover if rect.collidepoint(mouse_pos) else self.col_text #prüft ob die Maus über dem Button ist und passt Farbe an
        surf = self.font.render(text, True, col) #unseren Text zeichnen
        screen.blit(surf, surf.get_rect(center=rect.center)) #zeichnet den Text zentriert im Button-Rechteck

    def draw(self, screen):
        # Titel darstellen
        title_center_x = self.rect.centerx
        title_center_y = self.rect.top - 25
        screen.blit(self.title_label, self.title_label.get_rect(center=(title_center_x, title_center_y)))

        # Buttons
        self._draw_button(screen, self.rect_minus, self.button_minus)
        self._draw_button(screen, self.rect_plus, self.button_plus)
        # Blöcke
        vol = self.sound_manager.get_music_volume() #aktuelle Lautstärke holen
        filled = int(round(vol * self.num_blocks)) #für die Anzahl der gefüllten Blöcke

        #jeden Block zeichnen
        for i in range(self.num_blocks):
            bx = self.rect.x + i * (self.block_width + self.gap)
            block_rect = pygame.Rect(bx, self.rect.y, self.block_width, self.rect.height)
            col = self.col_fill if i < filled else self.col_empty
            pygame.draw.rect(screen, col, block_rect, border_radius=2)

    def handle_click(self, pos):
        vol = self.sound_manager.get_music_volume()
        step = 1.0 / self.num_blocks

        if self.rect_minus.collidepoint(pos):
            self.sound_manager.set_music_volume(max(0.0, vol - step))
            return True

        if self.rect_plus.collidepoint(pos):
            self.sound_manager.set_music_volume(min(1.0, vol + step))
            return True

        return False

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
        screen.blit(img, (self.rect.x, self.rect.y))  

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.sound_manager.toggle_mute()