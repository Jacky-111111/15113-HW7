"""Level data and level object construction."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from game.objects import ExitDoor, Hazard, Platform


@dataclass
class Level:
    """Container for all static geometry and spawn positions in one level."""

    levelName: str
    platforms: list[Platform]
    hazards: list[Hazard]
    exits: list[ExitDoor]
    spawnPositions: dict[str, tuple[int, int]]


STARTER_LEVEL_DEFINITION = {
    "levelName": "Starter Cavern",
    "spawnPositions": {
        "fire": (70, 530),
        "water": (120, 530),
    },
    "platformRects": [
        {"platformType": "ground", "rect": (0, 608, 960, 32)},  # Ground
        {"platformType": "platform", "rect": (180, 535, 170, 24)},
        {"platformType": "platform", "rect": (430, 495, 150, 24)},
        {"platformType": "platform", "rect": (680, 450, 200, 24)},
        {"platformType": "platform", "rect": (310, 380, 150, 24)},
        {"platformType": "platform", "rect": (530, 315, 160, 24)},
        {"platformType": "platform", "rect": (140, 275, 170, 24)},
    ],
    "hazards": [
        {"hazardType": "water", "rect": (250, 608 - 20, 140, 20)},
        {"hazardType": "fire", "rect": (560, 608 - 20, 140, 20)},
        {"hazardType": "toxic", "rect": (760, 608 - 20, 90, 20)},
    ],
    "exits": [
        {"exitType": "fire", "rect": (870, 560, 32, 48)},
        {"exitType": "water", "rect": (910, 560, 32, 48)},
    ],
}


def loadStarterLevel() -> Level:
    """Build and return the starter level object.

    This function uses in-code dictionaries for readability during early
    development. New collaborators can quickly tweak coordinates while
    testing gameplay.
    """

    definition = STARTER_LEVEL_DEFINITION

    platforms: list[Platform] = []
    for platformData in definition["platformRects"]:
        if isinstance(platformData, tuple):
            # Backward-compatible path for older test data format.
            x, y, width, height = platformData
            platforms.append(Platform(rect=pygame.Rect(x, y, width, height)))
        else:
            platforms.append(
                Platform(
                    rect=pygame.Rect(*platformData["rect"]),
                    platformType=platformData.get("platformType", "platform"),
                )
            )

    hazards = [
        Hazard(
            rect=pygame.Rect(*hazardData["rect"]),
            hazardType=hazardData["hazardType"],
        )
        for hazardData in definition["hazards"]
    ]

    exits = [
        ExitDoor(
            rect=pygame.Rect(*exitData["rect"]),
            exitType=exitData["exitType"],
        )
        for exitData in definition["exits"]
    ]

    return Level(
        levelName=definition["levelName"],
        platforms=platforms,
        hazards=hazards,
        exits=exits,
        spawnPositions=definition["spawnPositions"],
    )


# TODO: Move level definitions to external JSON files once we add multiple levels.
