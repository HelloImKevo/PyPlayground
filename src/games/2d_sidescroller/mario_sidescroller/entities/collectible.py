"""Collectible entities: Coin, Mushroom, Star."""

import pygame
from settings import TILE_SIZE, GRAVITY, TERMINAL_VELOCITY


class Coin(pygame.sprite.Sprite):
    """Static coin collectible."""

    def __init__(self, x: int, y: int):
        super().__init__()
        self.width = 16
        self.height = 16
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (8, 8), 8)
        pygame.draw.circle(self.image, (255, 255, 100), (8, 8), 5)
        self.rect = self.image.get_rect(center=(x, y))
        self.collected = False
        self._bob_timer = 0.0

    def update(self, dt: float):
        self._bob_timer += dt

    def draw(self, surface: pygame.Surface, camera_offset: tuple[int, int]):
        if self.collected:
            return
        import math
        bob = math.sin(self._bob_timer * 3) * 2
        draw_rect = self.rect.move(-int(camera_offset[0]),
                                    -int(camera_offset[1]) + int(bob))
        pygame.draw.circle(surface, (255, 215, 0),
                           draw_rect.center, 8)
        pygame.draw.circle(surface, (255, 255, 100),
                           draw_rect.center, 5)


class Mushroom(pygame.sprite.Sprite):
    """Power-up mushroom that moves horizontally after spawning."""

    def __init__(self, x: int, y: int):
        super().__init__()
        self.width = TILE_SIZE - 8
        self.height = TILE_SIZE - 8
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((220, 40, 40))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.vel = pygame.math.Vector2(80, 0)
        self.on_ground = False
        self.collected = False
        # Emergence animation
        self._emerging = True
        self._emerge_start_y = self.rect.y
        self._emerge_target_y = self.rect.y - TILE_SIZE
        self._emerge_progress = 0.0

    def update(self, dt: float, tilemap=None):
        if self.collected:
            return

        if self._emerging:
            self._emerge_progress += dt * 2
            self.rect.y = int(self._emerge_start_y + (self._emerge_target_y - self._emerge_start_y) * min(1, self._emerge_progress))
            if self._emerge_progress >= 1.0:
                self._emerging = False
            return

        if tilemap is None:
            return
        # Gravity
        self.vel.y = min(self.vel.y + GRAVITY * dt, TERMINAL_VELOCITY)

        # Horizontal
        self.rect.x += round(self.vel.x * dt)
        for tile_rect in tilemap.get_colliders_near(self.rect):
            if self.rect.colliderect(tile_rect):
                if self.vel.x > 0:
                    self.rect.right = tile_rect.left
                elif self.vel.x < 0:
                    self.rect.left = tile_rect.right
                self.vel.x = -self.vel.x

        # Vertical
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

    def draw(self, surface: pygame.Surface, camera_offset: tuple[int, int]):
        if self.collected:
            return
        draw_rect = self.rect.move(-int(camera_offset[0]), -int(camera_offset[1]))
        pygame.draw.rect(surface, (220, 40, 40), draw_rect)
        # White spots
        pygame.draw.circle(surface, (255, 255, 255),
                           (draw_rect.centerx - 4, draw_rect.top + 6), 3)
        pygame.draw.circle(surface, (255, 255, 255),
                           (draw_rect.centerx + 4, draw_rect.top + 6), 3)


class Star(pygame.sprite.Sprite):
    """Bouncing invincibility star."""

    def __init__(self, x: int, y: int):
        super().__init__()
        self.width = TILE_SIZE - 8
        self.height = TILE_SIZE - 8
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.vel = pygame.math.Vector2(100, -250)
        self.on_ground = False
        self.collected = False
        self._emerging = True
        self._emerge_start_y = self.rect.y
        self._emerge_target_y = self.rect.y - TILE_SIZE
        self._emerge_progress = 0.0

    def update(self, dt: float, tilemap=None):
        if self.collected:
            return
        if self._emerging:
            self._emerge_progress += dt * 2
            self.rect.y = int(self._emerge_start_y + (self._emerge_target_y - self._emerge_start_y) * min(1, self._emerge_progress))
            if self._emerge_progress >= 1.0:
                self._emerging = False
            return

        if tilemap is None:
            return
        # Gravity
        self.vel.y = min(self.vel.y + GRAVITY * dt, TERMINAL_VELOCITY)

        # Horizontal
        self.rect.x += round(self.vel.x * dt)
        for tile_rect in tilemap.get_colliders_near(self.rect):
            if self.rect.colliderect(tile_rect):
                if self.vel.x > 0:
                    self.rect.right = tile_rect.left
                elif self.vel.x < 0:
                    self.rect.left = tile_rect.right
                self.vel.x = -self.vel.x

        # Vertical — bounce on ground
        self.on_ground = False
        self.rect.y += round(self.vel.y * dt)
        for tile_rect in tilemap.get_colliders_near(self.rect):
            if self.rect.colliderect(tile_rect):
                if self.vel.y > 0:
                    self.rect.bottom = tile_rect.top
                    self.on_ground = True
                    self.vel.y = -300  # bounce
                elif self.vel.y < 0:
                    self.rect.top = tile_rect.bottom
                    self.vel.y = 0

    def draw(self, surface: pygame.Surface, camera_offset: tuple[int, int]):
        if self.collected:
            return
        draw_rect = self.rect.move(-int(camera_offset[0]), -int(camera_offset[1]))
        # Animated color
        import math
        t = pygame.time.get_ticks() / 150
        r = int((math.sin(t) * 0.5 + 0.5) * 255)
        g = int((math.sin(t + 2) * 0.5 + 0.5) * 255)
        b = int((math.sin(t + 4) * 0.5 + 0.5) * 255)
        # Draw star shape as a filled polygon
        cx, cy = draw_rect.center
        s = self.width // 2
        points = []
        for i in range(5):
            import math as m
            angle_outer = m.radians(-90 + i * 72)
            angle_inner = m.radians(-90 + i * 72 + 36)
            points.append((cx + int(s * m.cos(angle_outer)),
                           cy + int(s * m.sin(angle_outer))))
            points.append((cx + int(s * 0.4 * m.cos(angle_inner)),
                           cy + int(s * 0.4 * m.sin(angle_inner))))
        pygame.draw.polygon(surface, (r, g, b), points)
