"""Settings menu scene — volume, fullscreen, etc."""

import pygame
from engine.scene_manager import Scene, SceneManager
from engine.input_handler import Action
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, user_settings


class SettingsMenu(Scene):
    """Overlay scene for adjustable game settings."""

    OPTIONS = ["Music Volume", "SFX Volume", "Fullscreen", "Back"]

    def __init__(self, manager: SceneManager):
        super().__init__(manager)
        self.selected = 0

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self, dt: float, input_handler=None):
        if input_handler is None:
            return
        if input_handler.is_just_pressed(Action.UP):
            self.selected = (self.selected - 1) % len(self.OPTIONS)
        if input_handler.is_just_pressed(Action.DOWN):
            self.selected = (self.selected + 1) % len(self.OPTIONS)

        option = self.OPTIONS[self.selected]

        if option == "Music Volume":
            if input_handler.is_just_pressed(Action.LEFT):
                user_settings["music_volume"] = max(0, user_settings["music_volume"] - 10)
            if input_handler.is_just_pressed(Action.RIGHT):
                user_settings["music_volume"] = min(100, user_settings["music_volume"] + 10)
        elif option == "SFX Volume":
            if input_handler.is_just_pressed(Action.LEFT):
                user_settings["sfx_volume"] = max(0, user_settings["sfx_volume"] - 10)
            if input_handler.is_just_pressed(Action.RIGHT):
                user_settings["sfx_volume"] = min(100, user_settings["sfx_volume"] + 10)
        elif option == "Fullscreen":
            if input_handler.is_just_pressed(Action.CONFIRM) or input_handler.is_just_pressed(Action.LEFT) or input_handler.is_just_pressed(Action.RIGHT):
                user_settings["fullscreen"] = not user_settings["fullscreen"]
                flags = pygame.FULLSCREEN if user_settings["fullscreen"] else 0
                pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

        if option == "Back" and (input_handler.is_just_pressed(Action.CONFIRM) or input_handler.is_just_pressed(Action.JUMP)):
            self.manager.pop()
        if input_handler.is_just_pressed(Action.BACK):
            self.manager.pop()

    def draw(self, surface: pygame.Surface):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        title_font = pygame.font.SysFont("arial", 42, bold=True)
        title = title_font.render("Settings", True, (255, 255, 255))
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 100)))

        font = pygame.font.SysFont("arial", 28)
        for i, option in enumerate(self.OPTIONS):
            is_sel = i == self.selected
            color = (255, 255, 100) if is_sel else (200, 200, 200)
            y = 200 + i * 60

            if option == "Music Volume":
                label = f"Music Volume:  < {user_settings['music_volume']:3d} >"
            elif option == "SFX Volume":
                label = f"SFX Volume:    < {user_settings['sfx_volume']:3d} >"
            elif option == "Fullscreen":
                state = "ON" if user_settings["fullscreen"] else "OFF"
                label = f"Fullscreen:      {state}"
            else:
                label = option

            text = font.render(label, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            surface.blit(text, rect)
            if is_sel:
                arrow = font.render(">", True, (255, 255, 100))
                surface.blit(arrow, (rect.left - 30, rect.y))
