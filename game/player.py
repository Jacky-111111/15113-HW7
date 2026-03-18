"""Player entity logic for movement, hazards, and exit checks."""

from __future__ import annotations

from collections.abc import Iterable

import pygame

import settings
from game.objects import ExitDoor, Hazard, Platform
from game.physics import move_rect_with_platform_collisions


class Player:
    """A controllable platformer character (fire or water)."""

    def __init__(
        self,
        playerName: str,
        playerType: str,
        color: tuple[int, int, int],
        spawnPosition: tuple[int, int],
        moveLeftKey: int,
        moveRightKey: int,
        jumpKey: int,
    ) -> None:
        self.playerName = playerName
        self.playerType = playerType
        self.color = color
        self.spawnPosition = spawnPosition

        self.moveLeftKey = moveLeftKey
        self.moveRightKey = moveRightKey
        self.jumpKey = jumpKey

        self.rect = pygame.Rect(
            spawnPosition[0],
            spawnPosition[1],
            settings.PLAYER_WIDTH,
            settings.PLAYER_HEIGHT,
        )

        self.horizontalVelocity = 0.0
        self.verticalVelocity = 0.0
        self.movementSpeed = settings.DEFAULT_MOVEMENT_SPEED
        self.jumpStrength = settings.DEFAULT_JUMP_STRENGTH

        self.isOnGround = False
        self.isAlive = True
        self.hasReachedExit = False

    def resetToSpawn(self) -> None:
        """Reset transient player state after death or manual restart."""
        self.rect.topleft = self.spawnPosition
        self.horizontalVelocity = 0.0
        self.verticalVelocity = 0.0
        self.isOnGround = False
        self.isAlive = True
        self.hasReachedExit = False

    def processInput(self, pressedKeys: pygame.key.ScancodeWrapper) -> None:
        """Read controls and update desired movement values."""
        self.horizontalVelocity = 0.0
        if pressedKeys[self.moveLeftKey]:
            self.horizontalVelocity -= self.movementSpeed
        if pressedKeys[self.moveRightKey]:
            self.horizontalVelocity += self.movementSpeed

        # Jump is only allowed when grounded to keep behavior predictable.
        if pressedKeys[self.jumpKey] and self.isOnGround:
            self.verticalVelocity = -self.jumpStrength
            self.isOnGround = False

    def applyGravity(self) -> None:
        """Apply gravity with a terminal fall speed."""
        self.verticalVelocity += settings.GRAVITY_PER_FRAME
        if self.verticalVelocity > settings.MAX_FALL_SPEED:
            self.verticalVelocity = settings.MAX_FALL_SPEED

    def updateMovement(self, platforms: Iterable[Platform]) -> None:
        """Apply physics and resolve collisions against solid platforms."""
        self.applyGravity()
        newRect, isOnGround = move_rect_with_platform_collisions(
            self.rect,
            self.horizontalVelocity,
            self.verticalVelocity,
            platforms,
        )
        if isOnGround and self.verticalVelocity > 0:
            self.verticalVelocity = 0
        if not isOnGround and self.isOnGround:
            # TODO: Consider adding coyote time for forgiving jump windows.
            pass
        self.rect = newRect
        self.isOnGround = isOnGround

    def _isHazardDeadly(self, hazardType: str) -> bool:
        """Return True when this player should die from a hazard type."""
        if hazardType == "toxic":
            return True
        if hazardType == "fire":
            return self.playerType != "fire"
        if hazardType == "water":
            return self.playerType != "water"
        return False

    def checkHazardCollision(self, hazards: Iterable[Hazard]) -> bool:
        """Return True when colliding with a deadly hazard."""
        for hazard in hazards:
            if self.rect.colliderect(hazard.rect) and self._isHazardDeadly(hazard.hazardType):
                self.isAlive = False
                return True
        return False

    def updateExitStatus(self, exits: Iterable[ExitDoor]) -> None:
        """Mark whether this player is currently in their matching exit."""
        self.hasReachedExit = False
        for exitDoor in exits:
            if exitDoor.exitType == self.playerType and self.rect.colliderect(exitDoor.rect):
                self.hasReachedExit = True
                break

    def draw(self, surface: pygame.Surface) -> None:
        """Draw a simple placeholder rectangle for this character."""
        pygame.draw.rect(surface, self.color, self.rect)
