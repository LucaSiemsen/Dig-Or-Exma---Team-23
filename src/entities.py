from __future__ import annotations

from typing import Optional, TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from src.level import Level
    from src.enemy import ProfessorEnemy


# kleine Hilfsfunktion zum Laden + Skalieren von Bildern
def load_scaled(path: str, size: int) -> pygame.Surface:
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (size, size))
# Basisklasse für Gegner (Enemy) – Student benutzt sie NICHT.
# Das ist nur notwendig, weil enemy.py davon erbt.
# (Rekonstruktion einer alten Entity-Klasse, die früher existierte.)

class Entity:
    def __init__(self, grid_x, grid_y, tile_size, sprite):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.sprite = sprite  # kann Sprite-Objekt ODER Surface sein

    def draw(self, screen, offset_x, offset_y):
        px = offset_x + self.grid_x * self.tile_size
        py = offset_y + self.grid_y * self.tile_size

        # Wenn das Sprite-Objekt selbst eine draw()-Methode hat (graphics.Sprite),
        # rufen wir diese auf. Ansonsten gehen wir davon aus, dass es ein Surface ist.
        if hasattr(self.sprite, "draw"):
            self.sprite.draw(screen, px, py)
        else:
            screen.blit(self.sprite, (px, py))


class Student:
    # repräsentiert den Spieler im Grid
    def __init__(self, grid_x: int, grid_y: int, tile_size: int, sprite: pygame.Surface):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size

        # das ursprünglich übergebene Bild hebe ich als Idle-Bild auf
        self.sprite = pygame.transform.scale(sprite, (tile_size, tile_size))

        # Richtung, in die der Student sich zuletzt bewegt hat
        self.last_dx = 0
        self.last_dy = 1  # Start: schaut nach unten

                # Animation Frames laden (unsere Team-Sprites)

        # Rechtslauf – nur die einzelnen Frames benutzen
        self.anim_right = [
            load_scaled("assets/sprites/student move right einzeln.png", tile_size),
            load_scaled("assets/sprites/Student move right einzeln 1.png", tile_size),
        ]

        # Linkslauf – hier gibt es nur einen "einzeln", ich dupliziere ihn einfach
        self.anim_left = [
            load_scaled("assets/sprites/Student move left einzeln.png", tile_size),
            load_scaled("assets/sprites/Student move left einzeln.png", tile_size),
        ]

        # Untenlauf – nur die zwei Einzelframes, NICHT das Sprite-Sheet
        self.anim_down = [
            load_scaled("assets/sprites/Student move down einzeln.png", tile_size),
            load_scaled("assets/sprites/Student move down einzeln (2).png", tile_size),
        ]

        # Obenlauf – die drei Einzelframes
        self.anim_up = [
            load_scaled("assets/sprites/Student move up einzeln 1.png", tile_size),
            load_scaled("assets/sprites/Student move up einzeln 2.png", tile_size),
            load_scaled("assets/sprites/Student move up einzeln 3.png", tile_size),
        ]



        # Idle Bild, wenn er steht
        self.idle = self.sprite

        # aktueller Animationszustand
        self.current_frames: list[pygame.Surface] = [self.idle]
        self.frame = 0
        self.frame_timer = 0.0
        self.frame_speed = 0.15  # kleiner = schneller

        # falls wir in einen Professor reinlaufen und der eine Frage hat
        self.pending_question = None  # kommt aus questions.py
        self.pending_professor: Optional["ProfessorEnemy"] = None

        # Status von PowerUps (z.B. Pizza-Schild)
        self.has_pizza_shield: bool = False

    @property
    def pos(self) -> tuple[int, int]:
        # aktuelle Position im Grid
        return self.grid_x, self.grid_y

    def reset(self, grid_x: int, grid_y: int) -> None:
        # Student auf Startposition zurücksetzen (z.B. bei Restart)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pending_question = None
        self.pending_professor = None
        self.last_dx = 0
        self.last_dy = 1
        self.current_frames = [self.idle]
        self.frame = 0
        self.frame_timer = 0.0

    def move(self, dx: int, dy: int, level: "Level") -> Optional["ProfessorEnemy"]:
        """
        bewegt den Studenten um ein Feld.
        das Level kümmert sich dann um:
        - Graben
        - ECTS
        - PowerUps
        - Professoren
        """

        # wenn das Level schon vorbei ist, machen wir nichts mehr
        if level.is_finished:
            return None

        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        # nicht aus dem Spielfeld rauslaufen
        if not level.in_bounds(new_x, new_y):
            return None

        # wenn da noch Erde ist, dann wird automatisch gegraben
        if level.tiles[new_x][new_y].is_solid:
            level.dig(new_x, new_y)

        # Position aktualisieren
        self.grid_x = new_x
        self.grid_y = new_y

        # letzte Bewegungsrichtung merken (wichtig für Animation)
        if dx != 0 or dy != 0:
            self.last_dx = dx
            self.last_dy = dy

        # Level fragen, was auf dem neuen Feld liegt (ECTS, PowerUp, Professor)
        prof = level.on_player_enter_tile(new_x, new_y, self)

        # falls wir einen Professor getroffen haben, merken wir uns das
        if prof is not None:
            self.pending_professor = prof
            self.pending_question = prof.get_question()

        return prof

    def update_animation(self, dt: float) -> None:
        # anhand der letzten Richtung auswählen, welche Frames benutzt werden

        if self.last_dx > 0:
            self.current_frames = self.anim_right
        elif self.last_dx < 0:
            self.current_frames = self.anim_left
        elif self.last_dy > 0:
            self.current_frames = self.anim_down
        elif self.last_dy < 0:
            self.current_frames = self.anim_up
        else:
            # steht gerade, also Idle
            self.current_frames = [self.idle]

        # wenn nur ein Frame da ist (Idle), nicht animieren
        if len(self.current_frames) <= 1:
            self.frame = 0
            return

        # Animationslogik:
        # Diesen Teil habe ich mir von ChatGPT erklären lassen,
        # weil ich den Framewechsel mit Timer alleine nicht so hinbekommen hätte.
        self.frame_timer += dt
        if self.frame_timer >= self.frame_speed:
            self.frame = (self.frame + 1) % len(self.current_frames)
            self.frame_timer = 0.0

    def draw(self, screen: pygame.Surface, offset_x: int, offset_y: int) -> None:
        # Student an die richtige Stelle im Fenster zeichnen
        px = offset_x + self.grid_x * self.tile_size
        py = offset_y + self.grid_y * self.tile_size
        screen.blit(self.current_frames[self.frame], (px, py))



