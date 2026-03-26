"""Lightweight particle effects system."""

import random
import pygame
from settings import GRAVITY


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "color", "lifetime", "max_lifetime",
                 "size", "gravity")

    def __init__(self, x, y, vx, vy, color, lifetime, size, gravity=True):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.gravity = gravity


class ParticleEmitter:
    """Manages a pool of particles with burst spawning."""

    MAX_PARTICLES = 200

    def __init__(self):
        self.particles: list[Particle] = []

    def emit(self, pos: tuple, count: int, color: tuple,
             spread: float = 100, speed: float = 150,
             lifetime: float = 0.6, size: float = 3, gravity: bool = True):
        """Burst-spawn *count* particles at *pos*."""
        for _ in range(count):
            if len(self.particles) >= self.MAX_PARTICLES:
                break
            angle = random.uniform(0, 6.283)
            spd = random.uniform(speed * 0.3, speed)
            import math
            vx = math.cos(angle) * spd * (spread / 100)
            vy = math.sin(angle) * spd - speed * 0.5
            lt = random.uniform(lifetime * 0.5, lifetime)
            sz = random.uniform(size * 0.5, size)
            # Slight color variation
            r = max(0, min(255, color[0] + random.randint(-20, 20)))
            g = max(0, min(255, color[1] + random.randint(-20, 20)))
            b = max(0, min(255, color[2] + random.randint(-20, 20)))
            self.particles.append(
                Particle(pos[0], pos[1], vx, vy, (r, g, b), lt, sz, gravity))

    def update(self, dt: float):
        alive = []
        for p in self.particles:
            p.lifetime -= dt
            if p.lifetime <= 0:
                continue
            p.x += p.vx * dt
            p.y += p.vy * dt
            if p.gravity:
                p.vy += GRAVITY * 0.5 * dt
            # Shrink over lifetime
            ratio = p.lifetime / p.max_lifetime
            p.size = max(0.5, p.size * (0.95 + 0.05 * ratio))
            alive.append(p)
        self.particles = alive

    def draw(self, surface: pygame.Surface, camera_offset: tuple[int, int]):
        ox, oy = int(camera_offset[0]), int(camera_offset[1])
        for p in self.particles:
            sx = int(p.x) - ox
            sy = int(p.y) - oy
            sz = max(1, int(p.size))
            pygame.draw.rect(surface, p.color, (sx, sy, sz, sz))
