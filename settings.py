"""Central configuration values for the game prototype."""

from __future__ import annotations


# Window settings
WINDOW_TITLE = "HW7 - Fireboy & Watergirl Prototype"
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 60

# Grid and object sizing
TILE_SIZE = 32
PLAYER_WIDTH = 28
PLAYER_HEIGHT = 44

# Physics constants
GRAVITY_PER_FRAME = 0.6
MAX_FALL_SPEED = 14.0
DEFAULT_MOVEMENT_SPEED = 4.0
DEFAULT_JUMP_STRENGTH = 12.0

# UI spacing
HUD_PADDING = 12

# Input-independent gameplay settings
RESET_MESSAGE_DURATION_SECONDS = 1.8

# TODO: When level count grows, move the starting level key to a save/profile system.
STARTING_LEVEL_KEY = "starter_cavern"
