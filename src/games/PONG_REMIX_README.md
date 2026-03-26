# Pong Remix — Environment Setup

This document covers exactly how to set up your environment and run **Pong Remix**
(`src/games/pong_remix.py`).

---

## What's in the Box

A full 60 FPS Pong game built on `pygame` with these twists beyond vanilla Pong:

| Twist | Description |
|---|---|
| **Power-ups** | 5 types spawn randomly on the field — hit them with the ball to activate: **BIG** (enlarge your paddle), **SHR** (shrink opponent), **FIR** (fireball speed boost), **MUL** (spawn an extra ball), **CRV** (sine-wave curve ball) |
| **Spin mechanic** | Moving your paddle while hitting the ball imparts spin, curving the ball's trajectory |
| **Rally acceleration** | Ball speed increases with each consecutive hit in a rally |
| **Particle effects** | Colour-shifting ball trails, hit bursts, and goal confetti |
| **Screen shake** | Impact shake on every goal scored |
| **Multi-ball** | The MUL power-up splits the ball — all balls are live simultaneously |
| **Adaptive AI** | AI difficulty scales dynamically based on the score difference |
| **Synthesised audio** | Hit, wall, goal, and power-up sounds generated in code — no asset files needed |

---

## Prerequisites

| Requirement | Minimum Version | Notes |
|---|---|---|
| **Python** | 3.9+ | Tested on 3.13.4. Any 3.9+ should work. |
| **pygame** | 2.x | Tested on 2.6.1 (SDL 2.28.4). |
| **macOS / Linux / Windows** | — | Cross-platform; no native dependencies beyond SDL (bundled with pygame wheels). |

No external asset files (images, fonts, sounds) are needed — everything is
generated in code.

---

## Step-by-step Setup

### 1. Create a virtual environment

From the repository root (`PyPlayground/`):

```bash
python3 -m venv .venv
```

> **Why a venv?** The repo's older `venv/` directory and `requirements.txt`
> target a system-wide install. A local `.venv` keeps Pong Remix's dependency
> (`pygame`) isolated and reproducible.

### 2. Activate the virtual environment

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (cmd)
.venv\Scripts\activate.bat
```

Your prompt should now show `(.venv)`.

### 3. Install pygame

```bash
pip install pygame
```

This pulls in a pre-built wheel that bundles SDL2, so no separate SDL
installation is required on any major OS.

> **Tip:** You can also install everything the repo needs at once:
> ```bash
> pip install -r requirements.txt
> ```

### 4. Verify the installation

```bash
python -c "import pygame; print('pygame', pygame.ver)"
```

Expected output (version may differ):

```
pygame 2.6.1 (SDL 2.28.4, Python 3.13.4)
Hello from the pygame community. https://www.pygame.org/contribute.html
pygame 2.6.1
```

### 5. Run the game

```bash
# From the repository root
python src/games/pong_remix.py

# Or as a module
python -m src.games.pong_remix
```

A 960×640 window should open showing the Pong Remix title screen.

---

## Troubleshooting

| Symptom | Cause & Fix |
|---|---|
| `ModuleNotFoundError: No module named 'pygame'` | pygame is not installed in the active environment. Run `pip install pygame` inside your activated venv. |
| Window opens but is completely black / unresponsive | On macOS with certain Python builds (e.g., pyenv), you may need the "framework" build. Try `brew install python` or use the official python.org installer. |
| `pygame.error: No available video device` | You're running over SSH or in a headless container. pygame requires a display. Use X11 forwarding (`ssh -X`) or a virtual framebuffer (`Xvfb`). |
| `ImportError: ... SDL ...` | Rare on modern pip (wheels bundle SDL). If you're building from source, install SDL2 dev libs: `brew install sdl2` (macOS) or `sudo apt install libsdl2-dev` (Debian/Ubuntu). |
| Slow / choppy frame rate | Ensure you're not running inside a VM without GPU passthrough. pygame uses software rendering by default and should comfortably hit 60 FPS on bare metal. |

---

## Controls Quick Reference

| Input | Action |
|---|---|
| **W / S** | Player 1 paddle up / down |
| **M** (at menu) | Toggle mouse control for Player 1 |
| **Up / Down arrows** | Player 2 paddle (2-player mode) |
| **TAB + ENTER** (at menu) | Start in 2-player mode |
| **ENTER** | Start / restart game |
| **ESC** | Return to menu / quit |

---

## What Was Done During Initial Setup

For reference, here's the exact sequence that was followed to get the game
running the first time on a macOS machine:

1. **Configured the Python environment** — the workspace already had a
   `.venv` virtual environment with Python 3.13.4.
2. **Installed pygame** — `pip install pygame` pulled in `pygame 2.6.1`
   with bundled SDL 2.28.4.  The package was already listed in the repo's
   `requirements.txt` but had not been installed in the `.venv`.
3. **Syntax-checked the source** — `python -m py_compile src/games/pong_remix.py`
   passed cleanly on the first attempt.  No compilation or import errors
   were encountered.
4. **Confirmed the import** — `python -c "import pygame; print(pygame.ver)"`
   printed `2.6.1`, confirming the library loads without issues.

No patches, workarounds, or additional system-level dependencies were needed
beyond `pip install pygame`.
