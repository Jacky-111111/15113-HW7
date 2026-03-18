"""Simple physics helper functions for axis-aligned platformer movement."""

from __future__ import annotations

from collections.abc import Iterable

import pygame

from game.objects import Platform


def move_rect_with_platform_collisions(
    currentRect: pygame.Rect,
    horizontalVelocity: float,
    verticalVelocity: float,
    platforms: Iterable[Platform],
) -> tuple[pygame.Rect, bool]:
    """Move an entity and resolve collisions against static platforms.

    Returns:
        A tuple of:
        - updated rectangle after horizontal and vertical collision resolution
        - grounded flag indicating whether the entity stands on a platform
    """

    movedRect = currentRect.copy()
    isOnGround = False

    movedRect.x += int(horizontalVelocity)
    for platform in platforms:
        if not movedRect.colliderect(platform.rect):
            continue
        if horizontalVelocity > 0:
            movedRect.right = platform.rect.left
        elif horizontalVelocity < 0:
            movedRect.left = platform.rect.right

    movedRect.y += int(verticalVelocity)
    for platform in platforms:
        if not movedRect.colliderect(platform.rect):
            continue
        if verticalVelocity > 0:
            movedRect.bottom = platform.rect.top
            isOnGround = True
        elif verticalVelocity < 0:
            movedRect.top = platform.rect.bottom

    return movedRect, isOnGround


# TODO: Add swept AABB support if higher movement speeds cause tunneling.
