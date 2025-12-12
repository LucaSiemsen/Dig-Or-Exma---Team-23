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


class VolumeSlider:
    def __init__(self, x, y, width, height, sound_manager, font):
        self.rect = pygame.Rect(x, y, width, height) #rahmen für den Slider
        self.sound_manager = sound_manager #Soundmanager Referenz
        self.font = font #Schriftart für Texte

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

        #Button Hitboxen erstellen (für Klick-Erkennung)
        #Minus Button (Links)
        minus_surface = self.font.render(self.button_minus, True, self.col_text) #wir machen aus dem Text ein Surface (bild)
        minus_rect = minus_surface.get_rect() #get rect baut mir ein Rechteck um das Surface (Bild)
        minus_rect.midright = (self.rect.left - 15, self.rect.centery)
        self.rect_minus = minus_rect.inflate(10, 10) #macht das Rect größer, damit es leichter anklickbar ist.
        
        # Plus Button (Rechts)
        plus_surface = self.font.render(self.button_plus, True, self.col_text) #wir machen aus dem Text ein Surface (bild)
        plus_rect = plus_surface.get_rect() #get rect baut mir ein Rechteck um das Surface (Bild)
        plus_rect.midleft = (self.rect.right + 15, self.rect.centery)
        self.rect_plus = plus_rect.inflate(10, 10)

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
        # zentrieren des Titels über dem Slider-Rechteck
        title_rect = self.title_label.get_rect(center=(self.rect.centerx, self.rect.top - 25))
        screen.blit(self.title_label, title_rect)

        # Buttons
        self._draw_button(screen, self.rect_minus, self.button_minus)
        self._draw_button(screen, self.rect_plus, self.button_plus)
        # Blöcke
        vol = self.sound_manager.get_music_volume()  # 0..1
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

def draw_buff_timer_top_right(screen, font, student, x=1100, y=20, size=40, gap=2):
    if student is None:
        return

    if student.has_pizza_shield and student.pizza_shield_left > 0:
        secs = int(student.pizza_shield_left)
        text = font.render(f"Schild: {secs}s", True, (255, 255, 255))

        img_shield = pygame.image.load("assets/sprites/pizza ganz.png").convert_alpha()
        img_shield = pygame.transform.scale(img_shield, (size, size))

        screen.blit(img_shield, (x, y))

        text_rect = text.get_rect(midleft=(x + size + gap, y + size // 2))
        screen.blit(text, text_rect)
