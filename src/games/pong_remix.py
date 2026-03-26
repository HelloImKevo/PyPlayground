#!/usr/bin/env python3
"""
Pong Remix — A twisted take on the classic Pong.

Twists over vanilla Pong:
  • Power-ups spawn on the field (Big Paddle, Shrink Enemy, Fireball,
    Multi-Ball, Curve Ball).
  • Hitting the ball while your paddle is moving applies *spin*, curving
    the ball's vertical trajectory.
  • Rally speed — each consecutive hit in a rally increases ball speed.
  • Particle trail behind every ball, colour-shifting with speed.
  • Screen-shake on goals.
  • AI opponent with adaptive difficulty (or local 2-player mode).
  • First to 7 wins.

Controls:
  Player 1 (left):  W / S  to move,  or  Mouse Y-axis
  Player 2 (right):  Up / Down arrows   (hold TAB at title screen for
                     2-player mode; otherwise AI controls the right paddle)

Run:
  python -m src.games.pong_remix          (from repo root)
  python src/games/pong_remix.py          (directly)
"""

import math
import os
import random
import sys

import pygame

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCREEN_W, SCREEN_H = 960, 640
FPS = 60
WIN_SCORE = 7

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
DARK_GREY = (30, 30, 30)
NEON_BLUE = (0, 200, 255)
NEON_PINK = (255, 50, 150)
NEON_GREEN = (50, 255, 100)
NEON_ORANGE = (255, 160, 30)
NEON_YELLOW = (255, 255, 50)
NEON_PURPLE = (180, 60, 255)

# Paddle
PADDLE_W = 14
PADDLE_H = 100
PADDLE_SPEED = 7
PADDLE_MARGIN = 30

# Ball
BALL_RADIUS = 10
BALL_BASE_SPEED = 5.5
BALL_MAX_SPEED = 14.0
BALL_RALLY_ACCEL = 0.35

# Power-ups
POWERUP_SIZE = 24
POWERUP_DURATION = 6.0  # seconds
POWERUP_SPAWN_INTERVAL = (5.0, 10.0)  # seconds range

# Particles
PARTICLE_LIFETIME = 0.4  # seconds
MAX_PARTICLES = 300


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------
def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def lerp_colour(c1, c2, t):
    t = clamp(t, 0.0, 1.0)
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def random_sign():
    return random.choice((-1, 1))


# ---------------------------------------------------------------------------
# Particle
# ---------------------------------------------------------------------------
class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "colour", "radius")

    def __init__(self, x, y, vx, vy, life, colour, radius=3):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.colour = colour
        self.radius = radius

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt

    @property
    def alive(self):
        return self.life > 0

    def draw(self, surface):
        alpha = clamp(self.life / self.max_life, 0.0, 1.0)
        r = max(1, int(self.radius * alpha))
        c = tuple(int(ch * alpha) for ch in self.colour)
        pygame.draw.circle(surface, c, (int(self.x), int(self.y)), r)


# ---------------------------------------------------------------------------
# Power-up types
# ---------------------------------------------------------------------------
class PowerUpKind:
    BIG_PADDLE = "big_paddle"
    SHRINK_ENEMY = "shrink_enemy"
    FIREBALL = "fireball"
    MULTI_BALL = "multi_ball"
    CURVE_BALL = "curve_ball"


POWERUP_COLOURS = {
    PowerUpKind.BIG_PADDLE: NEON_GREEN,
    PowerUpKind.SHRINK_ENEMY: NEON_PURPLE,
    PowerUpKind.FIREBALL: NEON_ORANGE,
    PowerUpKind.MULTI_BALL: NEON_YELLOW,
    PowerUpKind.CURVE_BALL: NEON_BLUE,
}

POWERUP_LABELS = {
    PowerUpKind.BIG_PADDLE: "BIG",
    PowerUpKind.SHRINK_ENEMY: "SHR",
    PowerUpKind.FIREBALL: "FIR",
    PowerUpKind.MULTI_BALL: "MUL",
    PowerUpKind.CURVE_BALL: "CRV",
}

ALL_POWERUP_KINDS = list(POWERUP_COLOURS.keys())


