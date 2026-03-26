"""Scene Manager and base Scene class."""

from abc import ABC, abstractmethod
import pygame


class Scene(ABC):
    """Abstract base class for all game scenes."""

    def __init__(self, manager: "SceneManager"):
        self.manager = manager

    def on_enter(self):
        """Called when the scene becomes the active scene."""

    def on_exit(self):
        """Called when the scene is removed or replaced."""

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """Process a single pygame event."""

    @abstractmethod
    def update(self, dt: float, input_handler=None):
        """Update scene logic. *dt* is seconds since last frame."""

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        """Draw the scene onto *surface*."""


class SceneManager:
    """Stack-based scene manager (push / pop / switch)."""

    def __init__(self):
        self._stack: list[Scene] = []

    @property
    def current(self) -> Scene | None:
        return self._stack[-1] if self._stack else None

    def push(self, scene: Scene):
        if self.current:
            self.current.on_exit()
        self._stack.append(scene)
        scene.on_enter()

    def pop(self):
        if self._stack:
            old = self._stack.pop()
            old.on_exit()
            if self.current:
                self.current.on_enter()

    def switch(self, scene: Scene):
        """Replace the top scene (or push if stack is empty)."""
        if self._stack:
            old = self._stack.pop()
            old.on_exit()
        self._stack.append(scene)
        scene.on_enter()

    @property
    def is_empty(self) -> bool:
        return len(self._stack) == 0
