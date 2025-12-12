# level.py
# kümmert sich um das Spielfeld / Level:
# - Tiles (Blöcke)
# - ECTS (Sammelpunkte)
# - PowerUps (optional)
# - Professoren (Gegner)
# - BAföG-Timer (Zeitbegrenzung)

import random
import os
import pygame
from src.graphics import Sprite
from src.enemy import ProfessorEnemy
from src.powerups import PowerUp, PowerUpType

# versucht, die Werte aus config zu holen
try:
    from src.config import (
        GRID_COLS,
        GRID_ROWS,
        GRID_MARGIN_X_TILES,
        GRID_MARGIN_Y_TILES,
        BAFOEG_TIME_SECONDS,
        REQUIRED_ECTS,
        QUESTIONS_BY_PROF,
        PROFESSORS,
    )
    from .timer import BafoegTimer
except ImportError:
    # einfache Standardwerte, falls config oder timer noch fehlen
    GRID_COLS = 12
    GRID_ROWS = 8
    GRID_MARGIN_X_TILES = 2
    GRID_MARGIN_Y_TILES = 2
    BAFOEG_TIME_SECONDS = 120
    REQUIRED_ECTS = 5
    QUESTIONS_BY_PROF = {}
    PROFESSORS = []

    class BafoegTimer:
        # sehr einfache Variante eines Timers
        def __init__(self, start_time):
            self.time_left = start_time  # noch verbleibende Zeit
            self.is_over = False         # True, wenn Zeit abgelaufen

        def update(self, dt):
            # zieht dt von der Zeit ab
            if self.is_over:
                return
            self.time_left -= dt
            if self.time_left <= 0:
                self.time_left = 0
                self.is_over = True

    # einfache Ersatz-Variante, falls graphics.py fehlt
    class Sprite:
        def __init__(self, path, w, h):
            # macht einfach ein rotes Rechteck anstatt richtiger Grafik
            self.surface = pygame.Surface((w, h))
            self.surface.fill((200, 80, 80))

        def draw(self, screen, x, y):
            screen.blit(self.surface, (x, y))


class TileType:
    # einfache "Enum" für Tile-Arten
    SOLID = 0   # Erde / Block
    EMPTY = 1   # Tunnel


class Tile:
    # Repräsentiert ein einzelnes Feld im Grid
    def __init__(self, tile_type):
        self.type = tile_type   # speichert, ob SOLID oder EMPTY

    @property
    def is_solid(self):
        # True, wenn Block / Erde
        return self.type == TileType.SOLID

    @property
    def is_empty(self):
        # True, wenn Tunnel
        return self.type == TileType.EMPTY

    def dig(self):
        # macht aus einem Block einen Tunnel
        self.type = TileType.EMPTY


