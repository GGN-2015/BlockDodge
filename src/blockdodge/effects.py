from __future__ import annotations

import random
from typing import TYPE_CHECKING

import pygame

from .constants import (
    DEFAULT_SCORE_STEP,
    LEVEL_INTERVAL,
    SPRINT_SCORE_STEP,
)
from .entities import Bullet, Player

if TYPE_CHECKING:
    from .state import GameState
    from .transmitter import Transmitter


class Effect(Bullet):
    def cause_effect(self, block: Player, state: "GameState", transmitter: "Transmitter") -> None:
        raise NotImplementedError


class Buff(Effect):
    damage_type = 1


class Debuff(Effect):
    damage_type = 2


class Shield(Buff):
    def cause_effect(self, block: Player, state: "GameState", transmitter: "Transmitter") -> None:
        block.shield_capacity += 1
        state.display_times["shield"] = 500


class Magnet(Buff):
    def cause_effect(self, block: Player, state: "GameState", transmitter: "Transmitter") -> None:
        block.magnet = True
        state.set_timed_effect("magnet", 10000, 10500, "magnet")


class Defense(Buff):
    def cause_effect(self, block: Player, state: "GameState", transmitter: "Transmitter") -> None:
        block.bullet_ignore = True
        block.effect_ignore = True
        if block.coordinate_x > 0:
            block.change_position(block.coordinate_x - 1, block.coordinate_y)
        state.set_timed_effect("defense", 500, 500, "defense", pauseable=False)


class Timeslack(Buff):
    def cause_effect(self, block: Player, state: "GameState", transmitter: "Transmitter") -> None:
        if block.quick:
            state.bullet_speed = state.bullet_speed_base
            block.quick = False
            state.stop_effect("quick")
            return
        if not block.timeslack:
            state.bullet_speed = 3
            transmitter.set_interval(state.interval_base * 2)
            block.timeslack = True
        state.set_timed_effect("timeslack", 5000, 5500, "timeslack")


class Invincibility(Buff):
    def cause_effect(self, block: Player, state: "GameState", transmitter: "Transmitter") -> None:
        block.effect_ignore = True
        block.bullet_ignore = True
        state.set_timed_effect("invincibility", 5000, 5500, "invincibility")


