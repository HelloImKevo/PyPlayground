# Mario-Style 2D Sidescroller

A fully playable Mario-style 2D platformer built with **Python 3.12+** and **pygame 2.x**.

## Setup & Run

```bash
cd mario_sidescroller
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt
python main.py
```

## Controls

| Action       | Keyboard            | Gamepad         |
|-------------|---------------------|-----------------|
| Move Left   | Left Arrow / A      | D-pad Left      |
| Move Right  | Right Arrow / D     | D-pad Right     |
| Jump        | Space               | A Button        |
| Run         | Left Shift          | —               |
| Pause       | Escape              | Start           |
| Confirm     | Enter               | Start           |
| Back        | Backspace           | B Button        |

### Jump Mechanics
- **Tap** Space for a short hop; **hold** Space for a full jump.
- **Coyote time**: You can still jump briefly after walking off an edge.
- **Jump buffering**: Press jump slightly before landing and it will trigger on contact.

## Game Structure

- **Title Screen** — Start Game, Settings, Quit
- **Settings** — Music/SFX volume, fullscreen toggle
- **Gameplay** — Run, jump, stomp enemies, collect coins, hit ? blocks
- **Victory** — Reach the flagpole at the end of each level
- **Game Over** — Lose all lives; retry or return to menu

## Levels

Levels are defined as JSON files in `levels/level_data/`. Tile IDs:

| ID | Type             |
|----|------------------|
| 0  | Air              |
| 1  | Ground (solid)   |
| 2  | Brick (solid)    |
| 3  | Question Block   |
| 4  | Pipe (solid)     |
| 5  | Hazard           |
| 6  | Used ? block     |
| 7  | Pipe top         |
| 8  | Flagpole         |
| 9  | Flag base        |

### Adding Custom Levels

1. Create `levels/level_data/level_03.json` (follow the pattern of level_01/02).
2. Define a 2D grid array, `player_spawn`, `enemy_spawns`, `coin_spawns`, `question_blocks`, and `flag_pos`.
3. The game will auto-chain to level 3 after completing level 2.

## Replacing Placeholder Assets

All art is currently rendered as colored shapes. To use real sprites:

1. Place PNG files in `assets/sprites/`.
2. Use `engine/asset_loader.load_image("filename.png")` in entity draw methods.
3. Place WAV/OGG audio files in `assets/audio/`.
4. Use `engine/asset_loader.load_sound("jump.wav")` to load sound effects.

## Project Structure

```
mario_sidescroller/
├── main.py              # Entry point
├── settings.py          # Constants & runtime config
├── engine/              # Core systems (scene manager, camera, input, physics)
├── scenes/              # Title, gameplay, settings, victory, game over
├── entities/            # Player, enemies, collectibles, particles
├── levels/              # Level loader, tilemap, JSON level data
└── assets/              # Placeholder directories for sprites, audio, fonts
```
