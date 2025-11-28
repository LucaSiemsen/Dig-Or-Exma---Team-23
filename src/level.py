# level.py
# kümmert sich um das eigentliche Spielfeld / Level:
# - Tiles (solid/empty)
# - ECTS
# - PowerUps
# - Professoren
# - BAföG-Timer + Win/Lose

from __future__ import annotations

import random
from typing import Optional

import pygame

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
    # Fallback, falls config.py noch nicht existiert
    GRID_COLS = 12
    GRID_ROWS = 8
    GRID_MARGIN_X_TILES = 2
    GRID_MARGIN_Y_TILES = 2
    BAFOEG_TIME_SECONDS = 120
    REQUIRED_ECTS = 5
    QUESTIONS_BY_PROF = {}
    PROFESSORS = []

try:
    from src.graphics import Sprite
except ImportError:
    # einfacher Platzhalter, falls graphics.py noch nicht existiert
    class Sprite:
        def __init__(self, path: str, w: int, h: int):
            # einfaches rotes Rechteck statt richtigem Sprite
            self.surface = pygame.Surface((w, h))
            self.surface.fill((200, 80, 80))

        def draw(self, screen: pygame.Surface, x: int, y: int):
            screen.blit(self.surface, (x, y))

# ProfessorEnemy absichern
try:
    from src.enemy import ProfessorEnemy
except ImportError:
    # einfacher Platzhalter, falls enemy.py noch fehlt
    class ProfessorEnemy:
        def __init__(self, x: int, y: int, tile_size: int, sprite, questions):
            self.grid_x = x
            self.grid_y = y
            self.tile_size = tile_size
            self.sprite = sprite
            self.questions = questions or []

        def update(self, dt: float, level: "Level"):
            # hier könnte später Bewegung rein
            pass

        def draw(self, screen: pygame.Surface, offset_x: int, offset_y: int):
            px = offset_x + self.grid_x * self.tile_size
            py = offset_y + self.grid_y * self.tile_size
            self.sprite.draw(screen, px, py)

        def get_question(self):
            # Dummy-Frage, falls noch keine echten Fragen da sind
            if self.questions:
                return self.questions[0]
            class DummyQuestion:
                text = "Platzhalter-Frage (enemy.py fehlt noch)."
                answers = ["A", "B", "C"]
                correct = 0
                explanation = "Hier kommen später echte Fragen hin."
            return DummyQuestion()

    class BafoegTimer:
        def __init__(self, start_time: float):
            self.time_left = start_time
            self.is_over = False

        def update(self, dt: float):
            if self.is_over:
                return
            self.time_left -= dt
            if self.time_left <= 0:
                self.time_left = 0
                self.is_over = True

# ProfessorEnemy absichern
try:
    from src.enemy import ProfessorEnemy
except ImportError:
    # einfacher Platzhalter, falls enemy.py noch fehlt
    class ProfessorEnemy:
        def __init__(self, x: int, y: int, tile_size: int, sprite, questions):
            self.grid_x = x
            self.grid_y = y
            self.tile_size = tile_size
            self.sprite = sprite
            self.questions = questions or []

        def update(self, dt: float, level: "Level"):
            # hier könnte später Bewegung rein
            pass

        def draw(self, screen: pygame.Surface, offset_x: int, offset_y: int):
            px = offset_x + self.grid_x * self.tile_size
            py = offset_y + self.grid_y * self.tile_size
            self.sprite.draw(screen, px, py)

        def get_question(self):
            # Dummy-Frage, falls noch keine echten Fragen da sind
            if self.questions:
                return self.questions[0]
            class DummyQuestion:
                text = "Platzhalter-Frage (enemy.py fehlt noch)."
                answers = ["A", "B", "C"]
                correct = 0
                explanation = "Hier kommen später echte Fragen hin."
            return DummyQuestion()

# PowerUps optional machen (falls powerups.py noch nicht da ist)
try:
    from powerups import PowerUp, PowerUpType
    POWERUPS_AVAILABLE = True