class Sprint(Buff):
    def cause_effect(self, block: Player, state: "GameState", transmitter: "Transmitter") -> None:
        if block.effect_ignore:
            return
        if block.quick:
            state.bullet_speed = state.bullet_speed_base
            block.quick = False
            state.stop_effect("quick")
        state.bullet_speed = state.bullet_speed_base * 4
        transmitter.set_interval(state.interval_base // 4)
        state.score_step = SPRINT_SCORE_STEP
        block.effect_ignore = True
        block.bullet_ignore = True
        state.set_timed_effect("sprint", 4000, 4500, "sprint")


class Pure(Buff):
    def cause_effect(self, block: Player, state: "GameState", transmitter: "Transmitter") -> None:
        block.effect_ignore = False
        block.bullet_ignore = False
        block.magnet = False
        block.fearless = False
        block.timeslack = False
        block.quick = False
        state.bullet_speed = state.bullet_speed_base
        transmitter.set_interval(state.interval_base)
        for name in ["magnet", "fearless", "invincibility", "timeslack", "sprint"]:
            state.stop_effect(name)
        state.set_timed_effect("pure", 500, 500, "pure", pauseable=False)


class Brave(Debuff):
    def cause_effect(self, block: Player, state: "GameState", transmitter: "Transmitter") -> None:
        block.bullet_ignore = True
        block.effect_ignore = True
        if block.coordinate_x < 2:
            block.change_position(block.coordinate_x + 1, block.coordinate_y)
        state.set_timed_effect("brave", 500, 500, "brave", pauseable=False)


class Fearless(Debuff):
    def cause_effect(self, block: Player, state: "GameState", transmitter: "Transmitter") -> None:
        if not block.fearless:
            block.fearless = True
            transmitter.set_interval(state.interval_base - 500)
        state.set_timed_effect("fearless", 6000, 6500, "fearless")


class Goodluck(Debuff):
    def cause_effect(self, block: Player, state: "GameState", transmitter: "Transmitter") -> None:
        transmitter.goodluck = True
        state.set_timed_effect("goodluck", 500, 500, "goodluck", pauseable=False)


class Quick(Debuff):
    def cause_effect(self, block: Player, state: "GameState", transmitter: "Transmitter") -> None:
        if block.timeslack:
            block.timeslack = False
            state.bullet_speed = state.bullet_speed_base
            transmitter.set_interval(state.interval_base)
            state.stop_effect("timeslack")
            return
        if not block.quick:
            block.quick = True
            state.bullet_speed = state.bullet_speed_base * 3
        state.set_timed_effect("quick", 5000, 5500, "quick")


class Nightwalk(Debuff):
    def cause_effect(self, block: Player, state: "GameState", transmitter: "Transmitter") -> None:
        state.set_timed_effect("nightwalk", 4000, 4000, "nightwalk")


class Final(Buff):
    damage_type = 3

    def cause_effect(self, block: Player, state: "GameState", transmitter: "Transmitter") -> None:
        block.win = True


def lose_efficacy(name: str, state: "GameState", transmitter: "Transmitter") -> None:
    block = state.player
    if name == "magnet":
        block.magnet = False
    elif name == "defense":
        block.bullet_ignore = False
        block.effect_ignore = False
    elif name == "timeslack":
        state.bullet_speed = state.bullet_speed_base
        transmitter.set_interval(state.interval_base)
        block.timeslack = False
    elif name == "invincibility":
        block.effect_ignore = False
        block.bullet_ignore = False
    elif name == "sprint":
        state.bullet_speed = state.bullet_speed_base
        transmitter.set_interval(state.interval_base)
        state.score_step = DEFAULT_SCORE_STEP
        block.bullet_ignore = False
        block.effect_ignore = False
    elif name == "brave":
        block.bullet_ignore = False
        block.effect_ignore = False
    elif name == "fearless":
        transmitter.set_interval(state.interval_base)
        block.fearless = False
    elif name == "quick":
        state.bullet_speed = state.bullet_speed_base
        block.quick = False


def random_buff(x: int, y: int, image: pygame.Surface) -> Buff:
    value = random.randrange(0, 100)
    if value < 20:
        return Shield(x, y, image)
    if value < 35:
        return Magnet(x, y, image)
    if value < 55:
        return Defense(x, y, image)
    if value < 70:
        return Timeslack(x, y, image)
    if value < 75:
        return Invincibility(x, y, image)
    if value < 90:
        return Pure(x, y, image)
    return Sprint(x, y, image)


def random_debuff(x: int, y: int, image: pygame.Surface) -> Debuff:
    value = random.randrange(0, 100)
    if value < 25:
        return Brave(x, y, image)
    if value < 50:
        return Fearless(x, y, image)
    if value < 75:
        return Goodluck(x, y, image)
    if value < 100:
        return Quick(x, y, image)
    return Nightwalk(x, y, image)


def random_effect(x: int, y: int, image: pygame.Surface, buff_image: pygame.Surface, debuff_image: pygame.Surface) -> Effect:
    value = random.randrange(0, 100)
    if value < 30:
        effect = random_buff(x, y, buff_image)
    else:
        effect = random_debuff(x, y, debuff_image)
    effect.image = image
    return effect


def certain_buff(number: int, x: int, y: int, image: pygame.Surface) -> Buff:
    if number == 1:
        return Shield(x, y, image)
    if number == 2:
        return Magnet(x, y, image)
    if number == 3:
        return Defense(x, y, image)
    if number == 4:
        return Timeslack(x, y, image)
    if number == 5:
        return Invincibility(x, y, image)
    if number == 6:
        return Pure(x, y, image)
    return Sprint(x, y, image)
