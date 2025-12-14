# ------------------------------------------------------------
# level.py
# Kümmert sich um das Spielfeld / Level:
# - Tiles (Blöcke: Erde/Gras/Tunnel)
# - ECTS (Sammelpunkte / Coins)
# - PowerUps
# - Professoren (Gegner)
# ------------------------------------------------------------
# Autor: Luca Siemsen (9393491)
# GenAI-Kennzeichnung
# Tool: ChatGPT 5.2
# Verwendungszweck:Implementierung und Strukturierung der Level-Generierung mit semesterabhängiger Logik (ECTS-Platzierung, Prof-Filtering).
# Prompt: 
# - Wie implementiere ich die automatische Professoren genereirung aber ab lvl 3 soll ein manueller Professor erzeugt werden?
#- Wie kann ich einem Professor sagen, dass er einen ECTS "bewachen soll"?
# ------------------------------------------------------------
import os
import random
import pygame

from src.graphics import Sprite
from src.enemy import ProfessorEnemy
from src.powerups import PowerUp, PowerUpType
from src.tile import Tile, TileType
from .timer import BafoegTimer

# ------------------------------------------------------------
# Config / Fallbacks:
# Wenn config oder timer fehlen, laufen wir mit Standardwerten,
# damit das Spiel nicht direkt crasht.
# ------------------------------------------------------------


from src.config import (
    # ALLE KONSTANTEN, die Level braucht
    GRID_COLS,
    GRID_ROWS,
    BAFOEG_TIME_SECONDS,  
    REQUIRED_ECTS,
    LEVELS,
    PROFESSORS
    )



