"""Utilities for loading and scaling game image assets safely."""

from __future__ import annotations

from pathlib import Path

import pygame


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_ROOT = PROJECT_ROOT / "assets"


def loadScaledSprite(
    relativeAssetPath: str,
    targetSize: tuple[int, int],
    useWhiteColorKey: bool = False,
) -> pygame.Surface | None:
    """Load, optionally color-key, and scale an image asset.

    Returns None when loading fails so callers can fall back to
    rectangle rendering. This keeps the prototype robust even if an
    asset is missing on another collaborator's machine.
    """

    assetPath = ASSETS_ROOT / relativeAssetPath
    if not assetPath.exists():
        return None

    try:
        spriteSurface = pygame.image.load(str(assetPath)).convert_alpha()
    except (FileNotFoundError, pygame.error):
        return None

    if useWhiteColorKey:
        spriteSurface.set_colorkey((255, 255, 255))

    return pygame.transform.smoothscale(spriteSurface, targetSize)
