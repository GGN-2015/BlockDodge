from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame

from .constants import (
    BLOCK_HEIGHT,
    BLOCK_SIZE,
    BLOCK_WIDTH,
    BULLET_HEIGHT,
    BULLET_WIDTH,
    PLAYER_POINTS,
)
from .geometry import Rect

if TYPE_CHECKING:
    from .state import GameState


@dataclass(slots=True)
class Player:
    x: int = PLAYER_POINTS[0][1][0]
    y: int = PLAYER_POINTS[0][1][1]
    coordinate_x: int = 0
    coordinate_y: int = 1
    shield_capacity: int = 0
    bullet_ignore: bool = False
    magnet: bool = False
    effect_ignore: bool = False
    fearless: bool = False
    timeslack: bool = False
    quick: bool = False
    win: bool = False

    @property
    def rect(self) -> Rect:
        return Rect(self.x, self.y, BLOCK_WIDTH, BLOCK_HEIGHT)

    def reset(self) -> None:
        self.coordinate_x = 0
        self.coordinate_y = 1
        self.x, self.y = PLAYER_POINTS[0][1]
        self.shield_capacity = 0
        self.bullet_ignore = False
        self.magnet = False
        self.effect_ignore = False
        self.fearless = False
        self.timeslack = False
        self.quick = False
        self.win = False

    def change_position(self, coordinate_x: int, coordinate_y: int) -> None:
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.x, self.y = PLAYER_POINTS[coordinate_x][coordinate_y]

    def move_up(self) -> None:
        if self.coordinate_y > 0:
            self.change_position(self.coordinate_x, self.coordinate_y - 1)

    def move_down(self) -> None:
        if self.coordinate_y < 2:
            self.change_position(self.coordinate_x, self.coordinate_y + 1)

    def draw(self, surface: pygame.Surface, image: pygame.Surface) -> None:
        surface.blit(image, (self.x, self.y))


class Bullet:
    damage_type = 0

    def __init__(self, x: int, y: int, image: pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.pos_x = float(x)
        self.image = image
        self.is_fired = False

    def move(self, state: "GameState") -> None:
        self.pos_x -= state.bullet_speed
        self.x = int(self.pos_x)

    def collision_rect(self) -> Rect:
        return Rect(self.x, self.y + 12, BULLET_WIDTH, 24)

    def collides_with(self, block: Player) -> bool:
        return self.collision_rect().intersects(block.rect)

    def leave_screen(self) -> bool:
        return self.x + BULLET_WIDTH < 10

    def meet_with(self, block: Player) -> bool:
        return block.x < self.x + BULLET_WIDTH and block.x + BLOCK_SIZE > self.x

    def pass_player(self, block: Player) -> bool:
        return block.x > self.x + BULLET_WIDTH

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, (self.x, self.y))
