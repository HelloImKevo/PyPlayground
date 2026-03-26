"""Enemy entities: Goomba and Koopa types."""

import pygame
from settings import TILE_SIZE, GRAVITY, TERMINAL_VELOCITY, ENEMY_SPEED


class Enemy(pygame.sprite.Sprite):
    """Base enemy with patrol AI."""

    COLOR = (139, 69, 19)  # brown

    def __init__(self, x: int, y: int, enemy_type: str = "goomba"):
        super().__init__()
        self.enemy_type = enemy_type
        self.width = TILE_SIZE - 4
        self.height = TILE_SIZE - 4
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel = pygame.math.Vector2(-ENEMY_SPEED, 0)
        self.on_ground = False
        self.alive = True
        self.is_shell = False
        self._shell_speed = 300
        self._set_color()

    def _set_color(self):
        if self.enemy_type == "koopa":
            self.image.fill((34, 139, 34))  # green
        else:
            self.image.fill((139, 69, 19))  # brown

    def stomp(self):
        """Called when the player stomps this enemy."""
        if self.enemy_type == "koopa" and not self.is_shell:
            self.is_shell = True
            self.vel.x = 0
            self.height = TILE_SIZE // 2
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((34, 100, 34))
            old_bottom = self.rect.bottom
            self.rect = self.image.get_rect(bottomleft=(self.rect.left, old_bottom))
        else:
            self.alive = False

    def kick_shell(self, direction: int):
        """Kick a koopa shell. direction: 1 = right, -1 = left."""
        if self.is_shell:
            self.vel.x = self._shell_speed * direction

    def update(self, dt: float, tilemap):
        if not self.alive:
            return

        # Gravity
        self.vel.y = min(self.vel.y + GRAVITY * dt, TERMINAL_VELOCITY)

        # Horizontal movement
        self.rect.x += round(self.vel.x * dt)
        for tile_rect in tilemap.get_colliders_near(self.rect):
            if self.rect.colliderect(tile_rect):
                if self.vel.x > 0:
                    self.rect.right = tile_rect.left
                elif self.vel.x < 0:
                    self.rect.left = tile_rect.right
                self.vel.x = -self.vel.x  # reverse direction

        # Vertical movement
        self.on_ground = False
        self.rect.y += round(self.vel.y * dt)
        for tile_rect in tilemap.get_colliders_near(self.rect):
            if self.rect.colliderect(tile_rect):
                if self.vel.y > 0:
                    self.rect.bottom = tile_rect.top
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = tile_rect.bottom
                self.vel.y = 0

        # Ledge detection (don't walk off edges) — only for patrol, not shells
        if self.on_ground and not self.is_shell and self.vel.x != 0:
            check_x = self.rect.right + 2 if self.vel.x > 0 else self.rect.left - 2
            check_y = self.rect.bottom + 4
            found_floor = False
            for tile_rect in tilemap.get_colliders_near(pygame.Rect(check_x - 2, check_y, 4, 4)):
                if tile_rect.collidepoint(check_x, check_y):
                    found_floor = True
                    break
            if not found_floor:
                self.vel.x = -self.vel.x

    def draw(self, surface: pygame.Surface, camera_offset: tuple[int, int]):
        if not self.alive:
            return
        draw_rect = self.rect.move(-int(camera_offset[0]), -int(camera_offset[1]))
        color = (34, 100, 34) if self.is_shell else ((34, 139, 34) if self.enemy_type == "koopa" else (139, 69, 19))
        pygame.draw.rect(surface, color, draw_rect)
        pygame.draw.rect(surface, (0, 0, 0), draw_rect, 1)
        if not self.is_shell:
            # Eyes
            ey = draw_rect.top + 5
            pygame.draw.rect(surface, (255, 255, 255),
                             (draw_rect.centerx - 5, ey, 3, 3))
            pygame.draw.rect(surface, (255, 255, 255),
                             (draw_rect.centerx + 2, ey, 3, 3))
