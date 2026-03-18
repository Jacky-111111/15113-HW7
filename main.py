"""Entry point for the Fireboy/Watergirl HW7 prototype."""

from __future__ import annotations

import pygame

import settings
from game.game_manager import GameManager


def runGame() -> None:
    """Initialize pygame and run the main loop."""
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.WINDOW_TITLE)
    clock = pygame.time.Clock()

    gameManager = GameManager()
    isRunning = True

    while isRunning:
        deltaTimeSeconds = clock.tick(settings.FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            else:
                gameManager.handleEvent(event)

        pressedKeys = pygame.key.get_pressed()
        gameManager.update(deltaTimeSeconds, pressedKeys)
        gameManager.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    runGame()
