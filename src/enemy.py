import random
import pygame
from src.entities import Entity

# Wir holen uns die Fragen direkt aus unserer "Datenbank" (questions.py)
try:
    from src.questions import questions as QUESTION_DB
except ImportError:
    # Falls die Datei noch fehlt, nehmen wir Dummy-Daten, damit nix abstürzt
    QUESTION_DB = {
        1: {"prof_name": "Fallback", "question": "Frage?", "answers": ["A", "B", "C", "D"], "correct": 0}
    }

# --------------------------------------------------------------------------------
# GenAI-Kennzeichnung
# Tool: Google Gemini
# Prompt: Optimierung der Enemy-Klasse: Implementierung einer sauberen Vererbung 
#         von der Entity-Basisklasse sowie Logik für zufällige Bewegung im Grid.
# --------------------------------------------------------------------------------

class Enemy(Entity):
    """
    Basisklasse für alle Gegner (Dozenten & Klausuren).
    Hier steckt die Logik für Bewegung, Lebenspunkte und Fragen drin.
    """
    def __init__(self, grid_x: int, grid_y: int, tile_size: int, sprite: pygame.Surface, hp: int):
        # Position und Grafik an die Mutterklasse (Entity) weitergeben
        super().__init__(grid_x, grid_y, tile_size, sprite)
        
        self.hp = hp
        self.max_hp = hp
        
        # Ich wandle das Dictionary aus questions.py in eine Liste um,
        # damit ich mit random.choice() einfach zufällige Fragen ziehen kann.
        self.questions_pool = list(QUESTION_DB.values())
        
        # Kleiner Zufalls-Timer für die Bewegung, damit nicht alle Gegner
        # exakt gleichzeitig loslaufen (sieht natürlicher aus).
        self._move_cooldown = random.uniform(0.5, 1.5)

    def get_question(self) -> dict:
        """
        Gibt eine zufällige Frage aus dem Pool zurück, wenn der Spieler
        in den Gegner reinläuft.
        """
        if not self.questions_pool:
            # Sollte eigentlich nicht passieren, aber sicher ist sicher
            return {
                "prof_name": "Fehler", 
                "question": "Keine Fragen gefunden!", 
                "answers": ["Ok", "Ok", "Ok", "Ok"], 
                "correct": 0
            }
        
        # Zufällige Frage auswählen
        return random.choice(self.questions_pool)

    def take_answer(self) -> bool:
        """
        Wird aufgerufen, wenn der Spieler eine Frage richtig beantwortet hat.
        Zieht 1 HP ab.
        Rückgabe: True, wenn der Gegner besiegt ist (HP <= 0).
        """
        self.hp -= 1
        # Debug-Print, damit ich in der Konsole sehe, was passiert
        print(f"Gegner {self.__class__.__name__} getroffen! Verbleibende HP: {self.hp}")
        
        return self.hp <= 0

    def update(self, dt: float, level) -> None:
        """
        Steuert die KI-Bewegung des Gegners.
        Wird jeden Frame vom Level aufgerufen.
        """
        # Cooldown runterzählen
        self._move_cooldown -= dt
        
        # Wenn wir noch warten müssen oder das Level vorbei ist -> nix tun
        if self._move_cooldown > 0 or level.is_finished:
            return

        # Cooldown neu setzen (leicht zufällig)
        self._move_cooldown = random.uniform(0.8, 1.2)

        # Versuchen, in eine zufällige Richtung zu laufen
        # (Oben, Unten, Links, Rechts)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = self.grid_x + dx, self.grid_y + dy
            
            # Check: Ist das Feld überhaupt noch im Level?
            if not level.in_bounds(nx, ny):
                continue
            
            # Check: Steht da schon ein anderer Prof? (Wir wollen nicht stapeln)
            # 'level.professors' ist die Liste aller Gegner im Level
            if hasattr(level, 'professors') and any(e.grid_x == nx and e.grid_y == ny for e in level.professors):
                continue
                
            # Wenn alles frei ist -> Position updaten und Schleife abbrechen
            self.grid_x = nx
            self.grid_y = ny
            break


class Dozent(Enemy):
    """
    Der Standard-Gegner.
    Braucht nur 1 richtige Antwort, um besiegt zu werden.
    """
    def __init__(self, grid_x: int, grid_y: int, tile_size: int, sprite: pygame.Surface):
        # Ruft den Enemy-Konstruktor mit 1 HP auf
        super().__init__(grid_x, grid_y, tile_size, sprite, hp=1)


class Klausur(Enemy):
    """
    Der Boss-Gegner.
    Braucht 5 richtige Antworten und bewegt sich langsamer.
    """
    def __init__(self, grid_x: int, grid_y: int, tile_size: int, sprite: pygame.Surface):
        # Klausuren sind zäh: 5 HP
        super().__init__(grid_x, grid_y, tile_size, sprite, hp=5)
    
    def update(self, dt: float, level) -> None:
        # Trick: Ich übergebe nur die halbe Zeit (dt * 0.5) an die Update-Funktion.
        # Dadurch läuft der Timer langsamer ab und die Klausur bewegt sich nur halb so oft.
        super().update(dt * 0.5, level)

# Damit der alte Code in level.py nicht crasht, der noch "ProfessorEnemy" sucht:
ProfessorEnemy = Dozent
