from __future__ import annotations

from dataclasses import dataclass, field

from .constants import (
    DEFAULT_SCORE_STEP,
    LEVEL_BULLET_SPEED,
    LEVEL_INTERVAL,
    SPRINT_SCORE_STEP,
)
from .entities import Player


@dataclass(slots=True)
class EffectClock:
    remaining_ms: int
    on_elapsed: str
    display_remaining_ms: int
    pauseable: bool = True
    active: bool = True

    def pause(self) -> None:
        if self.pauseable:
            self.active = False

    def resume(self) -> None:
        if self.pauseable:
            self.active = True


@dataclass(slots=True)
class GameState:
    player: Player = field(default_factory=Player)
    bullet_speed_base: float = LEVEL_BULLET_SPEED
    bullet_speed: float = LEVEL_BULLET_SPEED
    interval_base: int = LEVEL_INTERVAL
    score_step: int = DEFAULT_SCORE_STEP
    score: int = 0
    active_bullets: int = 0
    pause: bool = True
    first_start: bool = True
    win_message: str | None = None
    effect_clocks: dict[str, EffectClock] = field(default_factory=dict)
    display_times: dict[str, int] = field(
        default_factory=lambda: {
            "magnet": 0,
            "timeslack": 0,
            "invincibility": 0,
            "sprint": 0,
            "fearless": 0,
            "quick": 0,
            "nightwalk": 0,
            "defense": 0,
            "pure": 0,
            "brave": 0,
            "goodluck": 0,
            "shield": 0,
        }
    )

    def reset_runtime(self) -> None:
        self.effect_clocks.clear()
        for key in self.display_times:
            self.display_times[key] = 0
        self.score = 0
        self.score_step = DEFAULT_SCORE_STEP
        self.active_bullets = 0
        self.bullet_speed = self.bullet_speed_base

    def effect_pause(self) -> None:
        for clock in self.effect_clocks.values():
            clock.pause()

    def effect_resume(self) -> None:
        for clock in self.effect_clocks.values():
            clock.resume()

    def effect_stop(self) -> None:
        self.player.effect_ignore = False
        self.player.bullet_ignore = False
        self.player.magnet = False
        self.player.fearless = False
        self.player.timeslack = False
        self.player.quick = False
        self.bullet_speed = self.bullet_speed_base
        self.score_step = DEFAULT_SCORE_STEP
        self.effect_clocks.clear()

    def set_timed_effect(
        self,
        name: str,
        duration_ms: int,
        display_ms: int,
        on_elapsed: str,
        *,
        pauseable: bool = True,
    ) -> None:
        self.display_times[name] = display_ms
        self.effect_clocks[name] = EffectClock(duration_ms, on_elapsed, display_ms, pauseable)

    def stop_effect(self, name: str) -> None:
        self.effect_clocks.pop(name, None)

    def sprint_score(self) -> None:
        self.score_step = SPRINT_SCORE_STEP
