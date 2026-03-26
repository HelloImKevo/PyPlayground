"""Title Screen / Main Menu scene."""

import math
import pygame
from engine.scene_manager import Scene, SceneManager
from engine.input_handler import Action
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class TitleScreen(Scene):
    """Animated title with menu options: Start Game, Settings, Quit."""

    MENU_OPTIONS = ["Start Game", "Settings", "Quit"]

    def __init__(self, manager: SceneManager):
        super().__init__(manager)
        self.selected = 0
        self.timer = 0.0
        # Parallax layers: (color, speed, y_offset, height)
        self.parallax_layers = [
            ((30, 30, 80), 15, 350, 250),
            ((50, 50, 120), 30, 300, 300),
            ((70, 70, 160), 60, 250, 350),
        ]
        self.scroll_offsets = [0.0] * len(self.parallax_layers)

    def handle_event(self, event: pygame.event.Event):
        pass  # handled via input_handler in update

    def update(self, dt: float, input_handler=None):
        self.timer += dt
        # Scroll parallax
        for i, (_, speed, _, _) in enumerate(self.parallax_layers):
            self.scroll_offsets[i] = (self.scroll_offsets[i] + speed * dt) % SCREEN_WIDTH

        if input_handler is None:
            return
        if input_handler.is_just_pressed(Action.UP):
            self.selected = (self.selected - 1) % len(self.MENU_OPTIONS)
        if input_handler.is_just_pressed(Action.DOWN):
            self.selected = (self.selected + 1) % len(self.MENU_OPTIONS)
        if input_handler.is_just_pressed(Action.CONFIRM) or input_handler.is_just_pressed(Action.JUMP):
            self._select_option()
        if input_handler.is_just_pressed(Action.BACK):
            self._quit()

    def _select_option(self):
        choice = self.MENU_OPTIONS[self.selected]
        if choice == "Start Game":
            from scenes.gameplay import GameplayScene
            self.manager.switch(GameplayScene(self.manager, level_id=1))
        elif choice == "Settings":
            from scenes.settings_menu import SettingsMenu
            self.manager.push(SettingsMenu(self.manager))
        elif choice == "Quit":
            self._quit()

    @staticmethod
    def _quit():
        pygame.quit()
        raise SystemExit

    def draw(self, surface: pygame.Surface):
        surface.fill((20, 20, 50))

        # Parallax background
        for i, (color, _speed, y_off, h) in enumerate(self.parallax_layers):
            offset = int(self.scroll_offsets[i])
            pygame.draw.rect(surface, color, (-offset, y_off, SCREEN_WIDTH + 200, h))
            pygame.draw.rect(surface, color, (SCREEN_WIDTH - offset, y_off, SCREEN_WIDTH + 200, h))

        # Title text with sine-wave bob
        title_font = pygame.font.SysFont("arial", 56, bold=True)
        bob_y = math.sin(self.timer * 2) * 8
        title_surf = title_font.render("Mario Sidescroller", True, (255, 220, 50))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 120 + bob_y))
        surface.blit(title_surf, title_rect)

        # Menu options
        menu_font = pygame.font.SysFont("arial", 30)
        for i, option in enumerate(self.MENU_OPTIONS):
            color = (255, 255, 100) if i == self.selected else (200, 200, 200)
            text_surf = menu_font.render(option, True, color)
            y = 280 + i * 55
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y))
            surface.blit(text_surf, text_rect)
            if i == self.selected:
                # Arrow indicator
                arrow = menu_font.render(">", True, (255, 255, 100))
                surface.blit(arrow, (text_rect.left - 30, text_rect.y))

        # Footer
        small_font = pygame.font.SysFont("arial", 16)
        footer = small_font.render("Arrow keys / WASD to navigate  |  Enter / Space to select", True, (140, 140, 140))
        surface.blit(footer, footer.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)))
