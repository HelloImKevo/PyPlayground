"""Unified keyboard / gamepad input handler."""

import enum
import pygame


class Action(enum.Enum):
    LEFT = "left"
    RIGHT = "right"
    JUMP = "jump"
    RUN = "run"
    PAUSE = "pause"
    CONFIRM = "confirm"
    BACK = "back"
    UP = "up"
    DOWN = "down"


# Default keyboard bindings: key -> action
_DEFAULT_KEYS: dict[int, Action] = {
    pygame.K_LEFT: Action.LEFT,
    pygame.K_a: Action.LEFT,
    pygame.K_RIGHT: Action.RIGHT,
    pygame.K_d: Action.RIGHT,
    pygame.K_UP: Action.UP,
    pygame.K_w: Action.UP,
    pygame.K_DOWN: Action.DOWN,
    pygame.K_s: Action.DOWN,
    pygame.K_SPACE: Action.JUMP,
    pygame.K_LSHIFT: Action.RUN,
    pygame.K_ESCAPE: Action.PAUSE,
    pygame.K_RETURN: Action.CONFIRM,
    pygame.K_BACKSPACE: Action.BACK,
}

# Gamepad button mapping (Xbox-style)
_DEFAULT_BUTTONS: dict[int, Action] = {
    0: Action.JUMP,      # A
    1: Action.BACK,      # B
    6: Action.PAUSE,     # Start
    7: Action.CONFIRM,   # Select / Back on some pads
}


class InputHandler:
    """Tracks held and just-pressed actions each frame."""

    def __init__(self):
        self._pressed: set[Action] = set()
        self._just_pressed: set[Action] = set()
        self._just_released: set[Action] = set()
        self._prev_pressed: set[Action] = set()
        self.key_map = dict(_DEFAULT_KEYS)
        self.button_map = dict(_DEFAULT_BUTTONS)
        self._joystick: pygame.joystick.Joystick | None = None
        self._init_joystick()

    # ------------------------------------------------------------------
    def _init_joystick(self):
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self._joystick = pygame.joystick.Joystick(0)
            self._joystick.init()

    # ------------------------------------------------------------------
    def begin_frame(self):
        """Call at the start of the frame BEFORE processing events."""
        self._just_pressed.clear()
        self._just_released.clear()

    def process_event(self, event: pygame.event.Event):
        """Feed each pygame event here."""
        if event.type == pygame.KEYDOWN:
            action = self.key_map.get(event.key)
            if action:
                self._pressed.add(action)
                self._just_pressed.add(action)
        elif event.type == pygame.KEYUP:
            action = self.key_map.get(event.key)
            if action:
                self._pressed.discard(action)
                self._just_released.add(action)
        elif event.type == pygame.JOYBUTTONDOWN:
            action = self.button_map.get(event.button)
            if action:
                self._pressed.add(action)
                self._just_pressed.add(action)
        elif event.type == pygame.JOYBUTTONUP:
            action = self.button_map.get(event.button)
            if action:
                self._pressed.discard(action)
                self._just_released.add(action)
        # Gamepad hat (D-pad)
        elif event.type == pygame.JOYHATMOTION and self._joystick:
            hat = event.value
            for act in (Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN):
                self._pressed.discard(act)
            if hat[0] < 0:
                self._pressed.add(Action.LEFT)
                self._just_pressed.add(Action.LEFT)
            elif hat[0] > 0:
                self._pressed.add(Action.RIGHT)
                self._just_pressed.add(Action.RIGHT)
            if hat[1] > 0:
                self._pressed.add(Action.UP)
                self._just_pressed.add(Action.UP)
            elif hat[1] < 0:
                self._pressed.add(Action.DOWN)
                self._just_pressed.add(Action.DOWN)

    # ------------------------------------------------------------------
    def is_pressed(self, action: Action) -> bool:
        """True while the action key/button is held."""
        return action in self._pressed

    def is_just_pressed(self, action: Action) -> bool:
        """True only on the frame the action was first pressed."""
        return action in self._just_pressed

    def is_just_released(self, action: Action) -> bool:
        """True only on the frame the action was released."""
        return action in self._just_released
