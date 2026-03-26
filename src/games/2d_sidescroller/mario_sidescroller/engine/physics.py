"""Physics helpers: gravity and tilemap collision resolution."""

import pygame
from settings import GRAVITY, TERMINAL_VELOCITY


def apply_gravity(entity, dt: float):
    """Apply gravity to an entity that has *vel* (Vector2)."""
    entity.vel.y = min(entity.vel.y + GRAVITY * dt, TERMINAL_VELOCITY)


def resolve_tilemap_collisions(entity, tilemap, dt: float):
    """Move entity and resolve collisions against the tilemap.

    Entity must expose: rect, vel (Vector2), on_ground (bool).
    Tilemap must expose: get_colliders_near(rect) -> list[pygame.Rect].
    Resolves X then Y independently to prevent corner-clipping.
    """
    # --- Horizontal ---
    entity.rect.x += round(entity.vel.x * dt)
    for tile_rect in tilemap.get_colliders_near(entity.rect):
        if entity.rect.colliderect(tile_rect):
            if entity.vel.x > 0:
                entity.rect.right = tile_rect.left
            elif entity.vel.x < 0:
                entity.rect.left = tile_rect.right
            entity.vel.x = 0

    # --- Vertical ---
    entity.on_ground = False
    entity.rect.y += round(entity.vel.y * dt)
    for tile_rect in tilemap.get_colliders_near(entity.rect):
        if entity.rect.colliderect(tile_rect):
            if entity.vel.y > 0:
                entity.rect.bottom = tile_rect.top
                entity.on_ground = True
            elif entity.vel.y < 0:
                entity.rect.top = tile_rect.bottom
            entity.vel.y = 0
