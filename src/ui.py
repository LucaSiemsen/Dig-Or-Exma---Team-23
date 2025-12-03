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
