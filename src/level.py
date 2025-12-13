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
from src.tile import Tile, TileType

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
        LEVELS,
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
    LEVELS = [{"ects": REQUIRED_ECTS, "pizzas": 1, "prof_count": len(PROFESSORS), "guard_mode": False}]


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
    def __init__(self, tile_size, level_index: int = 0):
        self.level_index = level_index

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
        Baut das Level abhängig von self.level_index.

        Idee dahinter (simpel gehalten):
        - Level 1: 2 Profs laufen frei rum, 2 ECTS random, 1 Pizza
        - Level 2: 2 Profs, einer startet direkt neben einem ECTS ("bewacht"), 2 ECTS random, 2 Pizza
        - Level 3: 3 ECTS nahe Ecken fix, pro ECTS ein Prof (spawnt in der Nähe), 3 Pizza
        - Level 4: 3 ECTS, zwei nah beieinander, Profs kommen sich eher in die Quere, 4 Pizza

        Hinweis:
        "Radius laufen" machen wir später in enemy.py, erstmal nur Spawn-Logik,
        damit man die Level-Unterschiede sofort merkt.
        """

        # ----------------------------
        # 0) Level-Config holen + absichern
        # ----------------------------
        if not LEVELS:
            # falls config kaputt ist, lieber nicht crashen
            cfg = {"ects": REQUIRED_ECTS, "pizzas": 1, "prof_count": len(PROFESSORS), "guard_mode": False}
        else:
            idx = max(0, min(self.level_index, len(LEVELS) - 1))
            cfg = LEVELS[idx]

        ects_target = int(cfg.get("ects", REQUIRED_ECTS))
        pizza_target = int(cfg.get("pizzas", 1))
        prof_target = int(cfg.get("prof_count", len(PROFESSORS)))
        guard_mode = bool(cfg.get("guard_mode", False))

        # ----------------------------
        # 1) Tiles resetten (Gras oben, Erde unten)
        # ----------------------------
        for x in range(self.cols):
            for y in range(self.rows):
                if y == 0:
                    # Oberste Reihe ist Gras
                    self.tiles[x][y] = Tile(TileType.GRASS)
                else:
                    # Alles darunter ist Erde
                    self.tiles[x][y] = Tile(TileType.SOLID)

        # kleiner Start-Tunnel, damit man nicht direkt eingesperrt ist
        self.tiles[1][1].dig()
        self.tiles[1][2].dig()
        self.tiles[2][2].dig()

        # ----------------------------
        # 2) ECTS-Positionen je Level bestimmen
        # ----------------------------
        ects_positions = set()

        if self.level_index == 2:  # Level 3 (0-basiert: 0,1,2,3)
            # 3 ECTS nahe Ecken fix
            ects_positions = {
                (1, 1),  # startnah, ist okay (alternativ (1,2))
                (self.cols - 2, 1),
                (1, self.rows - 2),
            }
            # Startfeld ist (1,1) – wenn du NICHT willst, dass da ein Coin liegt:
            # ects_positions.discard((1, 1))
            # ects_positions.add((2, 1))

        elif self.level_index == 3:  # Level 4
            # 3 ECTS: 1 Ecke + 2 nah beieinander (Cluster)
            ects_positions = {
                (self.cols - 2, 1),  # Ecke
                (self.cols // 2, self.rows // 2),
                (self.cols // 2 + 1, self.rows // 2),
            }

        else:
            # Level 1 & 2: random SOLID Felder (nicht auf Startfeld)
            while len(ects_positions) < ects_target:
                x = random.randrange(self.cols)
                y = random.randrange(self.rows)

                if (x, y) == (1, 1):
                    continue
                if self.tiles[x][y].is_solid:
                    ects_positions.add((x, y))

        # ECTS-Objekte anlegen
        for (x, y) in ects_positions:
            # falls ein ECTS zufällig auf (1,1) landet und du willst es nicht: hier skippen
            if (x, y) == (1, 1):
                continue
            self.ects_items.append(ECTS(x, y, self.tile_size))

        # wichtig fürs Gewinnen: benötigte ECTS setzen (hier = ects_target)
        self.required_ects = ects_target

        # ----------------------------
        # 3) PowerUps (nur Pizza) platzieren
        #    -> du wolltest: Pizza auf SOLID Blöcken, nicht im Tunnel, nicht auf Coins
        # ----------------------------
        kandidaten = []
        for x in range(self.cols):
            for y in range(self.rows):
                if (x, y) == (1, 1):
                    continue
                if (x, y) in ects_positions:
                    continue
                if not self.tiles[x][y].is_solid:
                    continue
                kandidaten.append((x, y))

        random.shuffle(kandidaten)

        # damit wir nicht über das Ende der Liste laufen, falls wenig Platz ist
        pizza_target = min(pizza_target, len(kandidaten))

        # --- UPDATE: Zufällige PowerUps (Pizza, Party, ChatGPT) ---
        types = [PowerUpType.PIZZA, PowerUpType.PARTY, PowerUpType.CHATGPT]

        for (x, y) in kandidaten[:pizza_target]:
            # Wähle zufällig einen Typ aus der Liste
            ptype = random.choice(types)
            self.powerups.append(PowerUp(x, y, self.tile_size, ptype))

        # ----------------------------
        # 4) Professoren erzeugen
        # ----------------------------
        self.professors = []

        # nur so viele Profs wie wir auch wirklich in config haben
        prof_infos = PROFESSORS[:min(prof_target, len(PROFESSORS))]

        # fürs "bewachen": wir nehmen irgendein Coin-Ziel
        guard_target = None
        if ects_positions:
            guard_target = next(iter(ects_positions))

        for i, prof_info in enumerate(prof_infos):
            bild_pfad = prof_info["sprite"]
            fragen_liste = prof_info["questions"]

            sprite = Sprite(bild_pfad, self.tile_size, self.tile_size)

            # ---- Spawn-Position bestimmen ----
            spawn_x, spawn_y = None, None

            # Level 2: erster Prof startet nahe eines ECTS (bewacht es so "gefühlt")
            if self.level_index == 1 and guard_mode and guard_target is not None and i == 0:
                gx, gy = guard_target
                kandidaten_guard = [(gx + 1, gy), (gx - 1, gy), (gx, gy + 1), (gx, gy - 1)]
                random.shuffle(kandidaten_guard)

                for xx, yy in kandidaten_guard:
                    if not self.in_bounds(xx, yy):
                        continue
                    if (xx, yy) == (1, 1):
                        continue
                    # nicht auf anderem Prof
                    if any(p.grid_x == xx and p.grid_y == yy for p in self.professors):
                        continue
                    spawn_x, spawn_y = xx, yy
                    break

            # Level 3: pro ECTS ein Prof -> wir spawnen die Profs einfach nahe der ECTS
            if self.level_index == 2:
                ects_list = list(ects_positions)
                if i < len(ects_list):
                    gx, gy = ects_list[i]
                    kandidaten_guard = [(gx + 1, gy), (gx - 1, gy), (gx, gy + 1), (gx, gy - 1)]
                    random.shuffle(kandidaten_guard)

                    for xx, yy in kandidaten_guard:
                        if not self.in_bounds(xx, yy):
                            continue
                        if (xx, yy) == (1, 1):
                            continue
                        if any(p.grid_x == xx and p.grid_y == yy for p in self.professors):
                            continue
                        spawn_x, spawn_y = xx, yy
                        break

            # falls wir noch keinen Spawn haben, nehmen wir random wie vorher
            if spawn_x is None:
                while True:
                    x = random.randrange(self.cols)
                    y = random.randrange(self.rows)

                    if (x, y) == (1, 1):
                        continue

                    if any(p.grid_x == x and p.grid_y == y for p in self.professors):
                        continue

                    spawn_x, spawn_y = x, y
                    break

            # ---- Prof erstellen ----
            prof = ProfessorEnemy(spawn_x, spawn_y, self.tile_size, sprite)
            prof.questions_pool = fragen_liste  # damit eure Prof-Fragen genutzt werden

            self.professors.append(prof)

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
