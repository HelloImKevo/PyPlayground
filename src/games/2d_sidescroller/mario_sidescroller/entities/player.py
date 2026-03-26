"""Player character with Mario-style physics."""

import pygame
from settings import (
    TILE_SIZE, GRAVITY, TERMINAL_VELOCITY,
    PLAYER_ACCEL, PLAYER_FRICTION, PLAYER_MAX_SPEED, PLAYER_RUN_MAX_SPEED,
    PLAYER_JUMP_IMPULSE, PLAYER_JUMP_CUT,
    COYOTE_TIME, JUMP_BUFFER_TIME,
    PLAYER_START_LIVES, INVINCIBILITY_DURATION,
    STAR_DURATION,
)
from engine.input_handler import Action


class Player(pygame.sprite.Sprite):
    """Controllable player character."""

    COLOR_NORMAL = (200, 50, 50)    # red
    COLOR_BIG = (200, 50, 50)
    COLOR_STAR = None  # cycles in draw

    def __init__(self, x: int, y: int):
        super().__init__()
        self.width = TILE_SIZE - 4
        self.height = TILE_SIZE - 4
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.COLOR_NORMAL)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel = pygame.math.Vector2(0, 0)

        # State
        self.on_ground = False
        self.facing_right = True
        self.is_running = False
        self.lives = PLAYER_START_LIVES
        self.score = 0
        self.coins = 0

        # Jump helpers
        self._coyote_timer = 0.0
        self._jump_buffer_timer = 0.0
        self._jumping = False  # true while holding jump mid-air

        # Power-up state
        self.is_big = False
        self.is_star = False
        self._star_timer = 0.0
        self._invincible = False
        self._invincible_timer = 0.0
        self._flash_timer = 0.0

        # Death animation
        self.dead = False
        self._death_timer = 0.0
        self._death_vel_y = 0.0

        # Victory auto-walk
        self.victory = False

    # ------------------------------------------------------------------
    # Size management
    # ------------------------------------------------------------------
    def grow(self):
        if not self.is_big:
            self.is_big = True
            old_bottom = self.rect.bottom
            self.height = TILE_SIZE * 2 - 4
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(self.COLOR_BIG)
            self.rect = self.image.get_rect(bottomleft=(self.rect.left, old_bottom))

    def shrink(self):
        if self.is_big:
            self.is_big = False
            old_bottom = self.rect.bottom
            self.height = TILE_SIZE - 4
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(self.COLOR_NORMAL)
            self.rect = self.image.get_rect(bottomleft=(self.rect.left, old_bottom))
            self._invincible = True
            self._invincible_timer = INVINCIBILITY_DURATION

    def activate_star(self):
        self.is_star = True
        self._star_timer = STAR_DURATION
        self._invincible = True
        self._invincible_timer = STAR_DURATION

    # ------------------------------------------------------------------
    # Damage
    # ------------------------------------------------------------------
    def take_damage(self):
        """Called when player is hit by an enemy (non-stomp)."""
        if self._invincible or self.is_star:
            return
        if self.is_big:
            self.shrink()
        else:
            self.die()

    def die(self):
        if self.dead:
            return
        self.dead = True
        self.lives -= 1
        self._death_timer = 0.0
        self._death_vel_y = -350  # death bounce

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def update_input(self, dt: float, input_handler):
        if self.dead or self.victory:
            return

        # Horizontal acceleration
        self.is_running = input_handler.is_pressed(Action.RUN)
        max_speed = PLAYER_RUN_MAX_SPEED if self.is_running else PLAYER_MAX_SPEED

        moving = False
        if input_handler.is_pressed(Action.LEFT):
            self.vel.x -= PLAYER_ACCEL * dt
            self.facing_right = False
            moving = True
        if input_handler.is_pressed(Action.RIGHT):
            self.vel.x += PLAYER_ACCEL * dt
            self.facing_right = True
            moving = True

        # Friction / deceleration
        if not moving:
            if self.vel.x > 0:
                self.vel.x = max(0, self.vel.x - PLAYER_FRICTION * dt)
            elif self.vel.x < 0:
                self.vel.x = min(0, self.vel.x + PLAYER_FRICTION * dt)

        # Clamp speed
        self.vel.x = max(-max_speed, min(self.vel.x, max_speed))

        # Coyote time
        if self.on_ground:
            self._coyote_timer = COYOTE_TIME
        else:
            self._coyote_timer = max(0, self._coyote_timer - dt)

        # Jump buffer
        if input_handler.is_just_pressed(Action.JUMP):
            self._jump_buffer_timer = JUMP_BUFFER_TIME

        self._jump_buffer_timer = max(0, self._jump_buffer_timer - dt)

        # Execute jump
        can_jump = self._coyote_timer > 0
        if self._jump_buffer_timer > 0 and can_jump:
            self.vel.y = PLAYER_JUMP_IMPULSE
            self._jumping = True
            self._coyote_timer = 0
            self._jump_buffer_timer = 0

        # Variable jump height: cut jump short on release
        if input_handler.is_just_released(Action.JUMP) and self._jumping and self.vel.y < PLAYER_JUMP_CUT:
            self.vel.y = PLAYER_JUMP_CUT

        if self.on_ground:
            self._jumping = False

    def update_physics(self, dt: float):
        """Apply gravity (collision resolution done externally)."""
        if self.dead:
            self._death_timer += dt
            self._death_vel_y += GRAVITY * dt
            self.rect.y += round(self._death_vel_y * dt)
            return

        if self.victory:
            # auto-walk right
            self.vel.x = PLAYER_MAX_SPEED * 0.5
            self.vel.y = min(self.vel.y + GRAVITY * dt, TERMINAL_VELOCITY)
            return

        # Gravity
        self.vel.y = min(self.vel.y + GRAVITY * dt, TERMINAL_VELOCITY)

        # Timers
        if self._invincible:
            self._invincible_timer -= dt
            self._flash_timer += dt
            if self._invincible_timer <= 0:
                self._invincible = False
                self._invincible_timer = 0
                self._flash_timer = 0

        if self.is_star:
            self._star_timer -= dt
            if self._star_timer <= 0:
                self.is_star = False
                self._invincible = False

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------
    def draw(self, surface: pygame.Surface, camera_offset: tuple[int, int]):
        if self.dead and self._death_timer > 1.5:
            return  # don't draw after death animation
        # Flashing during invincibility
        if self._invincible and not self.is_star:
            if int(self._flash_timer * 10) % 2 == 0:
                return  # skip every other frame for flash

        draw_rect = self.rect.move(-int(camera_offset[0]), -int(camera_offset[1]))

        if self.is_star:
            # Rainbow cycle
            import math
            t = pygame.time.get_ticks() / 100
            r = int((math.sin(t) * 0.5 + 0.5) * 255)
            g = int((math.sin(t + 2) * 0.5 + 0.5) * 255)
            b = int((math.sin(t + 4) * 0.5 + 0.5) * 255)
            color = (r, g, b)
        else:
            color = self.COLOR_NORMAL

        pygame.draw.rect(surface, color, draw_rect)
        # Eyes for direction
        eye_y = draw_rect.top + 6
        if self.facing_right:
            eye_x = draw_rect.right - 8
        else:
            eye_x = draw_rect.left + 4
        pygame.draw.rect(surface, (255, 255, 255), (eye_x, eye_y, 4, 4))
