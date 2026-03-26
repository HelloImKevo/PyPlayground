"""Global constants and user settings for the Mario-style sidescroller."""

import os

# Display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Tile / Physics
TILE_SIZE = 32
GRAVITY = 1200  # pixels/sec^2
TERMINAL_VELOCITY = 800  # pixels/sec

# Asset paths
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")

# Player defaults
PLAYER_ACCEL = 600       # horizontal acceleration px/s^2
PLAYER_FRICTION = 500    # deceleration when no input px/s^2
PLAYER_MAX_SPEED = 220   # normal max horizontal speed px/s
PLAYER_RUN_MAX_SPEED = 360
PLAYER_JUMP_IMPULSE = -450  # upward velocity on jump
PLAYER_JUMP_CUT = -150     # velocity capped to this on jump release
COYOTE_TIME = 0.08         # seconds
JUMP_BUFFER_TIME = 0.10    # seconds

# Player stats
PLAYER_START_LIVES = 3
INVINCIBILITY_DURATION = 2.0  # seconds after getting hit

# Enemies
ENEMY_SPEED = 60  # px/s
STOMP_BOUNCE = -300  # upward velocity on stomp

# Collectibles
COIN_SCORE = 100
MUSHROOM_SCORE = 1000
STAR_DURATION = 8.0  # seconds

# Mutable runtime settings
user_settings = {
    "music_volume": 70,
    "sfx_volume": 70,
    "fullscreen": False,
}
