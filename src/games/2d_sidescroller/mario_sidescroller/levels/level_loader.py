"""Level loader — parse JSON level data into usable objects."""

import json
import os
from levels.tilemap import Tilemap


class Level:
    """Holds all data for a single game level."""

    def __init__(self, grid, player_spawn, enemy_spawns, coin_spawns,
                 question_blocks, level_name="1-1", flag_pos=None):
        self.tilemap = Tilemap(grid)
        self.player_spawn = tuple(player_spawn)
        self.enemy_spawns = enemy_spawns  # list of {"type": str, "x": int, "y": int}
        self.coin_spawns = coin_spawns    # list of [x, y]
        self.question_blocks = question_blocks  # list of {"col": int, "row": int, "item": str}
        self.level_name = level_name
        self.flag_pos = flag_pos  # [x, y] or None


def load_level(level_id: int) -> Level:
    """Load level data from levels/level_data/level_XX.json."""
    here = os.path.dirname(__file__)
    path = os.path.join(here, "level_data", f"level_{level_id:02d}.json")
    with open(path, "r") as f:
        data = json.load(f)
    return Level(
        grid=data["grid"],
        player_spawn=data.get("player_spawn", [64, 400]),
        enemy_spawns=data.get("enemy_spawns", []),
        coin_spawns=data.get("coin_spawns", []),
        question_blocks=data.get("question_blocks", []),
        level_name=data.get("level_name", f"{level_id}-1"),
        flag_pos=data.get("flag_pos"),
    )


def level_exists(level_id: int) -> bool:
    here = os.path.dirname(__file__)
    path = os.path.join(here, "level_data", f"level_{level_id:02d}.json")
    return os.path.isfile(path)