class ECTS:
    # Repräsentiert einen Sammelpunkt (Coin/ECTS)
    def __init__(self, grid_x, grid_y, tile_size):
        self.gx = grid_x
        self.gy = grid_y
        self.tile_size = tile_size

        # Coin-Sprite-Strip (13 Frames untereinander)
        self.frames = []
        self._load_coin_frames()

    def _load_coin_frames(self):
        # Pfad mit Leerzeichen ist okay, aber muss exakt stimmen
        path = os.path.join("assets", "sprites", "Coin v3 (kann man animiert darstellen).png")

        try:
            sheet = pygame.image.load(path).convert_alpha()
        except:
            # Fallback: wenn das Sheet nicht gefunden wird, nehmen wir Coin v1
            fallback = os.path.join("assets", "sprites", "Coin v1.png")
            img = pygame.image.load(fallback).convert_alpha()
            img = pygame.transform.scale(img, (self.tile_size, self.tile_size))
            self.frames = [img]
            return

        frame_w = sheet.get_width()
        frame_h = frame_w  # weil Frames quadratisch sind (16x16)
        count = sheet.get_height() // frame_h

        for i in range(count):
            rect = pygame.Rect(0, i * frame_h, frame_w, frame_h)
            frame = sheet.subsurface(rect).copy()
            frame = pygame.transform.scale(frame, (self.tile_size, self.tile_size))
            self.frames.append(frame)

        if not self.frames:
            self.frames = [pygame.Surface((self.tile_size, self.tile_size))]

    def draw(self, screen, offset_x, offset_y):
        px = offset_x + self.gx * self.tile_size
        py = offset_y + self.gy * self.tile_size

        # Animation über Zeit: alle 100ms ein Frame weiter
        idx = (pygame.time.get_ticks() // 100) % len(self.frames)
        screen.blit(self.frames[idx], (px, py))



class Level:
    # Repräsentiert das komplette Level (Spielfeld + Inhalte)
    def __init__(self, tile_size):
        # Initialisiert ein Level.
        # :param tile_size: Größe eines Tiles in Pixeln

        self.cols = GRID_COLS          # Anzahl Spalten
        self.rows = GRID_ROWS          # Anzahl Zeilen
        self.tile_size = tile_size     # Tile-Größe

        # 2D-Liste mit Tiles (erstmal alles SOLID)
        self.tiles = []
        for x in range(self.cols):
            spalte = []
            for y in range(self.rows):
                spalte.append(Tile(TileType.SOLID))
            self.tiles.append(spalte)

        # BAföG-Timer (Zeitbegrenzung)
        self.timer = BafoegTimer(BAFOEG_TIME_SECONDS)

        # Inhalte im Level
        self.ects_items = []      # Liste mit allen ECTS
        self.powerups = []        # Liste mit allen PowerUps
        self.professors = []      # Liste mit allen Professoren

        # Status vom Level
        self.collected_ects = 0   # bisher eingesammelte ECTS
        self.required_ects = REQUIRED_ECTS  # ECTS-Zahl zum Gewinnen
        self.is_game_over = False # True, wenn verloren
        self.is_won = False       # True, wenn gewonnen
        self.game_over_reason = ""        # Text, warum verloren wurde
        self.last_powerup_message = None  # Text zum letzten PowerUp-Effekt

        # beim Erzeugen direkt das Level aufbauen
        self._build_world()

    @property
    def is_finished(self):
        # True, wenn das Level vorbei ist (egal ob gewonnen/verloren/Zeit um)
        return self.is_game_over or self.is_won or self.timer.is_over

    def _build_world(self):
        """
        Baut ein einfaches Level:
        - alles SOLID
        - kleiner Starttunnel
        - ECTS auf zufälligen Feldern
        - PowerUps (falls vorhanden)
        - Professoren zufällig platzieren
        """

        # alles SOLID (zur Sicherheit, falls später was geändert wird)
        for x in range(self.cols):
            for y in range(self.rows):
                self.tiles[x][y].type = TileType.SOLID

        # kleiner Start-Tunnel links oben
        self.tiles[1][1].dig()
        self.tiles[1][2].dig()
        self.tiles[2][2].dig()

        # ECTS zufällig auf SOLID-Feldern verteilen (nicht auf Startfeld)
        ects_positions = set()
        while len(ects_positions) < self.required_ects:
            x = random.randrange(self.cols)
            y = random.randrange(self.rows)

            if (x, y) == (1, 1):
                continue   # nicht auf Startfeld

            if self.tiles[x][y].is_solid:
                ects_positions.add((x, y))

        for (x, y) in ects_positions:
            self.ects_items.append(ECTS(x, y, self.tile_size))
        # PowerUps auf einige ECTS-Felder legen
        kandidaten = list(ects_positions)
        random.shuffle(kandidaten)

        anzahl = max(1, self.required_ects // 2)  # z.B. Hälfte der Coins bekommt ein PowerUp
        type_list = list(PowerUpType)            # PIZZA, PARTY, CHATGPT

        for (x, y) in kandidaten[:anzahl]:
            ptype = random.choice(type_list)
            self.powerups.append(PowerUp(x, y, self.tile_size, ptype))

        # Professoren erzeugen
        for prof_info in PROFESSORS:
            bild_pfad = prof_info["sprite"]     # Bild für den Professor
            fragen_liste = prof_info["questions"]  # Fragen für diesen Prof

            sprite = Sprite(bild_pfad, self.tile_size, self.tile_size)

            # Prof soll zufällig erscheinen, aber:
            # - nicht auf Startfeld
            # - nicht auf einem Feld, wo schon ein anderer Prof steht
            while True:
                x = random.randrange(self.cols)
                y = random.randrange(self.rows)

                if (x, y) == (1, 1):
                    continue

                kollidiert = False
                for p in self.professors:
                    if p.grid_x == x and p.grid_y == y:
                        kollidiert = True
                        break
                if kollidiert:
                    continue

                prof = ProfessorEnemy(x, y, self.tile_size, sprite)
                prof.questions_pool = fragen_liste
                self.professors.append(prof)
                break

    def in_bounds(self, x, y):
        # prüft, ob (x,y) noch im Grid liegt
        # :return: True, wenn 0 <= x < cols und 0 <= y < rows
        return 0 <= x < self.cols and 0 <= y < self.rows

    def dig(self, x, y):
        # Hilfsfunktion, damit andere Klassen nicht direkt tiles[x][y] ändern
        self.tiles[x][y].dig()

    def update(self, dt):
        # wird pro Frame vom Game aufgerufen
        # :param dt: vergangene Zeit (Sekunden) seit letztem Frame

        if self.is_finished:
            return  # nichts mehr updaten, wenn Spiel vorbei

        # Timer aktualisieren
        self.timer.update(dt)
        if self.timer.is_over and not self.is_won:
            self.is_game_over = True
            self.game_over_reason = "BAföG-Zeit abgelaufen."

        # alle Professoren updaten (z.B. Bewegung)
        for prof in self.professors:
            prof.update(dt, self)

    def on_player_enter_tile(self, gx, gy, student):
        """
        Wird aufgerufen, wenn der Spieler ein neues Feld betritt.

        Hier passiert:
        - ECTS einsammeln
        - PowerUps auslösen
        - Gewinn überprüfen
        - schauen, ob ein Professor auf dem Feld steht
        :return: Professor-Objekt, wenn einer dort steht, sonst None
        """

        beruehrter_prof = None

        # ECTS einsammeln
        for ects in list(self.ects_items):
            if ects.gx == gx and ects.gy == gy:
                self.ects_items.remove(ects)
                self.collected_ects += 1

        # prüfen, ob genug ECTS für den Sieg gesammelt wurden
        if self.collected_ects >= self.required_ects and not self.is_game_over:
            self.is_won = True

        # PowerUps auslösen
        for p in list(self.powerups):
            if p.grid_x == gx and p.grid_y == gy:
                self.powerups.remove(p)
                nachricht = p.apply_to(self, student)
                if nachricht:
                    self.last_powerup_message = nachricht

        # prüfen, ob auf dem Feld ein Professor steht
        for prof in self.professors:
            if prof.grid_x == gx and prof.grid_y == gy:
                beruehrter_prof = prof
                break

        return beruehrter_prof

    def get_question_for_prof(self, prof):
        # gibt die Frage zurück, die zu einem Professor gehört
        return prof.get_question()

    def remove_professor(self, prof):
        # löscht einen Professor aus dem Level,
        # z.B. wenn die Frage richtig beantwortet wurde
        if prof in self.professors:
            self.professors.remove(prof)

    def draw(self, screen, offset_x, offset_y, block_solid, block_empty):
        # zeichnet das komplette Level (Tiles + ECTS + PowerUps + Professoren)
        # :param screen: pygame-Fenster
        # :param offset_x: X-Offset für das Level
        # :param offset_y: Y-Offset für das Level
        # :param block_solid: Objekt/Sprite für feste Blöcke
        # :param block_empty: Objekt/Sprite für Tunnel

        # Tiles zeichnen
        for x in range(self.cols):
            for y in range(self.rows):
                tile = self.tiles[x][y]
                px = offset_x + x * self.tile_size
                py = offset_y + y * self.tile_size

                if tile.is_solid:
                    block_solid.draw(screen, px, py)
                else:
                    block_empty.draw(screen, px, py)

        # ECTS zeichnen
        for ects in self.ects_items:
            ects.draw(screen, offset_x, offset_y)

        # PowerUps zeichnen
        for p in self.powerups:
            p.draw(screen, offset_x, offset_y)

        # Professoren zeichnen
        for prof in self.professors:
            prof.draw(screen, offset_x, offset_y)
