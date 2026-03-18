"""Reusable level object classes."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

import colors


@dataclass
class Platform:
    """A solid rectangle that players can stand on and collide with."""

    rect: pygame.Rect

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, colors.PLATFORM_BROWN, self.rect)
        pygame.draw.rect(surface, colors.PLATFORM_OUTLINE, self.rect, width=2)


@dataclass
class Hazard:
    """A hazardous area with a typed damage rule."""

    rect: pygame.Rect
    hazardType: str

    def draw(self, surface: pygame.Surface) -> None:
        color_lookup = {
            "fire": colors.FIRE_HAZARD_COLOR,
            "water": colors.WATER_HAZARD_COLOR,
            "toxic": colors.TOXIC_HAZARD_COLOR,
        }
        pygame.draw.rect(surface, color_lookup[self.hazardType], self.rect)


@dataclass
class ExitDoor:
    """A typed goal zone that must be matched by player type."""

    rect: pygame.Rect
    exitType: str

    def draw(self, surface: pygame.Surface) -> None:
        color_lookup = {
            "fire": colors.FIRE_EXIT_COLOR,
            "water": colors.WATER_EXIT_COLOR,
        }
        pygame.draw.rect(surface, color_lookup[self.exitType], self.rect)
        pygame.draw.rect(surface, colors.BLACK, self.rect, width=2)