class PowerUp:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.colour = POWERUP_COLOURS[kind]
        self.label = POWERUP_LABELS[kind]
        self.rect = pygame.Rect(
            x - POWERUP_SIZE // 2, y - POWERUP_SIZE // 2, POWERUP_SIZE, POWERUP_SIZE
        )
        self.alive = True
        self.age = 0.0
        self.bob_offset = random.uniform(0, math.tau)

    def update(self, dt):
        self.age += dt

    def draw(self, surface, font):
        bob = math.sin(self.age * 3.0 + self.bob_offset) * 4
        cx, cy = self.x, int(self.y + bob)
        # glow
        glow_r = POWERUP_SIZE // 2 + 6 + int(math.sin(self.age * 5) * 3)
        glow_c = tuple(max(0, c - 100) for c in self.colour)
        pygame.draw.circle(surface, glow_c, (cx, cy), glow_r)
        # body
        pygame.draw.rect(
            surface,
            self.colour,
            (cx - POWERUP_SIZE // 2, cy - POWERUP_SIZE // 2, POWERUP_SIZE, POWERUP_SIZE),
            border_radius=5,
        )
        # label
        txt = font.render(self.label, True, BLACK)
        surface.blit(txt, (cx - txt.get_width() // 2, cy - txt.get_height() // 2))


# ---------------------------------------------------------------------------
# Paddle
# ---------------------------------------------------------------------------
class Paddle:
    def __init__(self, x, y, colour):
        self.base_x = x
        self.x = float(x)
        self.y = float(y)
        self.w = PADDLE_W
        self.h = PADDLE_H
        self.base_h = PADDLE_H
        self.colour = colour
        self.speed = PADDLE_SPEED
        self.vy = 0.0  # current frame velocity for spin
        self.score = 0
        self.effect_timers = {}  # kind -> remaining seconds

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.w / 2), int(self.y - self.h / 2), self.w, int(self.h))

    @property
    def center_y(self):
        return self.y

    def apply_power(self, kind, target_is_self):
        if kind == PowerUpKind.BIG_PADDLE and target_is_self:
            self.effect_timers[PowerUpKind.BIG_PADDLE] = POWERUP_DURATION
        elif kind == PowerUpKind.SHRINK_ENEMY and not target_is_self:
            self.effect_timers[PowerUpKind.SHRINK_ENEMY] = POWERUP_DURATION

    def update(self, dt):
        # Tick effect timers
        expired = []
        for k in list(self.effect_timers):
            self.effect_timers[k] -= dt
            if self.effect_timers[k] <= 0:
                expired.append(k)
        for k in expired:
            del self.effect_timers[k]

        # Compute effective paddle height
        target_h = self.base_h
        if PowerUpKind.BIG_PADDLE in self.effect_timers:
            target_h = self.base_h * 1.7
        if PowerUpKind.SHRINK_ENEMY in self.effect_timers:
            target_h = self.base_h * 0.55
        self.h += (target_h - self.h) * min(1.0, dt * 10)

        # Clamp to screen
        half = self.h / 2
        self.y = clamp(self.y, half, SCREEN_H - half)

    def move(self, direction, dt):
        """direction: -1 (up) / +1 (down) / 0"""
        self.vy = direction * self.speed * 60
        self.y += direction * self.speed * dt * 60

    def draw(self, surface):
        colour = self.colour
        # Flash if an effect is active
        if self.effect_timers:
            flash = int(pygame.time.get_ticks() / 120) % 2 == 0
            if flash:
                colour = WHITE
        rect = self.rect
        pygame.draw.rect(surface, colour, rect, border_radius=4)
        # inner highlight
        inner = rect.inflate(-4, -6)
        pygame.draw.rect(surface, lerp_colour(colour, WHITE, 0.25), inner, border_radius=3)


# ---------------------------------------------------------------------------
# Ball
# ---------------------------------------------------------------------------
class Ball:
    def __init__(self, x, y, angle=None, speed=None):
        self.x = float(x)
        self.y = float(y)
        if angle is None:
            angle = random.uniform(-math.pi / 4, math.pi / 4)
            if random.random() < 0.5:
                angle += math.pi
        self.speed = speed or BALL_BASE_SPEED
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
        self.radius = BALL_RADIUS
        self.alive = True
        self.rally = 0
        self.curve = 0.0  # curve factor
        self.curve_time = 0.0
        self.fireball = False
        self.fireball_time = 0.0

    @property
    def rect(self):
        r = self.radius
        return pygame.Rect(int(self.x - r), int(self.y - r), r * 2, r * 2)

    def colour(self):
        speed_ratio = clamp((self.speed - BALL_BASE_SPEED) / (BALL_MAX_SPEED - BALL_BASE_SPEED), 0, 1)
        if self.fireball:
            return lerp_colour(NEON_ORANGE, (255, 50, 20), speed_ratio)
        return lerp_colour(WHITE, NEON_PINK, speed_ratio)

    def update(self, dt):
        # Curve-ball wiggle
        if self.curve_time > 0:
            self.curve_time -= dt
            self.vy += self.curve * math.sin(pygame.time.get_ticks() * 0.015) * dt * 60
        else:
            self.curve = 0.0

        # Fireball timer
        if self.fireball_time > 0:
            self.fireball_time -= dt
            if self.fireball_time <= 0:
                self.fireball = False

        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60

        # Wall bounce (top / bottom)
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = abs(self.vy)
        elif self.y + self.radius >= SCREEN_H:
            self.y = SCREEN_H - self.radius
            self.vy = -abs(self.vy)

    def apply_power(self, kind):
        if kind == PowerUpKind.FIREBALL:
            self.fireball = True
            self.fireball_time = POWERUP_DURATION
            self.speed = min(self.speed + 3, BALL_MAX_SPEED)
            self._recalc_velocity()
        elif kind == PowerUpKind.CURVE_BALL:
            self.curve = random_sign() * random.uniform(3.0, 6.0)
            self.curve_time = POWERUP_DURATION

    def rally_hit(self, paddle_vy):
        """Called on every paddle hit."""
        self.rally += 1
        # Accelerate
        self.speed = min(self.speed + BALL_RALLY_ACCEL, BALL_MAX_SPEED)
        # Spin: paddle motion imparts vertical deflection
        spin = paddle_vy * 0.08
        self.vy += spin
        self._recalc_velocity()

    def _recalc_velocity(self):
        """Maintain direction but set magnitude to self.speed."""
        mag = math.hypot(self.vx, self.vy) or 1
        self.vx = self.vx / mag * self.speed
        self.vy = self.vy / mag * self.speed

    def draw(self, surface):
        c = self.colour()
        pos = (int(self.x), int(self.y))
        # glow
        if self.fireball:
            pygame.draw.circle(surface, (80, 20, 0), pos, self.radius + 6)
        else:
            pygame.draw.circle(surface, tuple(max(0, ch - 160) for ch in c), pos, self.radius + 4)
        pygame.draw.circle(surface, c, pos, self.radius)
        # highlight
        hl = (int(self.x) - 2, int(self.y) - 2)
        pygame.draw.circle(surface, lerp_colour(c, WHITE, 0.5), hl, max(2, self.radius // 3))


# ---------------------------------------------------------------------------
# Game
# ---------------------------------------------------------------------------
class PongRemix:
    """Main game class — owns the loop, state, and all entities."""

    # States
    MENU = 0
    PLAYING = 1
    GOAL = 2
    GAME_OVER = 3

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Pong Remix")
        self.clock = pygame.time.Clock()
        self.running = True

        # Fonts
        self.font_big = pygame.font.SysFont("monospace", 64, bold=True)
        self.font_med = pygame.font.SysFont("monospace", 28, bold=True)
        self.font_sm = pygame.font.SysFont("monospace", 18)

        # Audio (generate simple beeps as fallback — no asset files needed)
        self._init_sounds()

        # Paddles
        self.p1 = Paddle(PADDLE_MARGIN, SCREEN_H // 2, NEON_BLUE)
        self.p2 = Paddle(SCREEN_W - PADDLE_MARGIN, SCREEN_H // 2, NEON_PINK)

        # Balls, particles, power-ups
        self.balls: list[Ball] = []
        self.particles: list[Particle] = []
        self.powerups: list[PowerUp] = []

        # State
        self.state = self.MENU
        self.two_player = False
        self.goal_timer = 0.0
        self.shake_offset = [0, 0]
        self.shake_timer = 0.0
        self.powerup_timer = random.uniform(*POWERUP_SPAWN_INTERVAL)
        self.use_mouse_p1 = False

    # ------------------------------------------------------------------
    # Sound synthesiser (no external assets needed)
    # ------------------------------------------------------------------
    def _init_sounds(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        self.snd_hit = self._make_beep(440, 0.06)
        self.snd_wall = self._make_beep(330, 0.04)
        self.snd_goal = self._make_beep(220, 0.25)
        self.snd_powerup = self._make_beep(660, 0.10)

    @staticmethod
    def _make_beep(freq, duration, volume=0.3):
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        buf = bytearray(n_samples * 2)
        for i in range(n_samples):
            t = i / sample_rate
            # Exponential decay envelope
            envelope = max(0.0, 1.0 - t / duration)
            val = int(32767 * volume * envelope * math.sin(2 * math.pi * freq * t))
            val = clamp(val, -32767, 32767)
            # little-endian signed 16-bit
            buf[i * 2] = val & 0xFF
            buf[i * 2 + 1] = (val >> 8) & 0xFF
        snd = pygame.mixer.Sound(buffer=bytes(buf))
        return snd

    # ------------------------------------------------------------------
    # Public entry
    # ------------------------------------------------------------------
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)  # cap delta to avoid spiral-of-death
            self._handle_events()
            self._update(dt)
            self._draw()
        pygame.quit()

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == self.PLAYING:
                        self.state = self.MENU
                    else:
                        self.running = False
                elif event.key == pygame.K_RETURN:
                    if self.state in (self.MENU, self.GAME_OVER):
                        keys = pygame.key.get_pressed()
                        self.two_player = keys[pygame.K_TAB]
                        self._start_game()
                elif event.key == pygame.K_m:
                    if self.state == self.MENU:
                        self.use_mouse_p1 = not self.use_mouse_p1

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def _update(self, dt):
        if self.state == self.MENU:
            return
        if self.state == self.GAME_OVER:
            return
        if self.state == self.GOAL:
            self.goal_timer -= dt
            self._update_particles(dt)
            self._update_shake(dt)
            if self.goal_timer <= 0:
                if self.p1.score >= WIN_SCORE or self.p2.score >= WIN_SCORE:
                    self.state = self.GAME_OVER
                else:
                    self._serve()
                    self.state = self.PLAYING
            return

        # -- PLAYING state ------------------------------------------------
        self._input_paddles(dt)
        self.p1.update(dt)
        self.p2.update(dt)

        # Balls
        for ball in self.balls:
            ball.update(dt)
        self._check_collisions()
        # Remove dead balls
        self.balls = [b for b in self.balls if b.alive]
        # If all balls gone, score point for whichever side
        if not self.balls:
            # Shouldn't normally happen — goals handle this — but safety net
            self._serve()

        # Power-ups
        self.powerup_timer -= dt
        if self.powerup_timer <= 0:
            self._spawn_powerup()
            self.powerup_timer = random.uniform(*POWERUP_SPAWN_INTERVAL)
        for pu in self.powerups:
            pu.update(dt)
        self.powerups = [pu for pu in self.powerups if pu.alive]

        # Particles
        self._update_particles(dt)

        # Shake
        self._update_shake(dt)

        # Spawn ball-trail particles
        for ball in self.balls:
            self._spawn_trail(ball)

    def _input_paddles(self, dt):
        keys = pygame.key.get_pressed()

        # Player 1
        if self.use_mouse_p1:
            my = pygame.mouse.get_pos()[1]
            diff = my - self.p1.y
            move = clamp(diff, -self.p1.speed * 60 * dt, self.p1.speed * 60 * dt)
            self.p1.vy = move / dt if dt > 0 else 0
            self.p1.y += move
        else:
            d1 = 0
            if keys[pygame.K_w]:
                d1 -= 1
            if keys[pygame.K_s]:
                d1 += 1
            self.p1.move(d1, dt)

        # Player 2 / AI
        if self.two_player:
            d2 = 0
            if keys[pygame.K_UP]:
                d2 -= 1
            if keys[pygame.K_DOWN]:
                d2 += 1
            self.p2.move(d2, dt)
        else:
            self._ai_move(dt)

    def _ai_move(self, dt):
        """Adaptive AI — tracks the closest approaching ball with slight delay."""
        target_y = SCREEN_H / 2
        best_dist = float("inf")
        for ball in self.balls:
            if ball.vx > 0:  # approaching right paddle
                dist = self.p2.x - ball.x
                if 0 < dist < best_dist:
                    best_dist = dist
                    # Predict Y at paddle x
                    if ball.vx != 0:
                        t_arrive = dist / (ball.vx * 60)
                        predicted_y = ball.y + ball.vy * 60 * t_arrive
                        # Simple bounce prediction
                        while predicted_y < 0 or predicted_y > SCREEN_H:
                            if predicted_y < 0:
                                predicted_y = -predicted_y
                            if predicted_y > SCREEN_H:
                                predicted_y = 2 * SCREEN_H - predicted_y
                        target_y = predicted_y

        # Adaptive difficulty: reaction speed scales with score difference
        score_diff = self.p2.score - self.p1.score
        ai_speed_factor = clamp(0.65 + score_diff * 0.07, 0.45, 0.95)
        diff = target_y - self.p2.y
        max_move = self.p2.speed * ai_speed_factor * 60 * dt
        move = clamp(diff, -max_move, max_move)
        self.p2.vy = move / dt if dt > 0 else 0
        self.p2.y += move

    # -- Collisions -------------------------------------------------------
    def _check_collisions(self):
        for ball in self.balls:
            # Left goal
            if ball.x - ball.radius <= 0:
                self.p2.score += 1
                ball.alive = False
                self._on_goal(side="left")
                continue
            # Right goal
            if ball.x + ball.radius >= SCREEN_W:
                self.p1.score += 1
                ball.alive = False
                self._on_goal(side="right")
                continue

            # Paddle collisions
            self._paddle_ball(self.p1, ball, from_left=True)
            self._paddle_ball(self.p2, ball, from_left=False)

            # Power-up collisions
            for pu in self.powerups:
                if pu.alive and ball.rect.colliderect(pu.rect):
                    pu.alive = False
                    self._collect_powerup(pu, ball)

    def _paddle_ball(self, paddle, ball, from_left):
        prect = paddle.rect
        if not ball.rect.colliderect(prect):
            return
        # Ensure ball is moving toward paddle
        if from_left and ball.vx > 0:
            return
        if not from_left and ball.vx < 0:
            return

        # Reflect
        ball.vx = -ball.vx
        # Offset from centre → angle control
        offset = (ball.y - paddle.center_y) / (paddle.h / 2)
        offset = clamp(offset, -1.0, 1.0)
        ball.vy = offset * ball.speed * 0.75

        # Push out of paddle
        if from_left:
            ball.x = prect.right + ball.radius
        else:
            ball.x = prect.left - ball.radius

        ball.rally_hit(paddle.vy)
        self.snd_hit.play()

        # Burst particles at hit location
        self._spawn_burst(ball.x, ball.y, ball.colour(), count=12)

    def _on_goal(self, side):
        self.state = self.GOAL
        self.goal_timer = 1.2
        self.shake_timer = 0.3
        self.snd_goal.play()
        # Confetti
        cx = 80 if side == "left" else SCREEN_W - 80
        for _ in range(40):
            self.particles.append(
                Particle(
                    cx + random.uniform(-30, 30),
                    SCREEN_H // 2 + random.uniform(-80, 80),
                    random.uniform(-120, 120),
                    random.uniform(-200, 50),
                    random.uniform(0.5, 1.2),
                    random.choice([NEON_BLUE, NEON_PINK, NEON_GREEN, NEON_YELLOW, WHITE]),
                    radius=random.randint(2, 5),
                )
            )

    def _collect_powerup(self, pu, ball):
        self.snd_powerup.play()
        # Determine who benefits: based on which side the ball is heading
        pitcher = self.p1 if ball.vx > 0 else self.p2
        receiver = self.p2 if ball.vx > 0 else self.p1

        kind = pu.kind
        if kind == PowerUpKind.BIG_PADDLE:
            pitcher.apply_power(kind, target_is_self=True)
        elif kind == PowerUpKind.SHRINK_ENEMY:
            receiver.apply_power(kind, target_is_self=False)
        elif kind in (PowerUpKind.FIREBALL, PowerUpKind.CURVE_BALL):
            ball.apply_power(kind)
        elif kind == PowerUpKind.MULTI_BALL:
            # Spawn an extra ball from the same position
            angle = math.atan2(ball.vy, ball.vx) + random.choice([-1, 1]) * random.uniform(0.3, 0.8)
            new_ball = Ball(ball.x, ball.y, angle=angle, speed=ball.speed)
            new_ball.fireball = ball.fireball
            new_ball.fireball_time = ball.fireball_time
            self.balls.append(new_ball)

        # Visual burst
        self._spawn_burst(pu.x, pu.y, pu.colour, count=16)

    # -- Particles --------------------------------------------------------
    def _spawn_trail(self, ball):
        if len(self.particles) >= MAX_PARTICLES:
            return
        c = ball.colour()
        self.particles.append(
            Particle(
                ball.x + random.uniform(-2, 2),
                ball.y + random.uniform(-2, 2),
                random.uniform(-15, 15),
                random.uniform(-15, 15),
                random.uniform(0.1, PARTICLE_LIFETIME),
                c,
                radius=random.randint(2, ball.radius),
            )
        )

    def _spawn_burst(self, x, y, colour, count=10):
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            spd = random.uniform(40, 180)
            self.particles.append(
                Particle(
                    x, y,
                    math.cos(angle) * spd,
                    math.sin(angle) * spd,
                    random.uniform(0.15, 0.5),
                    colour,
                    radius=random.randint(2, 4),
                )
            )

    def _update_particles(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    # -- Power-up spawning -----------------------------------------------
    def _spawn_powerup(self):
        kind = random.choice(ALL_POWERUP_KINDS)
        margin = 120
        x = random.randint(margin, SCREEN_W - margin)
        y = random.randint(60, SCREEN_H - 60)
        self.powerups.append(PowerUp(x, y, kind))

    # -- Shake ------------------------------------------------------------
    def _update_shake(self, dt):
        if self.shake_timer > 0:
            self.shake_timer -= dt
            intensity = int(self.shake_timer * 30)
            self.shake_offset[0] = random.randint(-intensity, intensity)
            self.shake_offset[1] = random.randint(-intensity, intensity)
        else:
            self.shake_offset = [0, 0]

    # -- Game-flow helpers ------------------------------------------------
    def _start_game(self):
        self.p1.score = 0
        self.p2.score = 0
        self.p1.effect_timers.clear()
        self.p2.effect_timers.clear()
        self.p1.h = self.p1.base_h
        self.p2.h = self.p2.base_h
        self.particles.clear()
        self.powerups.clear()
        self.powerup_timer = random.uniform(*POWERUP_SPAWN_INTERVAL)
        self._serve()
        self.state = self.PLAYING

    def _serve(self):
        self.balls.clear()
        self.balls.append(Ball(SCREEN_W // 2, SCREEN_H // 2))
        # Reset paddle positions
        self.p1.y = SCREEN_H // 2
        self.p2.y = SCREEN_H // 2

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def _draw(self):
        surf = self.screen
        sx, sy = self.shake_offset

        surf.fill(BLACK)

        if self.state == self.MENU:
            self._draw_menu(surf)
        elif self.state == self.GAME_OVER:
            self._draw_game(surf, sx, sy)
            self._draw_game_over(surf)
        else:
            self._draw_game(surf, sx, sy)
            if self.state == self.GOAL:
                self._draw_goal_flash(surf)

        pygame.display.flip()

    # -- Menu -------------------------------------------------------------
    def _draw_menu(self, surf):
        # Title
        title = self.font_big.render("PONG REMIX", True, NEON_PINK)
        surf.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 120))

        lines = [
            "Press ENTER to start (1-player vs AI)",
            "Hold TAB + ENTER for 2-player mode",
            "",
            "Player 1:  W / S   (or press M to toggle mouse)",
            "Player 2:  UP / DOWN  (2-player only)",
            "",
            f"Mouse control: {'ON' if self.use_mouse_p1 else 'OFF'}",
            "",
            "First to 7 wins.  ESC to quit.",
            "",
            "POWER-UPS:",
            "  BIG  - Enlarge your paddle",
            "  SHR  - Shrink opponent's paddle",
            "  FIR  - Fireball speed boost",
            "  MUL  - Spawn an extra ball",
            "  CRV  - Curve ball wobble",
        ]
        y = 220
        for line in lines:
            colour = GREY if line.startswith("  ") else WHITE
            txt = self.font_sm.render(line, True, colour)
            surf.blit(txt, (SCREEN_W // 2 - txt.get_width() // 2, y))
            y += 24

    # -- Game field -------------------------------------------------------
    def _draw_game(self, surf, sx, sy):
        # Centre line
        for y in range(0, SCREEN_H, 20):
            pygame.draw.rect(surf, DARK_GREY, (SCREEN_W // 2 - 1 + sx, y + sy, 2, 10))

        # Scores
        s1 = self.font_big.render(str(self.p1.score), True, NEON_BLUE)
        s2 = self.font_big.render(str(self.p2.score), True, NEON_PINK)
        surf.blit(s1, (SCREEN_W // 2 - 80 + sx, 20 + sy))
        surf.blit(s2, (SCREEN_W // 2 + 45 + sx, 20 + sy))

        # Particles (behind everything)
        for p in self.particles:
            p.draw(surf)

        # Power-ups
        for pu in self.powerups:
            pu.draw(surf, self.font_sm)

        # Paddles
        self.p1.draw(surf)
        self.p2.draw(surf)

        # Balls
        for ball in self.balls:
            ball.draw(surf)

        # Active effects HUD
        self._draw_effects_hud(surf)

    def _draw_effects_hud(self, surf):
        y = SCREEN_H - 30
        for paddle, x_anchor in ((self.p1, 10), (self.p2, SCREEN_W - 160)):
            for kind, remaining in paddle.effect_timers.items():
                colour = POWERUP_COLOURS.get(kind, WHITE)
                label = f"{POWERUP_LABELS.get(kind, '???')} {remaining:.1f}s"
                txt = self.font_sm.render(label, True, colour)
                surf.blit(txt, (x_anchor, y))
                y -= 20
            y = SCREEN_H - 30  # reset for other paddle

    def _draw_goal_flash(self, surf):
        alpha = clamp(self.goal_timer / 1.2, 0, 1)
        if int(alpha * 10) % 2 == 0:
            txt = self.font_big.render("GOAL!", True, NEON_YELLOW)
            surf.blit(txt, (SCREEN_W // 2 - txt.get_width() // 2, SCREEN_H // 2 - 40))

    def _draw_game_over(self, surf):
        # Dim overlay
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surf.blit(overlay, (0, 0))

        winner = "Player 1" if self.p1.score >= WIN_SCORE else ("Player 2" if self.two_player else "AI")
        colour = NEON_BLUE if self.p1.score >= WIN_SCORE else NEON_PINK
        txt = self.font_big.render(f"{winner} WINS!", True, colour)
        surf.blit(txt, (SCREEN_W // 2 - txt.get_width() // 2, SCREEN_H // 2 - 60))

        sub = self.font_med.render("Press ENTER to play again", True, WHITE)
        surf.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, SCREEN_H // 2 + 20))

        esc = self.font_sm.render("ESC to quit", True, GREY)
        surf.blit(esc, (SCREEN_W // 2 - esc.get_width() // 2, SCREEN_H // 2 + 60))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    game = PongRemix()
    game.run()


if __name__ == "__main__":
    main()