except ImportError:
    POWERUPS_AVAILABLE = False


class TileType:
    # einfache „Enum“-Ersatzklasse
    SOLID = 0   # Erde / Buchblock
    EMPTY = 1   # Tunnel


class Tile:
    # repräsentiert ein Feld im Grid
    def __init__(self, ttype: int):
        self.type = ttype

    @property
    def is_solid(self) -> bool:
        return self.type == TileType.SOLID

    @property
    def is_empty(self) -> bool:
        return self.type == TileType.EMPTY

    def dig(self) -> None:
        # aus Erde wird Tunnel
        self.type = TileType.EMPTY


class ECTS:
    # gelbe Sammelpunkte (jeder gibt 1 ECTS)
    def __init__(self, gx: int, gy: int, tile_size: int):
        self.gx = gx
        self.gy = gy
        self.tile_size = tile_size

    def draw(self, screen: pygame.Surface, offset_x: int, offset_y: int) -> None:
        px = offset_x + self.gx * self.tile_size
        py = offset_y + self.gy * self.tile_size
        s = self.tile_size // 5
        rect = pygame.Rect(
            px + s,
            py + s,
            self.tile_size - 2 * s,
            self.tile_size - 2 * s,
        )
        pygame.draw.rect(screen, (250, 230, 80), rect)


