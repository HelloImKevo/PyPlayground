"""Core gameplay scene — integrates level, player, enemies, collectibles, HUD."""

import pygame
from engine.scene_manager import Scene, SceneManager
from engine.camera import Camera
from engine.input_handler import Action
from engine.physics import apply_gravity, resolve_tilemap_collisions
from engine.asset_loader import get_sound
from entities.player import Player
from entities.enemy import Enemy
from entities.collectible import Coin, Mushroom, Star
from entities.particles import ParticleEmitter
from levels.level_loader import load_level, level_exists
from levels.tilemap import SOLID_TILES
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE,
    COIN_SCORE, MUSHROOM_SCORE, STOMP_BOUNCE,
    user_settings,
)


class GameplayScene(Scene):
    """Main in-game scene."""

    def __init__(self, manager: SceneManager, level_id: int = 1):
        super().__init__(manager)
        self.level_id = level_id
        self.paused = False
        self._fade_alpha = 255
        self._fading_in = True

        # Load level
        self.level = load_level(level_id)
        tilemap = self.level.tilemap

        # Camera
        self.camera = Camera(tilemap.width, tilemap.height)

        # Player
        px, py = self.level.player_spawn
        self.player = Player(px, py)

        # Enemies
        self.enemies: list[Enemy] = []
        for e in self.level.enemy_spawns:
            self.enemies.append(Enemy(e["x"], e["y"], e["type"]))

        # Coins
        self.coins: list[Coin] = []
        for cx, cy in self.level.coin_spawns:
            self.coins.append(Coin(cx, cy))

        # Dynamic collectibles (from question blocks)
        self.powerups: list = []

        # Question block state: (col, row) -> used?
        self._qblock_used: dict[tuple[int, int], bool] = {}
        self._qblock_items: dict[tuple[int, int], str] = {}
        for qb in self.level.question_blocks:
            key = (qb["col"], qb["row"])
            self._qblock_used[key] = False
            self._qblock_items[key] = qb.get("item", "coin")

        # Particles
        self.particles = ParticleEmitter()

        # Score popups
        self._popups: list[dict] = []

        # Respawn tracking
        self._respawn_timer = 0.0
        self._respawning = False

        # Victory tracking
        self._victory_timer = 0.0

        # Audio
        self._sounds = {
            k: get_sound(k)
            for k in ("jump", "coin", "stomp", "powerup", "damage",
                      "death", "brick_break", "victory")
        }
        self._player_was_on_ground = True

    def on_enter(self):
        self._fade_alpha = 255
        self._fading_in = True

    def handle_event(self, event: pygame.event.Event):
        pass

    def _play(self, name: str):
        """Play a sound effect with the current SFX volume."""
        snd = self._sounds.get(name)
        if snd:
            vol = user_settings["sfx_volume"] / 100.0
            snd.set_volume(vol)
            snd.play()

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def update(self, dt: float, input_handler=None):
        # Fade in
        if self._fading_in:
            self._fade_alpha = max(0, self._fade_alpha - 400 * dt)
            if self._fade_alpha <= 0:
                self._fading_in = False

        if input_handler and input_handler.is_just_pressed(Action.PAUSE):
            self.paused = not self.paused
        if self.paused:
            return

        # --- Respawn sequence ---
        if self._respawning:
            self._respawn_timer -= dt
            if self._respawn_timer <= 0:
                self._respawn()
            return

        # --- Death check ---
        if self.player.dead:
            self.player.update_physics(dt)
            if self.player._death_timer > 2.0:
                if self.player.lives <= 0:
                    from scenes.game_over import GameOverScene
                    self.manager.switch(GameOverScene(self.manager, self.player.score,
                                                      self.level_id))
                else:
                    self._respawning = True
                    self._respawn_timer = 0.5
            return

        # --- Victory auto-walk ---
        if self.player.victory:
            self._victory_timer += dt
            self.player.update_physics(dt)
            resolve_tilemap_collisions(self.player, self.level.tilemap, dt)
            self.camera.update(self.player.rect, dt)
            if self._victory_timer > 3.0:
                from scenes.victory import VictoryScene
                self.manager.switch(VictoryScene(self.manager, self.player.score,
                                                  self.level_id))
            self._update_particles(dt)
            return

        # --- Normal gameplay ---
        if input_handler:
            self.player.update_input(dt, input_handler)
        # Detect jump: player just got upward velocity while was on ground
        if self.player.vel.y < -100 and self._player_was_on_ground:
            self._play("jump")

        self.player.update_physics(dt)
        resolve_tilemap_collisions(self.player, self.level.tilemap, dt)

        # Landing particles
        if self.player.on_ground and not self._player_was_on_ground:
            self.particles.emit((self.player.rect.midbottom[0], self.player.rect.bottom),
                                4, (160, 140, 120), spread=80, speed=40,
                                lifetime=0.3, size=2)
        self._player_was_on_ground = self.player.on_ground

        # Pit death
        if self.player.rect.top > self.level.tilemap.height + 100:
            self.player.die()
            self._play("death")

        # Camera
        self.camera.update(self.player.rect, dt)

        # Enemies
        cam_left = self.camera.offset.x
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            # Only update enemies near camera
            if enemy.rect.right < cam_left - 200:
                enemy.alive = False  # despawn
                continue
            if enemy.rect.left > cam_left + SCREEN_WIDTH + 400:
                continue
            enemy.update(dt, self.level.tilemap)

        # Player-Enemy collisions
        self._check_enemy_collisions()

        # Coins
        for coin in self.coins:
            if coin.collected:
                continue
            coin.update(dt)
            if self.player.rect.colliderect(coin.rect):
                coin.collected = True
                self.player.score += COIN_SCORE
                self.player.coins += 1
                self._play("coin")
                self._spawn_popup(coin.rect.centerx, coin.rect.top, f"+{COIN_SCORE}")
                self.particles.emit(coin.rect.center, 8, (255, 215, 0),
                                    spread=60, speed=100, lifetime=0.4, size=3)

        # Powerups
        for pu in self.powerups:
            if pu.collected:
                continue
            pu.update(dt, self.level.tilemap)
            if self.player.rect.colliderect(pu.rect):
                pu.collected = True
                if isinstance(pu, Mushroom):
                    self.player.grow()
                    self.player.score += MUSHROOM_SCORE
                    self._play("powerup")
                    self._spawn_popup(pu.rect.centerx, pu.rect.top, f"+{MUSHROOM_SCORE}")
                    self.particles.emit(pu.rect.center, 12, (220, 40, 40),
                                        spread=80, speed=120, lifetime=0.5)
                elif isinstance(pu, Star):
                    self.player.activate_star()
                    self.player.score += MUSHROOM_SCORE
                    self._play("powerup")
                    self._spawn_popup(pu.rect.centerx, pu.rect.top, "STAR!")
                    self.particles.emit(pu.rect.center, 15, (255, 255, 0),
                                        spread=100, speed=150, lifetime=0.6)

        # Question block headbutt detection
        self._check_question_blocks()

        # Victory flag check
        if self.level.flag_pos:
            fx, fy = self.level.flag_pos
            flag_rect = pygame.Rect(fx, fy - TILE_SIZE * 2, TILE_SIZE, TILE_SIZE * 3)
            if self.player.rect.colliderect(flag_rect) and not self.player.victory:
                self.player.victory = True
                self._victory_timer = 0
                self._play("victory")
                self.particles.emit((fx, fy), 30, (255, 165, 0),
                                    spread=100, speed=200, lifetime=1.0, size=4)

        # Particles & popups
        self._update_particles(dt)
        self._update_popups(dt)

    def _check_enemy_collisions(self):
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            if not self.player.rect.colliderect(enemy.rect):
                continue

            # Stomping: player falling and bottom near enemy top
            if (self.player.vel.y > 0 and
                    self.player.rect.bottom - enemy.rect.top < enemy.rect.height * 0.5):
                if enemy.is_shell and enemy.vel.x == 0:
                    # Kick the shell
                    direction = 1 if self.player.rect.centerx < enemy.rect.centerx else -1
                    enemy.kick_shell(direction)
                    self.player.vel.y = STOMP_BOUNCE
                    self._play("stomp")
                else:
                    enemy.stomp()
                    self.player.vel.y = STOMP_BOUNCE
                    self._play("stomp")
                    self.player.score += 200
                    self._spawn_popup(enemy.rect.centerx, enemy.rect.top, "+200")
                    self.particles.emit(enemy.rect.center, 10, (160, 120, 80),
                                        spread=80, speed=100, lifetime=0.4, size=3)
            else:
                # Hit from side — player takes damage (star kills enemy instead)
                if self.player.is_star:
                    enemy.alive = False
                    self.player.score += 200
                    self._spawn_popup(enemy.rect.centerx, enemy.rect.top, "+200")
                    self.particles.emit(enemy.rect.center, 10, (160, 120, 80),
                                        spread=80, speed=100, lifetime=0.4, size=3)
                else:
                    self.player.take_damage()
                    if self.player.dead:
                        self._play("death")
                    elif not self.player.dead:
                        self._play("damage")
                        self.particles.emit(self.player.rect.center, 6,
                                            (255, 100, 100), spread=60, speed=80,
                                            lifetime=0.3)

        # Shell-vs-enemy collisions
        for enemy in self.enemies:
            if not enemy.alive or not enemy.is_shell or enemy.vel.x == 0:
                continue
            for other in self.enemies:
                if other is enemy or not other.alive:
                    continue
                if enemy.rect.colliderect(other.rect):
                    other.alive = False
                    self.player.score += 200
                    self.particles.emit(other.rect.center, 8, (160, 120, 80),
                                        spread=60, speed=100, lifetime=0.4)

    def _check_question_blocks(self):
        """Detect player headbutting question blocks from below."""
        if self.player.vel.y >= 0:
            return  # only when moving upward
        tilemap = self.level.tilemap
        # Check tile above player's head
        check_points = [
            (self.player.rect.left + 4, self.player.rect.top - 2),
            (self.player.rect.right - 4, self.player.rect.top - 2),
        ]
        for px, py in check_points:
            col = px // TILE_SIZE
            row = py // TILE_SIZE
            key = (col, row)
            if key in self._qblock_used and not self._qblock_used[key]:
                self._qblock_used[key] = True
                tilemap.set_tile(col, row, 6)
                self._play("brick_break")
                item = self._qblock_items[key]
                spawn_x = col * TILE_SIZE + TILE_SIZE // 2
                spawn_y = row * TILE_SIZE
                if item == "coin":
                    self.player.score += COIN_SCORE
                    self.player.coins += 1
                    self._spawn_popup(spawn_x, spawn_y, f"+{COIN_SCORE}")
                    self.particles.emit((spawn_x, spawn_y), 8, (255, 215, 0),
                                        spread=60, speed=100, lifetime=0.4, size=3)
                elif item == "mushroom":
                    self.powerups.append(Mushroom(spawn_x, spawn_y))
                elif item == "star":
                    self.powerups.append(Star(spawn_x, spawn_y))
                break  # only one block per frame

    def _respawn(self):
        self._respawning = False
        px, py = self.level.player_spawn
        self.player.dead = False
        self.player.rect.topleft = (px, py)
        self.player.vel = pygame.math.Vector2(0, 0)
        self.player.is_big = False
        self.player.height = TILE_SIZE - 4
        self.player.image = pygame.Surface((self.player.width, self.player.height))
        self.player.image.fill(self.player.COLOR_NORMAL)
        self.player.rect = self.player.image.get_rect(topleft=(px, py))
        self.player._invincible = True
        self.player._invincible_timer = 2.0
        self._fade_alpha = 255
        self._fading_in = True

    def _spawn_popup(self, x, y, text):
        self._popups.append({"x": x, "y": y, "text": text,
                             "timer": 1.0, "max": 1.0})

    def _update_popups(self, dt):
        alive = []
        for p in self._popups:
            p["timer"] -= dt
            p["y"] -= 60 * dt
            if p["timer"] > 0:
                alive.append(p)
        self._popups = alive

    def _update_particles(self, dt):
        self.particles.update(dt)

    # ------------------------------------------------------------------
    # DRAW
    # ------------------------------------------------------------------
    def draw(self, surface: pygame.Surface):
        # Sky gradient
        surface.fill((107, 140, 255))

        cam_off = (self.camera.offset.x, self.camera.offset.y)

        # Tilemap
        self.level.tilemap.draw(surface, cam_off)

        # Coins
        for coin in self.coins:
            if not coin.collected:
                coin.draw(surface, cam_off)

        # Powerups
        for pu in self.powerups:
            pu.draw(surface, cam_off)

        # Enemies
        for enemy in self.enemies:
            enemy.draw(surface, cam_off)

        # Player
        self.player.draw(surface, cam_off)

        # Particles
        self.particles.draw(surface, cam_off)

        # Score popups
        popup_font = pygame.font.SysFont("arial", 16, bold=True)
        for p in self._popups:
            alpha = max(0, min(255, int(255 * (p["timer"] / p["max"]))))
            txt = popup_font.render(p["text"], True, (255, 255, 255))
            txt.set_alpha(alpha)
            sx = int(p["x"]) - int(cam_off[0])
            sy = int(p["y"]) - int(cam_off[1])
            surface.blit(txt, (sx, sy))

        # HUD
        self._draw_hud(surface)

        # Pause overlay
        if self.paused:
            self._draw_pause(surface)

        # Fade overlay
        if self._fade_alpha > 0:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(int(self._fade_alpha))
            surface.blit(fade_surf, (0, 0))

    def _draw_hud(self, surface: pygame.Surface):
        font = pygame.font.SysFont("arial", 20, bold=True)
        # Score
        score_text = font.render(f"SCORE: {self.player.score:05d}", True, (255, 255, 255))
        surface.blit(score_text, (15, 10))
        # Coins
        coin_text = font.render(f"COINS: {self.player.coins}", True, (255, 215, 0))
        surface.blit(coin_text, (15, 35))
        # World
        world_text = font.render(f"WORLD {self.level.level_name}", True, (255, 255, 255))
        wr = world_text.get_rect(midtop=(SCREEN_WIDTH // 2, 10))
        surface.blit(world_text, wr)
        # Lives
        lives_text = font.render(f"LIVES: {self.player.lives}", True, (255, 255, 255))
        surface.blit(lives_text, (SCREEN_WIDTH - 140, 10))

    def _draw_pause(self, surface: pygame.Surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        font = pygame.font.SysFont("arial", 48, bold=True)
        text = font.render("PAUSED", True, (255, 255, 255))
        surface.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        small = pygame.font.SysFont("arial", 20)
        hint = small.render("Press ESC to resume", True, (200, 200, 200))
        surface.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
