from __future__ import annotations

from dataclasses import dataclass

import pygame

from .constants import BLOCK_HEIGHT, BLOCK_WIDTH, BULLET_HEIGHT, BULLET_WIDTH, RESOURCE_DIR


@dataclass(slots=True)
class Assets:
    background_all: pygame.Surface
    main_page: pygame.Surface
    sword: pygame.Surface
    buff: pygame.Surface
    debuff: pygame.Surface
    random_effect: pygame.Surface
    goal: pygame.Surface
    player_frames: list[pygame.Surface]
    music_path: str
    endless_music_path: str

    @classmethod
    def load(cls) -> "Assets":
        def image(name: str) -> pygame.Surface:
            return pygame.image.load(str(RESOURCE_DIR / name)).convert_alpha()

        def scaled(name: str, size: tuple[int, int]) -> pygame.Surface:
            return pygame.transform.smoothscale(image(name), size)

        frames = [
            pygame.transform.smoothscale(image(f"mod_00{i}.png"), (BLOCK_WIDTH, BLOCK_HEIGHT))
            for i in range(3, 26)
        ]
        return cls(
            background_all=image("background_all.png").convert(),
            main_page=image("MainpagePic.png").convert(),
            sword=scaled("sword.png", (BULLET_WIDTH, BULLET_HEIGHT)),
            buff=scaled("BUFF.png", (BULLET_WIDTH, BULLET_HEIGHT)),
            debuff=scaled("DEBUFF.png", (BULLET_WIDTH, BULLET_HEIGHT)),
            random_effect=scaled("RandomEffect.png", (BULLET_WIDTH, BULLET_HEIGHT)),
            goal=scaled("goal.png", (BULLET_WIDTH, BULLET_HEIGHT)),
            player_frames=frames,
            music_path=str(RESOURCE_DIR / "music.wav"),
            endless_music_path=str(RESOURCE_DIR / "endless.wav"),
        )
