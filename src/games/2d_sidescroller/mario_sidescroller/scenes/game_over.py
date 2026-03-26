"""Game Over screen."""

import pygame
from engine.scene_manager import Scene, SceneManager
from engine.input_handler import Action
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class GameOverScene(Scene):
    """Game over screen with retry / quit options."""

    OPTIONS = ["Retry", "Main Menu"]

    def __init__(self, manager: SceneManager, score: int, level_id: int = 1):
        super().__init__(manager)
        self.score = score
        self.level_id = level_id
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
        if input_handler.is_just_pressed(Action.CONFIRM) or input_handler.is_just_pressed(Action.JUMP):
            choice = self.OPTIONS[self.selected]
            if choice == "Retry":
                from scenes.gameplay import GameplayScene
                self.manager.switch(GameplayScene(self.manager, self.level_id))
            elif choice == "Main Menu":
                from scenes.title_screen import TitleScreen
                self.manager.switch(TitleScreen(self.manager))

    def draw(self, surface: pygame.Surface):
        surface.fill((60, 10, 10))

        title_font = pygame.font.SysFont("arial", 56, bold=True)
        font = pygame.font.SysFont("arial", 28)

        title = title_font.render("GAME OVER", True, (255, 60, 60))
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 150)))

        score_text = font.render(f"Final Score: {self.score:05d}", True, (255, 255, 255))
        surface.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, 250)))

        for i, option in enumerate(self.OPTIONS):
            color = (255, 255, 100) if i == self.selected else (200, 200, 200)
            text = font.render(option, True, color)
            y = 350 + i * 55
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            surface.blit(text, rect)
            if i == self.selected:
                arrow = font.render(">", True, (255, 255, 100))
                surface.blit(arrow, (rect.left - 30, rect.y))