class Level:
    def __init__(self, tile_size: int):
        self.cols = GRID_COLS
        self.rows = GRID_ROWS
        self.tile_size = tile_size

        # 2D-Liste mit Tiles (alles erstmal SOLID)
        self.tiles: list[list[Tile]] = [
            [Tile(TileType.SOLID) for _ in range(self.rows)]
            for _ in range(self.cols)
        ]

        # BAföG-Timer
        self.timer = BafoegTimer(BAFOEG_TIME_SECONDS)

        # Inhalte im Level
        self.ects_items: list[ECTS] = []
        self.powerups: list[PowerUp] = []
        self.professors: list[ProfessorEnemy] = []

        # Status vom Level
        self.collected_ects = 0
        self.required_ects = REQUIRED_ECTS
        self.is_game_over = False
        self.is_won = False
        self.game_over_reason: str = ""
        self.last_powerup_message: Optional[str] = None

        # Welt wird direkt beim Erzeugen gebaut
        self._build_world()

    @property
    def is_finished(self) -> bool:
        # True, wenn das Level vorbei ist (egal ob gewonnen oder verloren)
        return self.is_game_over or self.is_won or self.timer.is_over

    def _build_world(self) -> None:
        """
        sehr simples Level:
        - alles erst SOLID
        - kleiner Starttunnel
        - ECTS auf SOLID-Feldern
        - PowerUps nur, wenn powerups.py vorhanden ist
        - Professoren spawnen irgendwo
        """
        # alles SOLID setzen
        for x in range(self.cols):
            for y in range(self.rows):
                self.tiles[x][y].type = TileType.SOLID

        # Start-Korridor ungefähr links oben
        self.tiles[1][1].dig()
        self.tiles[1][2].dig()
        self.tiles[2][2].dig()

        # ECTS verteilen (nur auf SOLID-Feldern, nicht auf Startfeld)
        ects_positions: set[tuple[int, int]] = set()
        while len(ects_positions) < self.required_ects:
            x = random.randrange(self.cols)
            y = random.randrange(self.rows)
            if (x, y) == (1, 1):
                continue
            if self.tiles[x][y].is_solid:
                ects_positions.add((x, y))

        for (x, y) in ects_positions:
            self.ects_items.append(ECTS(x, y, self.tile_size))

        # PowerUps verteilen (nur wenn powerups.py existiert)
        if POWERUPS_AVAILABLE:
            candidates = list(ects_positions)
            random.shuffle(candidates)

            # versuchen, PowerUpType wie ein Enum zu behandeln
            try:
                type_list = list(PowerUpType)
            except TypeError:
                # falls das nicht geht (z.B. einfache Klasse), Liste manuell bauen
                type_list = []
                if hasattr(PowerUpType, "SPEED"):
                    type_list.append(PowerUpType.SPEED)
                if hasattr(PowerUpType, "TIME"):
                    type_list.append(PowerUpType.TIME)
                if hasattr(PowerUpType, "SHIELD"):
                    type_list.append(PowerUpType.SHIELD)
                if not type_list:
                    # falls gar nichts da ist, nehmen wir einfach PowerUpType selbst
                    type_list = [PowerUpType]

            # ungefähr die Hälfte der ECTS-Felder bekommt ein PowerUp
            for (x, y) in candidates[: max(1, self.required_ects // 2)]:
                ptype = random.choice(type_list)
                self.powerups.append(PowerUp(x, y, self.tile_size, ptype))

        # Professoren erzeugen
        for prof_info in PROFESSORS:
            img_path = prof_info["sprite"]
            qlist = prof_info["questions"]

            sprite = Sprite(img_path, self.tile_size, self.tile_size)

            # Prof darf überall spawnen, aber:
            # - nicht auf Startfeld
            # - nicht auf Feld, wo schon ein anderer Prof steht
            while True:
                x = random.randrange(self.cols)
                y = random.randrange(self.rows)

                if (x, y) == (1, 1):
                    continue

                if any(p.grid_x == x and p.grid_y == y for p in self.professors):
                    continue

                prof = ProfessorEnemy(x, y, self.tile_size, sprite, qlist)
                self.professors.append(prof)
                break


    def in_bounds(self, x: int, y: int) -> bool:
        # check, ob Koordinaten noch innerhalb des Grids liegen
        return 0 <= x < self.cols and 0 <= y < self.rows

    def dig(self, x: int, y: int) -> None:
        # Wrapper, damit andere Klassen nicht direkt auf tiles zugreifen müssen
        self.tiles[x][y].dig()

    def update(self, dt: float) -> None:
        # wird pro Frame vom Game aufgerufen

        if self.is_finished:
            return

        # Timer aktualisieren
        self.timer.update(dt)
        if self.timer.is_over and not self.is_won:
            self.is_game_over = True
            self.game_over_reason = "BAföG-Zeit abgelaufen."

        # Professoren bewegen (Logik steckt in ProfessorEnemy)
        for prof in self.professors:
            prof.update(dt, self)

    def on_player_enter_tile(self, gx: int, gy: int, student) -> Optional[ProfessorEnemy]:
        """
        wird von Student.move() aufgerufen, wenn der Spieler auf ein neues Feld kommt

        hier passiert:
        - ECTS einsammeln
        - PowerUps aktivieren
        - Win-Check
        - schauen, ob ein Professor auf dem Feld steht
        """
        touched_prof: Optional[ProfessorEnemy] = None

        # ECTS einsammeln
        for ects in list(self.ects_items):
            if ects.gx == gx and ects.gy == gy:
                self.ects_items.remove(ects)
                self.collected_ects += 1

        # Sieg, falls genug ECTS da sind
        if self.collected_ects >= self.required_ects and not self.is_game_over:
            self.is_won = True

        # PowerUps auslösen
        for p in list(self.powerups):
            if p.grid_x == gx and p.grid_y == gy:
                self.powerups.remove(p)
                msg = p.apply_to(self, student)
                if msg:
                    self.last_powerup_message = msg

        # checken, ob auf dem Feld ein Professor steht
        for prof in self.professors:
            if prof.grid_x == gx and prof.grid_y == gy:
                touched_prof = prof
                break

        return touched_prof

    def get_question_for_prof(self, prof: ProfessorEnemy):
        """
        wird vom Game aufgerufen, wenn der Spieler auf einem Professor-Feld steht
        die eigentliche Frage kommt aber vom Professor-Objekt selbst
        """
        return prof.get_question()

    def draw(
        self,
        screen: pygame.Surface,
        offset_x: int,
        offset_y: int,
        block_solid,
        block_empty,
    ) -> None:
        # zeichnet das komplette Level (Grid + ECTS + PowerUps + Profs)

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
