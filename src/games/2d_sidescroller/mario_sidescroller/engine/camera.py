"""Side-scrolling camera that tracks the player."""

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    """Horizontal-follow camera with look-ahead and level clamping."""

    def __init__(self, level_width: int, level_height: int):
        self.offset = pygame.math.Vector2(0, 0)
        self.level_width = level_width
        self.level_height = level_height
        self.look_ahead = 60  # pixels ahead of player

    def update(self, target_rect: pygame.Rect, dt: float):
        """Smoothly follow *target_rect* (the player)."""
        # Desired x: center player horizontally with look-ahead
        goal_x = target_rect.centerx - SCREEN_WIDTH // 2 + self.look_ahead
        goal_y = target_rect.centery - SCREEN_HEIGHT // 2

        # Smooth lerp
        self.offset.x += (goal_x - self.offset.x) * min(1, 5 * dt)
        self.offset.y += (goal_y - self.offset.y) * min(1, 5 * dt)

        # Clamp to level boundaries
        self.offset.x = max(0, min(self.offset.x, self.level_width - SCREEN_WIDTH))
        self.offset.y = max(0, min(self.offset.y, self.level_height - SCREEN_HEIGHT))

    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        """Return *rect* shifted by camera offset (for drawing)."""
        return rect.move(-int(self.offset.x), -int(self.offset.y))

    def apply_pos(self, pos):
        """Return a position tuple shifted by camera offset."""
        return (pos[0] - int(self.offset.x), pos[1] - int(self.offset.y))
