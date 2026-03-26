"""Mario-Style Sidescroller — entry point."""

import sys
import os

# Ensure the package root is on sys.path so bare imports work.
sys.path.insert(0, os.path.dirname(__file__))

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, user_settings
from engine.scene_manager import SceneManager
from engine.input_handler import InputHandler
from scenes.title_screen import TitleScreen


def main():
    pygame.init()
    pygame.mixer.init()

    flags = 0
    if user_settings["fullscreen"]:
        flags |= pygame.FULLSCREEN
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    pygame.display.set_caption("Mario Sidescroller")
    clock = pygame.time.Clock()

    scene_manager = SceneManager()
    input_handler = InputHandler()

    # Start at the title screen
    scene_manager.push(TitleScreen(scene_manager))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        input_handler.begin_frame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            input_handler.process_event(event)
            if scene_manager.current:
                scene_manager.current.handle_event(event)

        if not running:
            break

        if scene_manager.current:
            scene_manager.current.update(dt, input_handler)
            scene_manager.current.draw(screen)
        else:
            running = False

        # Show FPS in title bar
        fps_str = f"Mario Sidescroller — {clock.get_fps():.0f} FPS"
        pygame.display.set_caption(fps_str)
        pygame.display.flip()

        if scene_manager.is_empty:
            running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
