# pygame Mario-Style Sidescroller — Structured Build Prompt

Mario-Style Sidescroller · pygame · Python 3.12+

Keywords: Python, pygame, sidescroller, platformer, 2D physics, tile map, sprite, game loop


---


## Role

You are an IQ 160 Senior Python Game Engineer with deep mastery of the `pygame` library, including its rendering pipeline, event loop architecture, sprite groups, surface blitting, and clock-driven game loops. You excel at structuring clean, maintainable game architectures — separating concerns across scenes, entities, and state machines — while squeezing maximum performance from Python's runtime. You are fluent in collision detection strategies, tile map design, asset management, audio mixing, and input handling across keyboard, mouse, and gamepad peripherals.


---


## Objective

Build a fully playable Mario-style 2D sidescroller platformer using **Python 3.12+** and **pygame 2.x**. The game must be constructed **incrementally** — each phase below is a self-contained deliverable that compiles and runs before proceeding to the next phase. Do **not** skip ahead; complete and verify each phase in order.


---


## Constraints & Guardrails

| Constraint | Detail |
|---|---|
| **Language** | Python 3.12+ (no Cython, no C extensions) |
| **Engine** | `pygame` (and `pygame.math`, `pygame.sprite`) — no additional game frameworks |
| **Assets** | Generate placeholder art programmatically (colored rectangles / simple shapes) so the game is runnable without external asset files. Provide clear hooks (`ASSET_DIR`, loader functions) to swap in real sprites later. |
| **Resolution** | Logical resolution 800 × 600; support a scalable display surface for fullscreen toggle. |
| **Frame Rate** | Target 60 FPS via `pygame.time.Clock`; all movement and physics must be **delta-time aware** (`dt`). |
| **Architecture** | Scene-Manager pattern — every distinct screen (menu, gameplay, settings, game-over) is a `Scene` object managed by a central `SceneManager`. |
| **Project Structure** | Organize into a clean package layout (see Phase 0). No single-file monolith. |
| **No External Services** | Fully offline; no network calls, no cloud dependencies. |


---


## Project Structure (Target)

```
mario_sidescroller/
├── main.py                  # Entry point
├── requirements.txt         # pygame dependency
├── README.md                # Setup & run instructions
├── settings.py              # Global constants & user settings
├── engine/
│   ├── __init__.py
│   ├── scene_manager.py     # SceneManager & base Scene class
│   ├── camera.py            # Side-scrolling camera
│   ├── input_handler.py     # Unified keyboard/gamepad input
│   ├── asset_loader.py      # Sprite sheet & audio loader
│   └── physics.py           # Gravity, collision resolver
├── scenes/
│   ├── __init__.py
│   ├── title_screen.py      # Main menu / title
│   ├── gameplay.py          # Core gameplay scene
│   ├── settings_menu.py     # Settings overlay
│   ├── victory.py           # Victory screen
│   └── game_over.py         # Game-over screen
├── entities/
│   ├── __init__.py
│   ├── player.py            # Player character
│   ├── enemy.py             # Base enemy + subtypes
│   ├── collectible.py       # Coins, power-ups
│   └── particles.py         # Particle FX system
├── levels/
│   ├── __init__.py
│   ├── level_loader.py      # Parse level data → tile grid
│   ├── tilemap.py           # Tilemap rendering & collision
│   └── level_data/
│       ├── level_01.json    # Level 1 definition
│       └── level_02.json    # Level 2 definition
└── assets/
    ├── sprites/             # (placeholder or real PNGs)
    ├── audio/               # (placeholder or real WAV/OGG)
    └── fonts/               # (optional custom fonts)
```


---


## Phase 0 — Project Scaffolding & Game Loop Foundation

**Goal:** Establish the project skeleton, install dependencies, and prove a stable 60 FPS game loop renders to screen.

