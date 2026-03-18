"""UI rendering helpers for title, instructions, and state text."""

from __future__ import annotations

import pygame

import colors
import settings
from game.player import Player


class GameUI:
    """Renders lightweight text overlays for gameplay feedback."""

    def __init__(self) -> None:
        self.titleFont = pygame.font.SysFont("arial", 32, bold=True)
        self.bodyFont = pygame.font.SysFont("arial", 20)
        self.smallFont = pygame.font.SysFont("arial", 16)
        self.creditFont = pygame.font.SysFont("arial", 12)

    def draw(
        self,
        surface: pygame.Surface,
        gameState: str,
        fireboy: Player,
        watergirl: Player,
        statusMessage: str | None,
    ) -> None:
        """Draw game title, controls, objective, and runtime status."""

        creditLineOne = "Collaborated by Jack Yu and <Name>."
        creditLineTwo = "With the help of Cursor."

        creditSurfaceOne = self.creditFont.render(creditLineOne, True, colors.TEXT_SECONDARY)
        creditRectOne = creditSurfaceOne.get_rect(
            topright=(settings.SCREEN_WIDTH - settings.HUD_PADDING, settings.HUD_PADDING + 2)
        )
        surface.blit(creditSurfaceOne, creditRectOne)

        creditSurfaceTwo = self.creditFont.render(creditLineTwo, True, colors.TEXT_SECONDARY)
        creditRectTwo = creditSurfaceTwo.get_rect(
            topright=(settings.SCREEN_WIDTH - settings.HUD_PADDING, creditRectOne.bottom + 2)
        )
        surface.blit(creditSurfaceTwo, creditRectTwo)

        titleSurface = self.titleFont.render("Fireboy & Watergirl - HW7 Starter", True, colors.TEXT_PRIMARY)
        surface.blit(titleSurface, (settings.HUD_PADDING, settings.HUD_PADDING))

        controlsText = "Fireboy: A/D move, W jump | Watergirl: Left/Right move, Up jump | R: Restart"
        controlsSurface = self.smallFont.render(controlsText, True, colors.TEXT_SECONDARY)
        surface.blit(controlsSurface, (settings.HUD_PADDING, settings.HUD_PADDING + 38))

        objectiveSurface = self.bodyFont.render(
            "Goal: both players must stand in their matching exit doors.",
            True,
            colors.TEXT_PRIMARY,
        )
        surface.blit(objectiveSurface, (settings.HUD_PADDING, settings.HUD_PADDING + 64))

        fireStatus = "Fireboy exit: YES" if fireboy.hasReachedExit else "Fireboy exit: NO"
        waterStatus = "Watergirl exit: YES" if watergirl.hasReachedExit else "Watergirl exit: NO"
        statusLine = f"{fireStatus} | {waterStatus}"
        statusLineSurface = self.bodyFont.render(statusLine, True, colors.TEXT_SECONDARY)
        surface.blit(statusLineSurface, (settings.HUD_PADDING, settings.HUD_PADDING + 90))

        if gameState == "won":
            winSurface = self.bodyFont.render(
                "You win! Press R to restart this level.",
                True,
                colors.TEXT_SUCCESS,
            )
            surface.blit(winSurface, (settings.HUD_PADDING, settings.HUD_PADDING + 120))
        elif statusMessage:
            messageSurface = self.bodyFont.render(statusMessage, True, colors.TEXT_WARNING)
            surface.blit(messageSurface, (settings.HUD_PADDING, settings.HUD_PADDING + 120))
