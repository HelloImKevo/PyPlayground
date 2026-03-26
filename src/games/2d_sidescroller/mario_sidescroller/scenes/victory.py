"""Victory screen — shown after completing a level."""

import pygame
from engine.scene_manager import Scene, SceneManager
from engine.input_handler import Action
from levels.level_loader import level_exists
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class VictoryScene(Scene):
    """Level complete screen with score and navigation options."""

    OPTIONS = ["Next Level", "Main Menu"]

    def __init__(self, manager: SceneManager, score: int, level_id: int):
        super().__init__(manager)
        self.score = score
        self.level_id = level_id
        self.selected = 0
        self.timer = 0.0
        self._has_next = level_exists(level_id + 1)
        if not self._has_next:
            self.OPTIONS = ["Main Menu"]

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self, dt: float, input_handler=None):
        self.timer += dt
        if input_handler is None:
            return
        if input_handler.is_just_pressed(Action.UP):
            self.selected = (self.selected - 1) % len(self.OPTIONS)
        if input_handler.is_just_pressed(Action.DOWN):
            self.selected = (self.selected + 1) % len(self.OPTIONS)
        if input_handler.is_just_pressed(Action.CONFIRM) or input_handler.is_just_pressed(Action.JUMP):
            choice = self.OPTIONS[self.selected]
            if choice == "Next Level":
                from scenes.gameplay import GameplayScene
                self.manager.switch(GameplayScene(self.manager, self.level_id + 1))
            elif choice == "Main Menu":
                from scenes.title_screen import TitleScreen
                self.manager.switch(TitleScreen(self.manager))

    def draw(self, surface: pygame.Surface):
        surface.fill((20, 60, 20))

        title_font = pygame.font.SysFont("arial", 50, bold=True)
        font = pygame.font.SysFont("arial", 28)

        if self._has_next:
            title_text = "LEVEL COMPLETE!"
        else:
            title_text = "CONGRATULATIONS — YOU WIN!"

        title = title_font.render(title_text, True, (255, 220, 50))
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 120)))

        score_text = font.render(f"Final Score: {self.score:05d}", True, (255, 255, 255))
        surface.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, 220)))

        for i, option in enumerate(self.OPTIONS):
            color = (255, 255, 100) if i == self.selected else (200, 200, 200)
            text = font.render(option, True, color)
            y = 340 + i * 55
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            surface.blit(text, rect)
            if i == self.selected:
                arrow = font.render(">", True, (255, 255, 100))
                surface.blit(arrow, (rect.left - 30, rect.y))
