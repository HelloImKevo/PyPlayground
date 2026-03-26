"""Tilemap rendering and collision lookups."""

import pygame
from settings import TILE_SIZE

# Tile type → color mapping for placeholder rendering
TILE_COLORS = {
    1: (139, 90, 43),    # ground — brown
    2: (180, 100, 50),   # brick — orange-brown
    3: (255, 215, 0),    # question block — gold
    4: (34, 139, 34),    # pipe — green
    5: (200, 30, 30),    # hazard — red
    6: (100, 100, 100),  # used question block — grey
    7: (34, 139, 34),    # pipe top — green
    8: (255, 165, 0),    # flagpole — orange
    9: (120, 60, 30),    # flag base — dark brown
}

SOLID_TILES = {1, 2, 3, 4, 6, 7, 9}


class Tilemap:
    """Grid-based tilemap with rendering and collision queries."""

    def __init__(self, grid: list[list[int]], tile_size: int = TILE_SIZE):
        self.grid = grid
        self.tile_size = tile_size
        self.rows = len(grid)
        self.cols = max(len(row) for row in grid) if grid else 0
        self.width = self.cols * tile_size
        self.height = self.rows * tile_size

    def get_tile(self, col: int, row: int) -> int:
        if 0 <= row < self.rows and 0 <= col < len(self.grid[row]):
            return self.grid[row][col]
        return 0

    def set_tile(self, col: int, row: int, value: int):
        if 0 <= row < self.rows and 0 <= col < len(self.grid[row]):
            self.grid[row][col] = value

    def get_colliders_near(self, rect: pygame.Rect) -> list[pygame.Rect]:
        """Return rects of solid tiles overlapping the query area."""
        ts = self.tile_size
        col_start = max(0, rect.left // ts - 1)
        col_end = min(self.cols, rect.right // ts + 2)
        row_start = max(0, rect.top // ts - 1)
        row_end = min(self.rows, rect.bottom // ts + 2)

        colliders = []
        for r in range(row_start, row_end):
            for c in range(col_start, col_end):
                tid = self.get_tile(c, r)
                if tid in SOLID_TILES:
                    colliders.append(pygame.Rect(c * ts, r * ts, ts, ts))
        return colliders

    def draw(self, surface: pygame.Surface, camera_offset: tuple[int, int]):
        """Draw only the tiles visible on screen."""
        ts = self.tile_size
        ox, oy = int(camera_offset[0]), int(camera_offset[1])
        sw, sh = surface.get_size()

        col_start = max(0, ox // ts)
        col_end = min(self.cols, (ox + sw) // ts + 1)
        row_start = max(0, oy // ts)
        row_end = min(self.rows, (oy + sh) // ts + 1)

        for r in range(row_start, row_end):
            for c in range(col_start, col_end):
                tid = self.get_tile(c, r)
                if tid == 0:
                    continue
                color = TILE_COLORS.get(tid, (255, 0, 255))
                screen_x = c * ts - ox
                screen_y = r * ts - oy
                pygame.draw.rect(surface, color, (screen_x, screen_y, ts, ts))
                # Outline for visual distinction
                pygame.draw.rect(surface, (0, 0, 0), (screen_x, screen_y, ts, ts), 1)
                # Special markers
                if tid == 3:  # question block
                    font = pygame.font.SysFont("arial", 18, bold=True)
                    q = font.render("?", True, (255, 255, 255))
                    surface.blit(q, q.get_rect(center=(screen_x + ts // 2, screen_y + ts // 2)))