# ==============================================================================
# GenAI-Kennzeichnung & Reflexion
# Tool: Google Gemini
# Verwendungszweck: Syntaktische Umsetzung des Entwurfsmusters "Vererbung".
# Prompt: "Erstelle eine abstrakte Basisklasse 'Entity' für ein Grid-basiertes Spiel,
#          die Redundanzen zwischen Spieler- und Gegner-Objekten (Position, Rendering)
#          eliminiert (DRY-Prinzip) und Polymorphie beim Zeichnen ermöglicht."
# ==============================================================================
# BASISKLASSE: ENTITY (Wird an Enemy vererbt)
# Author/Verantwortlich: Aaron Lehrke (937367)
# ==============================================================================
# Diese Klasse fungiert als zentraler Baustein (Parent Class) für alle beweglichen
# Objekte im Spiel (Gegner, Projektile, etc.).
# Ziel: Reduzierung von Code-Duplizierung. Anstatt dass jeder Gegnertyp eigene
# x/y-Variablen verwaltet, erben sie diese Funktionalität zentral von hier.
class Entity:
    def __init__(self, grid_x: int, grid_y: int, tile_size: int, sprite):
        """
        Initialisiert ein generisches Objekt auf dem Spielfeld.
        
        Args:
            grid_x, grid_y: Logische Koordinaten im Raster (nicht Pixel!).
            tile_size: Größe einer Kachel in Pixeln (für die Umrechnung).
            sprite: Das visuelle Objekt. Das kann entweder ein einfaches 
                    pygame.Surface sein oder eine komplexe Instanz aus graphics.py.
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.sprite = sprite

    @property
    def pos(self) -> tuple[int, int]:
        """
        Getter-Methode (Property), die den direkten Zugriff auf die Koordinaten
        kapselt. Gibt die Position als Tupel (x, y) zurück, was für
        Kollisionsabfragen im Level-Management benötigt wird.
        """
        return self.grid_x, self.grid_y

    def draw(self, screen, offset_x, offset_y):
        """
        Zentrale Rendering-Logik (View-Ebene).
        Wandelt die abstrakten Grid-Koordinaten in konkrete Pixel-Koordinaten um
        und bringt das Objekt auf den Bildschirm.
        """
        # Umrechnung: Logische Position * Kachelgröße + Verschiebung (Camera Offset)
        px = offset_x + self.grid_x * self.tile_size
        py = offset_y + self.grid_y * self.tile_size

        # WICHTIG: Polymorphie-Check (Duck Typing)
        # Wir prüfen hier dynamisch zur Laufzeit, welche Art von Grafik-Objekt wir haben.
        # Fall A: Es ist eine komplexe Klasse aus 'graphics.py' (hat eine .draw()-Methode).
        if hasattr(self.sprite, "draw"):
            self.sprite.draw(screen, px, py)
        # Fall B: Es ist ein einfaches Pygame-Bild (Surface).
        else:
            screen.blit(self.sprite, (px, py))
