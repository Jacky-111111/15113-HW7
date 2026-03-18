"""High-level gameplay orchestration and state management."""

from __future__ import annotations

import pygame

import colors
import settings
from game.assets import loadScaledSprite
from game.level import Level, loadStarterLevel
from game.player import Player
from game.ui import GameUI


class GameManager:
    """Coordinates level state, player updates, reset behavior, and drawing."""

    def __init__(self) -> None:
        self.level: Level = loadStarterLevel()
        self.ui = GameUI()

        self.fireboy = Player(
            playerName="Fireboy",
            playerType="fire",
            color=colors.FIREBOY_COLOR,
            spawnPosition=self.level.spawnPositions["fire"],
            moveLeftKey=pygame.K_a,
            moveRightKey=pygame.K_d,
            jumpKey=pygame.K_w,
        )
        self.watergirl = Player(
            playerName="Watergirl",
            playerType="water",
            color=colors.WATERGIRL_COLOR,
            spawnPosition=self.level.spawnPositions["water"],
            moveLeftKey=pygame.K_LEFT,
            moveRightKey=pygame.K_RIGHT,
            jumpKey=pygame.K_UP,
        )

        self.gameState = "playing"
        self.statusMessage: str | None = None
        self.statusMessageTimerSeconds = 0.0
        self.backgroundSprite: pygame.Surface | None = None

        self._loadVisualAssets()

    def _loadVisualAssets(self) -> None:
        """Load sprites and attach them to gameplay objects.

        If a file is missing, we keep rectangle fallbacks so the game
        remains fully playable during collaboration.
        """

        self.backgroundSprite = loadScaledSprite(
            "background/cave.png",
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
        )

        self.fireboy.sprite = loadScaledSprite(
            "players/fireboy.png",
            (self.fireboy.rect.width, self.fireboy.rect.height),
            useWhiteColorKey=True,
        )
        self.watergirl.sprite = loadScaledSprite(
            "players/watergirl.png",
            (self.watergirl.rect.width, self.watergirl.rect.height),
            useWhiteColorKey=True,
        )

        for platform in self.level.platforms:
            spritePath = "tiles/ground.png" if platform.platformType == "ground" else "tiles/platform.png"
            platform.sprite = loadScaledSprite(spritePath, (platform.rect.width, platform.rect.height))

        for hazard in self.level.hazards:
            hazardSpriteByType = {
                "fire": "hazards/fire.png",
                "water": "hazards/water.png",
                "toxic": "hazards/toxic.png",
            }
            spritePath = hazardSpriteByType.get(hazard.hazardType)
            if spritePath is None:
                continue
            hazard.sprite = loadScaledSprite(spritePath, (hazard.rect.width, hazard.rect.height))

        for exitDoor in self.level.exits:
            exitSpriteByType = {
                "fire": "exits/fire_door.png",
                "water": "exits/water_door.png",
            }
            spritePath = exitSpriteByType.get(exitDoor.exitType)
            if spritePath is None:
                continue
            exitDoor.sprite = loadScaledSprite(spritePath, (exitDoor.rect.width, exitDoor.rect.height))

    def handleEvent(self, event: pygame.event.Event) -> None:
        """Handle event-driven controls like manual restart."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.resetLevel("Level restarted.")

    def resetLevel(self, resetReason: str | None = None) -> None:
        """Reset players and game state without rebuilding level geometry."""
        self.fireboy.resetToSpawn()
        self.watergirl.resetToSpawn()
        self.gameState = "playing"
        if resetReason:
            self.statusMessage = resetReason
            self.statusMessageTimerSeconds = settings.RESET_MESSAGE_DURATION_SECONDS
        else:
            self.statusMessage = None
            self.statusMessageTimerSeconds = 0.0

    def _updateStatusMessageTimer(self, deltaTimeSeconds: float) -> None:
        if self.statusMessageTimerSeconds <= 0:
            return
        self.statusMessageTimerSeconds -= deltaTimeSeconds
        if self.statusMessageTimerSeconds <= 0:
            self.statusMessage = None
            self.statusMessageTimerSeconds = 0.0

    def _updatePlayers(self, pressedKeys: pygame.key.ScancodeWrapper) -> None:
        self.fireboy.processInput(pressedKeys)
        self.watergirl.processInput(pressedKeys)
        self.fireboy.updateMovement(self.level.platforms)
        self.watergirl.updateMovement(self.level.platforms)

    def _checkLossConditions(self) -> bool:
        fireboyDied = self.fireboy.checkHazardCollision(self.level.hazards)
        watergirlDied = self.watergirl.checkHazardCollision(self.level.hazards)
        if fireboyDied or watergirlDied:
            self.resetLevel("A player touched the wrong hazard. Level reset.")
            return True
        return False

    def _updateExitConditions(self) -> None:
        self.fireboy.updateExitStatus(self.level.exits)
        self.watergirl.updateExitStatus(self.level.exits)
        if self.fireboy.hasReachedExit and self.watergirl.hasReachedExit:
            self.gameState = "won"
            self.statusMessage = None
            self.statusMessageTimerSeconds = 0.0

    def update(self, deltaTimeSeconds: float, pressedKeys: pygame.key.ScancodeWrapper) -> None:
        """Advance one frame of game logic."""
        self._updateStatusMessageTimer(deltaTimeSeconds)

        if self.gameState == "won":
            return

        self._updatePlayers(pressedKeys)
        if self._checkLossConditions():
            return
        self._updateExitConditions()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all world objects and the UI."""
        if self.backgroundSprite is not None:
            surface.blit(self.backgroundSprite, (0, 0))
        else:
            surface.fill(colors.DARK_BG)

        for platform in self.level.platforms:
            platform.draw(surface)
        for hazard in self.level.hazards:
            hazard.draw(surface)
        for exitDoor in self.level.exits:
            exitDoor.draw(surface)

        self.fireboy.draw(surface)
        self.watergirl.draw(surface)

        self.ui.draw(
            surface=surface,
            gameState=self.gameState,
            fireboy=self.fireboy,
            watergirl=self.watergirl,
            statusMessage=self.statusMessage,
        )