### Deliverables
1. Create the directory structure above with empty `__init__.py` stubs.
2. `requirements.txt` containing `pygame>=2.5`.
3. `settings.py` — define constants: `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `FPS`, `TILE_SIZE`, `GRAVITY`, `ASSET_DIR`.
4. `main.py` — initialize pygame, create the display surface, instantiate `SceneManager`, and run the core loop:
   ```
   while running:
       dt = clock.tick(FPS) / 1000.0
       handle_events()
       current_scene.update(dt)
       current_scene.draw(screen)
       pygame.display.flip()
   ```
5. `engine/scene_manager.py` — implement `Scene` (abstract base with `handle_event`, `update`, `draw`, `on_enter`, `on_exit`) and `SceneManager` (push/pop/switch).
6. Create a temporary `PlaceholderScene` that fills the screen with a solid color and prints FPS to the window title — confirm it runs.
7. `README.md` — document setup: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && python main.py`.

### Verification
- Window opens at 800×600, solid color renders, title bar shows ~60 FPS, clean quit on window close or ESC.


---


## Phase 1 — Input Handling

**Goal:** Centralized, remappable input system that decouples raw pygame events from game actions.

### Deliverables
1. `engine/input_handler.py` — define an `Action` enum: `LEFT`, `RIGHT`, `JUMP`, `RUN`, `PAUSE`, `CONFIRM`, `BACK`.
2. Map default keyboard bindings (Arrow keys + WASD, Space=Jump, LShift=Run, ESC=Pause, Enter=Confirm).
3. Support `is_pressed(action)` (held) and `is_just_pressed(action)` (single-frame trigger).
4. Provide a gamepad fallback: D-pad/left-stick for movement, A=Jump, B=Back, Start=Pause (if a joystick is detected).
5. Integrate `InputHandler` into the main loop so scenes receive it via `update(dt, input_handler)`.

### Verification
- Placeholder scene prints action names to console when keys/buttons are pressed and released.


---


## Phase 2 — Title Screen & Main Menu

**Goal:** A polished main menu scene with navigable options.

### Deliverables
1. `scenes/title_screen.py` — render:
   - Game title text (large, centered, with a gentle sine-wave bobbing animation).
   - Menu options: **Start Game**, **Settings**, **Quit** — highlight the selected option.
2. Navigation via UP/DOWN (or gamepad D-pad) to cycle options; CONFIRM to select; BACK or Quit option to exit.
3. Transitions: "Start Game" → push `GameplayScene`; "Settings" → push `SettingsMenuScene`; "Quit" → `pygame.quit()`.
4. Render a simple parallax-scrolling background (2–3 layers of colored rectangles moving at different speeds) to give visual life to the menu.

### Verification
- Menu renders, options are navigable, selections trigger correct scene transitions.


---


## Phase 3 — Settings Menu

**Goal:** An in-game settings overlay that persists user preferences.

### Deliverables
1. `scenes/settings_menu.py` — display adjustable options:
   - **Music Volume** (0–100 slider, ±10 with LEFT/RIGHT).
   - **SFX Volume** (0–100 slider).
   - **Fullscreen Toggle** (ON/OFF).
   - **Back** — return to previous scene.
2. Store settings in `settings.py` as a mutable dict; optionally serialize to `settings.json` for persistence across sessions.
3. Fullscreen toggle should call `pygame.display.set_mode()` with/without `FULLSCREEN` flag immediately.

### Verification
- Volume sliders update values displayed on screen; fullscreen toggles correctly; pressing Back returns to title.


---


## Phase 4 — Tilemap & Level Design System

**Goal:** Data-driven level loading with a tile-based collision grid.

### Deliverables
1. `levels/level_data/level_01.json` — define a level using a 2D grid of tile IDs:
   - `0` = air, `1` = ground, `2` = brick/breakable, `3` = question block, `4` = pipe, `5` = hazard (spikes/pit-marker).
   - Include `player_spawn` coordinates and `enemy_spawns` list.
   - Level width should be **at minimum 5× screen width** to require scrolling.