# ============================================================
# ECTS (Coin)
# ============================================================
class ECTS:
    """Ein ECTS/Coin, der auf einem Grid-Feld liegt und animiert ist."""

    def __init__(self, grid_x: int, grid_y: int, tile_size: int):
        self.gx = grid_x
        self.gy = grid_y
        self.tile_size = tile_size

        # Coin Animation Frames (aus Sprite Sheet)
        self.frames: list[pygame.Surface] = []
        self._load_coin_frames()

    def _load_coin_frames(self):
        """
        Lädt die Coin-Frames:
        - Standard: Coin v3 (mehrere Frames untereinander)
        - Fallback: Coin v1 (ein Bild)
        """
        path = os.path.join("assets", "sprites", "Coin v3 (kann man animiert darstellen).png")

        try:
            sheet = pygame.image.load(path).convert_alpha()
        except:
            # Wenn Sheet nicht existiert -> fallback auf Coin v1
            fallback = os.path.join("assets", "sprites", "Coin v1.png")
            img = pygame.image.load(fallback).convert_alpha()
            img = pygame.transform.scale(img, (self.tile_size, self.tile_size))
            self.frames = [img]
            return

        # Frames sind quadratisch (Breite = Höhe pro Frame)
        frame_w = sheet.get_width()
        frame_h = frame_w
        count = sheet.get_height() // frame_h

        for i in range(count):
            rect = pygame.Rect(0, i * frame_h, frame_w, frame_h)
            frame = sheet.subsurface(rect).copy()
            frame = pygame.transform.scale(frame, (self.tile_size, self.tile_size))
            self.frames.append(frame)

        # Falls irgendwas komisch ist und keine Frames geladen wurden:
        if not self.frames:
            self.frames = [pygame.Surface((self.tile_size, self.tile_size))]

    def draw(self, screen: pygame.Surface, offset_x: int, offset_y: int):
        """Zeichnet den Coin an seine Pixelposition (Offset + Grid * TileSize)."""
        px = offset_x + self.gx * self.tile_size
        py = offset_y + self.gy * self.tile_size

        # Animation: alle 100ms nächstes Frame
        idx = (pygame.time.get_ticks() // 100) % len(self.frames)
        screen.blit(self.frames[idx], (px, py))


# ============================================================
# Level
# ============================================================
class Level:
    """
    Enthält das komplette Spielfeld und alles, was darauf liegt
    (Tiles, Coins, PowerUps, Professoren + Timer).
    """

    def __init__(self, tile_size: int, level_index: int = 0):
        self.level_index = level_index

        # Grid-Größe und Tile-Größe
        self.cols = GRID_COLS
        self.rows = GRID_ROWS
        self.tile_size = tile_size

        # Tiles als 2D-Liste [x][y]
        # Erst mal alles SOLID (Erde), wird dann in _build_world() umgebaut.
        self.tiles: list[list[Tile]] = []
        for x in range(self.cols):
            spalte = []
            for y in range(self.rows):
                spalte.append(Tile(TileType.SOLID))
            self.tiles.append(spalte)

        # Timer (BAföG)
        self.timer = BafoegTimer(BAFOEG_TIME_SECONDS)

        # Inhalte im Level
        self.ects_items: list[ECTS] = []
        self.powerups: list[PowerUp] = []
        self.professors: list[ProfessorEnemy] = []

        # Level-Status
        self.collected_ects = 0
        self.required_ects = REQUIRED_ECTS
        self.is_game_over = False
        self.is_won = False
        self.game_over_reason = ""
        self.last_powerup_message = None

        # Level direkt aufbauen
        self._build_world()

    @property
    def is_finished(self) -> bool:
        """Level ist vorbei, wenn gewonnen, verloren oder Zeit abgelaufen."""
        return self.is_game_over or self.is_won or self.timer.is_over

    # ------------------------------------------------------------
    # Welt/Level-Aufbau
    # ------------------------------------------------------------
    def _build_world(self):
        """
        Baut das Level abhängig von level_index.

        Idee (simpel gehalten):
        - Semester 1/2: ECTS random + Professoren random
        - Semester 2 optional guard_mode: 1 Prof startet bei einem ECTS
        - Semester 3: ECTS an festen Punkten, Profs spawnen nahe der ECTS
        - Semester 4: ECTS Cluster / mehr “Chaos”
        """

        # ----------------------------
        # 0) Level-Config holen + absichern
        # ----------------------------
        if not LEVELS:
            # Falls config leer ist -> minimaler Default
            cfg = {"ects": REQUIRED_ECTS, "pizzas": 1, "prof_count": len(PROFESSORS), "guard_mode": False}
        else:
            # level_index absichern, damit nix out-of-range ist
            idx = max(0, min(self.level_index, len(LEVELS) - 1))
            cfg = LEVELS[idx]

        # Werte aus Config ziehen (mit Defaults)
        ects_target = int(cfg.get("ects", REQUIRED_ECTS))
        pizza_target = int(cfg.get("pizzas", 1))          # aktuell nicht genutzt, bleibt aber drin
        prof_target = int(cfg.get("prof_count", len(PROFESSORS)))
        guard_mode = bool(cfg.get("guard_mode", False))

        # ----------------------------
        # 1) Tiles resetten: oben Gras, darunter Erde
        # ----------------------------
        for x in range(self.cols):
            for y in range(self.rows):
                if y == 0:
                    self.tiles[x][y] = Tile(TileType.GRASS)
                else:
                    self.tiles[x][y] = Tile(TileType.SOLID)

        # kleiner Start-Tunnel (damit Start nicht “eingemauert” ist)
        self.tiles[1][1].dig()
        self.tiles[1][2].dig()
        self.tiles[2][2].dig()

        # ----------------------------
        # 2) ECTS-Positionen festlegen
        # ----------------------------
        ects_positions: set[tuple[int, int]] = set()

        if self.level_index == 2:
            # Semester 3: 3 ECTS nahe Ecken
            ects_positions = {
                (1, 1),
                (self.cols - 2, 1),
                (1, self.rows - 2),
            }

        elif self.level_index == 3:
            # Semester 4: 1 Ecke + 2 als Cluster
            ects_positions = {
                (self.cols - 2, 1),
                (self.cols // 2, self.rows // 2),
                (self.cols // 2 + 1, self.rows // 2),
            }

        else:
            # Semester 1 & 2: random SOLID-Felder (nicht Startfeld)
            while len(ects_positions) < ects_target:
                x = random.randrange(self.cols)
                y = random.randrange(self.rows)

                if (x, y) == (1, 1):
                    continue

                # ECTS nur auf Erde (solid) legen
                if self.tiles[x][y].is_solid:
                    ects_positions.add((x, y))

        # ECTS-Objekte erzeugen
        for (x, y) in ects_positions:
            # Bei dir wird (1,1) bewusst übersprungen (Startfeld)
            if (x, y) == (1, 1):
                continue
            self.ects_items.append(ECTS(x, y, self.tile_size))

        # wichtig fürs Gewinnen
        self.required_ects = ects_target

        # ----------------------------
        # 3) PowerUps platzieren
        # ----------------------------
        # Kandidaten-Felder für PowerUps:
        # - nicht Startfeld
        # - nicht auf ECTS
        # - nur auf SOLID (also Erde)
        kandidaten: list[tuple[int, int]] = []
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

        # Anzahl PowerUps pro Level (Default: mindestens 1)
        powerups_total = int(cfg.get("powerups_total", max(1, self.required_ects // 2)))

        type_list = list(PowerUpType)  # z.B. PIZZA, PARTY, CHATGPT
        for (x, y) in kandidaten[:powerups_total]:
            ptype = random.choice(type_list)
            self.powerups.append(PowerUp(x, y, self.tile_size, ptype))

        # ----------------------------
        # 4) Professoren erzeugen
        # ----------------------------
        self.professors = []

        # Wir filtern zuerst Prof-Infos aus der Config:
        # - “harte” Profs (hp >= 3) erst ab Semester 3 (level_index >= 2)
        prof_infos: list[dict] = []
        for prof_info in PROFESSORS:
            prof_hp = int(prof_info.get("hp", 1))
            if prof_hp >= 3 and self.level_index < 2:
                continue
            prof_infos.append(prof_info)

        # Klausur-Prof ab Semester 3 erzwingen (falls vorhanden)
        if self.level_index >= 2:
            klausur = next((p for p in prof_infos if p.get("type") == "klausur"), None)
            if klausur is not None:
                # nach vorne schieben, damit er nicht durch slicing verloren geht
                prof_infos.remove(klausur)
                prof_infos.insert(0, klausur)

        # Anzahl Professoren auf prof_target begrenzen
        prof_infos = prof_infos[:min(prof_target, len(prof_infos))]

        # guard_target: irgendein ECTS (nur fürs “bewachen” im Semester 2)
        guard_target = next(iter(ects_positions)) if ects_positions else None

        for i, prof_info in enumerate(prof_infos):
            bild_pfad = prof_info["sprite"]
            fragen_liste = prof_info["questions"]

            sprite = Sprite(bild_pfad, self.tile_size, self.tile_size)

            # Spawn-Position suchen
            spawn_x, spawn_y = None, None

            # Semester 2 (level_index == 1): erster Prof soll nahe bei einem ECTS starten
            if self.level_index == 1 and guard_mode and guard_target is not None and i == 0:
                gx, gy = guard_target
                kandidaten_guard = [(gx + 1, gy), (gx - 1, gy), (gx, gy + 1), (gx, gy - 1)]
                random.shuffle(kandidaten_guard)

                for xx, yy in kandidaten_guard:
                    if not self.in_bounds(xx, yy):
                        continue
                    if (xx, yy) == (1, 1):
                        continue
                    # kein anderer Prof darf dort stehen
                    if any(p.grid_x == xx and p.grid_y == yy for p in self.professors):
                        continue
                    spawn_x, spawn_y = xx, yy
                    break

            # Semester 3 (level_index == 2): Profs spawnen nahe an ECTS (pro ECTS ein Prof)
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

            # Falls wir noch keinen Spawn gefunden haben -> random freies Feld
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

            # Prof erzeugen
            prof = ProfessorEnemy(spawn_x, spawn_y, self.tile_size, sprite)

            # Fragen-Liste an Prof geben (wichtig für Quiz)
            prof.questions_pool = fragen_liste

            # Wenn hp in config steht, übernehmen (z.B. Klausur hp=3)
            if "hp" in prof_info:
                prof.hp = int(prof_info["hp"])
                prof.max_hp = int(prof_info["hp"])

            self.professors.append(prof)

    # ------------------------------------------------------------
    # Hilfsfunktionen
    # ------------------------------------------------------------
    def in_bounds(self, x: int, y: int) -> bool:
        """True, wenn (x,y) im Grid liegt."""
        return 0 <= x < self.cols and 0 <= y < self.rows

    def dig(self, x: int, y: int):
        """Damit andere Klassen nicht direkt self.tiles[x][y] anfassen müssen."""
        self.tiles[x][y].dig()

    # ------------------------------------------------------------
    # Update
    # ------------------------------------------------------------
    def update(self, dt: float):
        """Wird pro Frame vom Game aufgerufen."""
        if self.is_finished:
            return

        # Timer runterzählen
        self.timer.update(dt)
        if self.timer.is_over and not self.is_won:
            self.is_game_over = True
            self.game_over_reason = "BAföG-Zeit abgelaufen."

        # Professoren updaten (Movement / KI kommt in enemy.py)
        for prof in self.professors:
            prof.update(dt, self)

    # ------------------------------------------------------------
    # Interaktion: Spieler betritt ein Feld
    # ------------------------------------------------------------
    def on_player_enter_tile(self, gx: int, gy: int, student):
        """
        Wird aufgerufen, wenn der Spieler ein Feld betritt.
        - ECTS einsammeln
        - PowerUp auslösen
        - Sieg prüfen
        - checken ob Prof auf dem Feld steht
        """
        beruehrter_prof = None

        # ECTS einsammeln
        for ects in list(self.ects_items):
            if ects.gx == gx and ects.gy == gy:
                self.ects_items.remove(ects)
                self.collected_ects += 1

        # Sieg prüfen
        if self.collected_ects >= self.required_ects and not self.is_game_over:
            self.is_won = True

        # PowerUps einsammeln
        for p in list(self.powerups):
            if p.grid_x == gx and p.grid_y == gy:
                self.powerups.remove(p)
                nachricht = p.apply_to(self, student)
                if nachricht:
                    self.last_powerup_message = nachricht

        # Prof-Kollision prüfen
        for prof in self.professors:
            if prof.grid_x == gx and prof.grid_y == gy:
                beruehrter_prof = prof
                break

        return beruehrter_prof

    # ------------------------------------------------------------
    # Quiz / Professoren-Handling
    # ------------------------------------------------------------
    def get_question_for_prof(self, prof):
        """Gibt eine Frage für den Prof zurück (Logik steckt im Prof)."""
        return prof.get_question()

    def remove_professor(self, prof):
        """Entfernt einen Prof aus dem Level (wenn besiegt)."""
        if prof in self.professors:
            self.professors.remove(prof)

    # ------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------
    def draw(self, screen: pygame.Surface, offset_x: int, offset_y: int, block_solid, block_empty):
        """Zeichnet Tiles + Items + Gegner."""
        # Tiles
        for x in range(self.cols):
            for y in range(self.rows):
                tile = self.tiles[x][y]
                px = offset_x + x * self.tile_size
                py = offset_y + y * self.tile_size

                if tile.is_solid:
                    block_solid.draw(screen, px, py)
                else:
                    block_empty.draw(screen, px, py)

        # ECTS
        for ects in self.ects_items:
            ects.draw(screen, offset_x, offset_y)

        # PowerUps
        for p in self.powerups:
            p.draw(screen, offset_x, offset_y)

        # Professoren
        for prof in self.professors:
            prof.draw(screen, offset_x, offset_y)
