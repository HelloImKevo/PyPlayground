"""Asset loader helpers for sprites, sounds, and music."""

import array
import math
import os
import pygame
from settings import ASSET_DIR


def _asset_path(*parts: str) -> str:
    return os.path.join(ASSET_DIR, *parts)


def load_image(name: str, scale: tuple[int, int] | None = None) -> pygame.Surface:
    """Load an image from assets/sprites/. Returns a placeholder if missing."""
    path = _asset_path("sprites", name)
    if os.path.isfile(path):
        img = pygame.image.load(path).convert_alpha()
    else:
        # Placeholder: 32×32 magenta rect
        w, h = scale or (32, 32)
        img = pygame.Surface((w, h), pygame.SRCALPHA)
        img.fill((255, 0, 255))
    if scale:
        img = pygame.transform.scale(img, scale)
    return img


def load_sound(name: str) -> pygame.mixer.Sound | None:
    """Load a WAV/OGG from assets/audio/. Returns None if missing."""
    path = _asset_path("audio", name)
    if os.path.isfile(path):
        return pygame.mixer.Sound(path)
    return None


def load_music(name: str) -> bool:
    """Queue a music file for streaming. Returns True if file exists."""
    path = _asset_path("audio", name)
    if os.path.isfile(path):
        pygame.mixer.music.load(path)
        return True
    return False


def generate_tone(frequency: float = 440.0, duration: float = 0.15,
                  volume: float = 0.3, sample_rate: int = 22050) -> pygame.mixer.Sound:
    """Generate a simple sine-wave tone as a pygame Sound object."""
    n_samples = int(sample_rate * duration)
    buf = array.array("h", [0] * n_samples)
    max_amp = int(32767 * volume)
    for i in range(n_samples):
        t = i / sample_rate
        # Fade out over last 20% for a clean tail
        env = min(1.0, (n_samples - i) / (n_samples * 0.2))
        buf[i] = int(max_amp * env * math.sin(2 * math.pi * frequency * t))
    return pygame.mixer.Sound(buffer=buf)


# ------------------------------------------------------------------
# Pre-built placeholder sounds (created on first access)
# ------------------------------------------------------------------
_placeholder_cache: dict[str, pygame.mixer.Sound] = {}

_PLACEHOLDER_DEFS: dict[str, tuple[float, float, float]] = {
    # name: (frequency_hz, duration_s, volume)
    "jump":        (520, 0.12, 0.25),
    "coin":        (880, 0.08, 0.2),
    "stomp":       (200, 0.10, 0.25),
    "powerup":     (660, 0.30, 0.2),
    "damage":      (180, 0.25, 0.3),
    "death":       (120, 0.50, 0.3),
    "brick_break": (300, 0.10, 0.2),
    "pause":       (440, 0.08, 0.15),
    "menu_select": (600, 0.06, 0.15),
    "victory":     (784, 0.40, 0.25),
}


def get_sound(name: str) -> pygame.mixer.Sound | None:
    """Get a sound by name: loads from file first, falls back to generated tone."""
    snd = load_sound(f"{name}.wav") or load_sound(f"{name}.ogg")
    if snd:
        return snd
    if name in _placeholder_cache:
        return _placeholder_cache[name]
    if name in _PLACEHOLDER_DEFS:
        freq, dur, vol = _PLACEHOLDER_DEFS[name]
        snd = generate_tone(freq, dur, vol)
        _placeholder_cache[name] = snd
        return snd
    return None