2. `levels/level_loader.py` — parse the JSON, return a `Level` object containing the tile grid, entity spawn points, and level dimensions.
3. `levels/tilemap.py`:
   - Render visible tiles only (camera-culled) using colored rectangles per tile type.
   - Expose `get_colliders_near(rect)` → returns a list of `pygame.Rect` for solid tiles overlapping the query area (spatial optimization).
4. Design `level_01` with: flat ground runway → small gap → elevated platforms → staircase → pipe/flagpole area.
5. Design `level_02` with: increased difficulty — moving platforms (defined as special tile entries), more gaps, more enemies.

### Verification
- Gameplay scene loads `level_01.json`, renders the tilemap, and the camera can be manually scrolled (temporary arrow-key camera panning) to see the full level.


---


## Phase 5 — Player Character & 2D Physics

**Goal:** A controllable player character with Mario-style physics.

### Deliverables
1. `entities/player.py` — `Player(pygame.sprite.Sprite)`:
   - Properties: `pos` (Vector2), `vel` (Vector2), `on_ground` (bool), `is_running`, `facing_right`, `lives`, `score`.
   - **Horizontal movement:** Acceleration-based (not instant velocity). Deceleration via friction when no input. Higher max speed when `RUN` is held.
   - **Jump:** Variable-height jump — apply upward impulse on JUMP press; cut vertical velocity short on JUMP release (like Mario's tap-vs-hold jump).
   - **Gravity:** Constant downward acceleration (`GRAVITY` from settings); terminal velocity cap.
   - **Coyote time:** Allow jump for ~80ms after walking off a ledge.
   - **Jump buffering:** Register a jump input ~100ms before landing and execute it on ground contact.
2. `engine/physics.py`:
   - `apply_gravity(entity, dt)`.
   - `resolve_tilemap_collisions(entity, tilemap, dt)` — sweep entity rect against solid tiles; resolve X and Y axes independently to prevent corner-clipping.
3. `engine/camera.py`:
   - Horizontal follow camera that tracks the player with slight look-ahead in the movement direction.
   - Clamp camera to level bounds (no rendering beyond level edges).
4. Integrate player into `GameplayScene`: spawn at `player_spawn`, update physics each frame, draw relative to camera offset.

### Verification
- Player runs and jumps across `level_01` with smooth acceleration, variable jump height, coyote time, and proper tilemap collision. Camera scrolls to follow.


---


## Phase 6 — Enemies & Collision Interactions

**Goal:** Introduce enemies with basic AI and player-enemy interaction.

### Deliverables
1. `entities/enemy.py` — base `Enemy(pygame.sprite.Sprite)`:
   - **Goomba-type:** Walks in one direction; reverses on wall collision or ledge detection (doesn't walk off edges).
   - **Koopa-type:** Same patrol behavior; when stomped, becomes a shell that slides and can hit other enemies.
2. Spawn enemies from `enemy_spawns` in level data; add them to a `pygame.sprite.Group`.
3. **Player ↔ Enemy collision:**
   - Player lands on top (player `vel.y > 0` and player bottom overlaps enemy top half) → enemy is defeated, player bounces upward.
   - Player collides from side or below → player takes damage (lose a life, brief invincibility flash for ~2 seconds).
4. **Enemy ↔ Tilemap collision:** Enemies obey gravity and resolve tile collisions identically to the player.
5. Enemies that scroll off-screen beyond a threshold behind the camera are despawned to save resources.

### Verification
- Goomba patrols a platform, reverses at edges. Player can stomp to defeat or get hit from the side. Koopa shell slides and defeats other enemies on contact.


---


## Phase 7 — Collectibles & HUD / User Interface

**Goal:** Coins, power-ups, score tracking, and an on-screen HUD.

### Deliverables
1. `entities/collectible.py`:
   - **Coin:** Static sprite; collected on player overlap → increment score, play SFX, spawn sparkle particle.
   - **Mushroom (Power-Up):** Emerges from question-block when hit from below; moves horizontally. On collection → player grows (double height hitbox), can take one extra hit before shrinking.
   - **Star (Invincibility):** Bouncing collectible; grants ~8 seconds of invincibility (player flashes rainbow, enemies defeated on contact).
2. **Question Block interaction:** When player headbutts a `?` block tile from below → block becomes "used" (visual change), spawns its designated collectible above.
3. **HUD overlay** (drawn on top of gameplay, not affected by camera):
   - Top-left: `SCORE: 00000` and coin icon with coin count.
   - Top-center: `WORLD 1-1` (level identifier).
   - Top-right: `LIVES: 3` with small player icon.
   - Optional: Countdown timer.
4. Animate score pop-ups (floating `+100`, `+200` text) at the collection point that drift upward and fade.

### Verification
- Coins collectible, score increments, HUD updates in real time. Question blocks spawn mushrooms/coins on headbutt. Mushroom power-up changes player state.


---


## Phase 8 — Victory & Game Over Conditions

**Goal:** Define clear win/lose states and corresponding scenes.

### Deliverables
1. **Victory condition:** Player reaches the flagpole/pipe at the end of the level → trigger a brief celebration (player auto-walks to flag, score tallies up) → transition to `VictoryScene`.
2. `scenes/victory.py`:
   - Display "LEVEL COMPLETE!" with final score and time bonus.
   - Options: **Next Level** (load next level JSON) or **Main Menu**.
3. **Game Over triggers:**
   - Player `lives` reaches 0.
   - Player falls below the level floor (pit death) → instant life loss, respawn at last checkpoint or level start if lives remain.
4. `scenes/game_over.py`:
   - Display "GAME OVER" with final score.
   - Options: **Retry** (restart current level with fresh lives) or **Main Menu**.
5. **Life loss sequence:** Brief death animation (player tumbles off-screen), 1-second pause, respawn.

### Verification
- Reaching end of level triggers victory flow and score tally. Dying to enemy/pit decrements lives; zero lives shows Game Over. Both screens offer correct navigation options.


---


## Phase 9 — Level Transitions & Scene Flow

**Goal:** Smooth transitions between levels and scenes.

### Deliverables
1. **Fade transition:** Implement a reusable `FadeTransition` utility — renders a black overlay with alpha ramping from 0→255 (fade out) then 255→0 (fade in) over ~0.5 seconds each.
2. Apply fade transitions on every scene switch (title → gameplay, level end → victory, game over → title, etc.).
3. **Level progression:** `GameplayScene` accepts a `level_id` parameter; on victory, `SceneManager` loads `GameplayScene(level_id + 1)`. If no more levels exist, show a "Congratulations — You Win!" final screen.
4. **Pipe warp (bonus):** Player pressing DOWN on a designated pipe tile → pipe-enter animation (player sinks into pipe) → fade → load a bonus room or skip to a later section of the level → pipe-exit animation.

### Verification
- Scene transitions fade smoothly rather than hard-cutting. Completing level 1 loads level 2. Pipe warps function if implemented.


---


## Phase 10 — Particle Effects

**Goal:** Lightweight particle system for visual juice.

### Deliverables
1. `entities/particles.py` — `ParticleEmitter` class:
   - Maintains a list of particle dicts: `{pos, vel, color, lifetime, size}`.
   - `emit(pos, count, color, spread, speed, lifetime)` — burst spawn.
   - `update(dt)` — move particles, shrink size, decrement lifetime, remove dead.
   - `draw(surface, camera_offset)` — render as small circles or 1–3px rects.
2. Apply particles to:
   - **Coin collection:** Gold sparkle burst.
   - **Enemy stomp:** Small puff of smoke/dust.
   - **Brick break:** Brick-colored fragments fly outward with gravity.
   - **Player landing:** Subtle dust puff when hitting the ground from a fall.
   - **Death:** Red/white burst at player position.
3. Keep particle counts reasonable (cap at ~200 alive at once) to maintain 60 FPS.

### Verification
- Stomping an enemy, collecting a coin, and breaking a brick each produce distinct particle bursts. No frame rate drop.


---


## Phase 11 — Audio & Music

**Goal:** Sound effects and background music with volume control tied to Settings.

### Deliverables
1. `engine/asset_loader.py` — add `load_sound(name)` and `load_music(name)` helpers that look in `assets/audio/`.
2. **Generate placeholder audio** programmatically using `pygame.sndarray` or `numpy` (sine wave blips) so the game runs without external WAV files. Document how to replace with real audio assets.
3. **Sound effects** (short clips via `pygame.mixer.Sound`):
   - `jump.wav`, `coin.wav`, `stomp.wav`, `powerup.wav`, `damage.wav`, `death.wav`, `brick_break.wav`, `pause.wav`, `menu_select.wav`, `victory.wav`.
4. **Background music** (looped via `pygame.mixer.music`):
   - Title screen music, gameplay music, victory jingle, game-over jingle.
   - Use `pygame.mixer.music.set_volume()` tied to the Settings music volume value.
5. SFX volume controlled globally via a multiplier applied when calling `sound.set_volume()`.
6. Music crossfades or stops cleanly on scene transitions (no abrupt cuts).

### Verification
- Jumping, collecting coins, stomping enemies, and dying all trigger distinct sounds. Background music plays and loops. Volume sliders in Settings control levels in real time.


---


## Phase 12 — Polish, Playtesting & README

**Goal:** Final integration pass, bug fixes, and documentation.

### Deliverables
1. **Playtest** both levels end-to-end. Fix any collision bugs, physics edge cases, or scene transition glitches.
2. **Performance check:** Profile with `cProfile` or in-game FPS counter. Optimize any hot spots (tilemap rendering, particle updates, sprite group draws).
3. **Edge cases:**
   - Resizing/fullscreen doesn't break layout.
   - Pausing mid-jump doesn't corrupt physics state.
   - Collecting the last coin in a level doesn't crash.
   - Rapid scene switching (mashing Confirm/Back) doesn't stack-overflow the scene manager.
4. **README.md** — comprehensive setup and play guide:
   - Prerequisites (Python 3.12+, pip).
   - Installation steps (`venv`, `pip install`, `python main.py`).
   - Controls reference table (keyboard + gamepad).
   - How to add custom levels (JSON format documentation).
   - How to replace placeholder assets with real sprites/audio.
   - Screenshots or ASCII diagrams of gameplay.
5. Add inline code comments explaining non-obvious logic (physics resolution order, coyote time implementation, variable jump mechanics).

### Verification
- Game is fully playable from title screen through both levels to victory/game-over. No crashes. README enables a new developer to clone, install, and play within 2 minutes.


---


## Summary — Phase Execution Order

| Phase | Name | Key Deliverable |
|-------|------|-----------------|
| 0 | Scaffolding & Game Loop | Project structure, 60 FPS loop, SceneManager |
| 1 | Input Handling | Remappable action-based input system |
| 2 | Title Screen | Animated main menu with navigation |
| 3 | Settings Menu | Volume, fullscreen, persistence |
| 4 | Tilemap & Level Design | JSON-driven levels, spatial tile collision |
| 5 | Player & Physics | Acceleration, variable jump, coyote time, camera |
| 6 | Enemies | Patrol AI, stomp/damage interactions |
| 7 | Collectibles & HUD | Coins, power-ups, question blocks, score display |
| 8 | Victory & Game Over | Win/lose conditions, screens, life system |
| 9 | Level Transitions | Fade transitions, level progression, pipe warps |
| 10 | Particle Effects | Dust, sparkles, brick fragments |
| 11 | Audio & Music | SFX, BGM, volume integration |
| 12 | Polish & README | Playtesting, optimization, documentation |

> **Reminder:** Each phase must compile and run successfully before moving to the next. Do not stub out future phases — build iteratively on working code.
