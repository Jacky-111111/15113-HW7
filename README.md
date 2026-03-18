# CMU 15-113 HW7 - Fireboy/Watergirl Starter Prototype

This repository is the **game/project option** for HW7: a collaboration-friendly Python prototype inspired by Fireboy and Watergirl.

It intentionally focuses on a clean architecture and one playable vertical slice, not a polished full clone.

## What This Builds (Phase 1)

A small two-player 2D platformer prototype using Pygame:
- Two controllable characters (Fireboy and Watergirl)
- Gravity, jumping, and platform collisions
- Typed hazards (fire, water, toxic)
- Typed exits (fire exit, water exit)
- Win condition that requires both players to reach matching exits
- Manual and automatic reset behavior

## Intentionally Unfinished

The following are intentionally left for future phases:
- Sprite art and animation systems
- Moving platforms, buttons/levers, and doors
- Multi-level progression and level select
- Audio and polish effects
- Collectibles (diamonds) and scoring

This is deliberate so teammates can extend from a stable and readable base.

## Project Structure

```text
15113-HW7/
  README.md
  requirements.txt
  main.py
  settings.py
  colors.py
  game/
    __init__.py
    game_manager.py
    level.py
    player.py
    objects.py
    physics.py
    ui.py
  assets/
    .gitkeep
```

## Setup

### Python Version

Use Python 3.10+ (3.11 recommended).

### Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

### Run the Game

```bash
python3 main.py
```

## Controls

### Fireboy
- `A`: Move left
- `D`: Move right
- `W`: Jump

### Watergirl
- `Left Arrow`: Move left
- `Right Arrow`: Move right
- `Up Arrow`: Jump

### Shared
- `R`: Restart/reset level

## Current Features

- Fixed-size game window and stable frame update loop
- Clear update/draw structure in `GameManager`
- Two independent players with separate controls
- Grounded jump rules (no intentional double-jump)
- Axis-aligned platform collision resolution
- Hazard immunity rules:
  - Fireboy is safe in fire, dies in water/toxic
  - Watergirl is safe in water, dies in fire/toxic
- Exit rules:
  - Fireboy must stand in fire exit
  - Watergirl must stand in water exit
  - Win only when both conditions are true at the same time
- One sample level that is easy to edit in code

## Unfinished / Future Work (Suggested Next Steps)

- TODO: Add moving platform support in `game/physics.py` and `game/player.py`.
- TODO: Replace rectangle placeholders with sprite assets after mechanics stabilize.
- TODO: Move level definitions from `game/level.py` to external JSON files.
- TODO: Add additional levels and a small level-loading progression system.
- TODO: Add coyote time / jump buffering for better feel.
- TODO: Add start and win screens with cleaner UX flow.

## Design Decisions

- **Modular files over one giant script:**  
  `game_manager.py`, `player.py`, `level.py`, `physics.py`, and `ui.py` separate concerns so teammates can edit one subsystem without touching unrelated logic.

- **Simple in-code level format:**  
  The starter level uses readable dictionaries/lists in `game/level.py`. This keeps iteration fast for early HW development and avoids premature tooling complexity.

- **Rectangle placeholder graphics:**  
  Colored rectangles keep gameplay debugging straightforward. This helps validate collision and rules before art integration.

- **Explicit naming and docstrings:**  
  The code favors readability (`horizontalVelocity`, `hasReachedExit`, `resetLevel`) so a collaborator can understand intent quickly.

## Prompt Log

This section records the main AI-assisted prompts used for Phase 1.

### Entry 1
- **Tool/Model Used:** Cursor with GPT-based coding assistant
- **Purpose:** Create a collaboration-first Python + Pygame starter architecture
- **Key Prompt Summary:** Requested a multi-file Fireboy/Watergirl-inspired prototype with clear responsibilities, descriptive naming, docstrings, TODOs, and a strong handoff README.

### Entry 2
- **Tool/Model Used:** Cursor planning + implementation workflow
- **Purpose:** Convert requirements into an actionable build plan, then implement a playable vertical slice
- **Key Prompt Summary:** Prioritized structure first, then minimum viable gameplay (movement, collision, typed hazards, typed exits, reset, one sample level), while avoiding overengineering.

## Collaboration Notes

If you are the next teammate:
- Start with `game/game_manager.py` to understand runtime flow.
- Tweak `STARTER_LEVEL_DEFINITION` in `game/level.py` first when testing mechanics.
- Keep constants in `settings.py` to avoid magic numbers.
- Add new mechanics behind clear TODO markers and docstrings so future handoffs stay smooth.