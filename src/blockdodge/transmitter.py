from __future__ import annotations

import random
from pathlib import Path

from .assets import Assets
from .constants import BULLET_HEIGHT, BULLET_TOTAL, BULLET_WIDTH, CONFIG_DIR, TRACK_POS_Y
from .effects import Final, certain_buff, random_buff, random_debuff, random_effect
from .entities import Bullet


class Transmitter:
    def __init__(self, track_number: int, start_x: int, assets: Assets, interval: int = 500) -> None:
        self.start_x = start_x
        self.interval = interval
        self.assets = assets
        self.track: list[list[int]] = [[] for _ in range(track_number)]
        self.track_length = 100000
        self.bullet_number = 0
        self.time_count = 0
        self.goodluck = False
        self.end_transmit = False
        self.bullets: list[Bullet | None] = [None for _ in range(BULLET_TOTAL)]

    def reset(self) -> None:
        self.track_length = 100000
        self.bullet_number = 0
        self.time_count = 0
        self.goodluck = False
        self.end_transmit = False
        self.track = [[] for _ in range(len(self.track))]
        self.bullets = [None for _ in range(BULLET_TOTAL)]

    def load_track(self, docname: str) -> None:
        self.reset()
        path = CONFIG_DIR / docname
        lines = Path(path).read_text(encoding="utf-8").splitlines()
        for lane_index in range(len(self.track)):
            line = lines[lane_index].strip()
            self.track_length = min(self.track_length, len(line))
            for ch in line:
                if ch == "0":
                    self.track[lane_index].append(0)
                elif "0" < ch <= "9":
                    self.track[lane_index].append(ord(ch) - ord("0"))
                    self.bullet_number += 1
                else:
                    self.track[lane_index].append(ord(ch) - ord("a") + 10)
                    self.bullet_number += 1

    def load_random_track(self, time_length: int) -> None:
        self.reset()
        self.track_length = time_length
        i = 0
        while i < self.track_length:
            flag = False
            added_bullets = 0
            for lane in self.track:
                value = random.randrange(0, 100)
                if value < 25:
                    flag = True
                    lane.append(0)
                elif value < 35:
                    flag = True
                    lane.append(2)
                    added_bullets += 1
                elif value < 45:
                    flag = True
                    lane.append(3)
                    added_bullets += 1
                else:
                    lane.append(1)
                    added_bullets += 1
            if not flag:
                for lane in self.track:
                    lane.pop()
                continue
            self.bullet_number += added_bullets
            i += 1

    def set_interval(self, interval: int) -> None:
        self.interval = max(1, interval)

    def _first_empty_slot(self) -> int | None:
        for index, bullet in enumerate(self.bullets):
            if bullet is None:
                return index
        return None

    def _append_bullet(self, bullet: Bullet) -> None:
        slot = self._first_empty_slot()
        if slot is not None:
            self.bullets[slot] = bullet

    def _append_three(self, factory) -> None:
        emitted = 0
        for slot, bullet in enumerate(self.bullets):
            if bullet is None:
                self.bullets[slot] = factory(emitted)
                emitted += 1
                if emitted > 2:
                    break

    def transmitter_check(self, paused: bool) -> None:
        if paused:
            return
        self.time_count += 50
        index = self.time_count // self.interval
        if index >= self.track_length and not self.end_transmit:
            self.end_transmit = True
            self._append_three(
                lambda lane: Final(self.start_x, TRACK_POS_Y[lane], self.assets.goal)
            )
            return
        if self.end_transmit:
            return
        if self.time_count % self.interval != 0:
            return
        if self.goodluck:
            self.goodluck = False
            self._append_three(
                lambda lane: random_effect(
                    self.start_x,
                    TRACK_POS_Y[lane],
                    self.assets.random_effect,
                    self.assets.buff,
                    self.assets.debuff,
                )
            )
            return
        for lane_index, lane in enumerate(self.track):
            value = lane[index]
            if value == 0:
                continue
            y = TRACK_POS_Y[lane_index]
            if value == 1:
                self._append_bullet(Bullet(self.start_x, y, self.assets.sword))
            elif value == 2:
                self._append_bullet(random_buff(self.start_x, y, self.assets.buff))
            elif value == 3:
                self._append_bullet(random_debuff(self.start_x, y, self.assets.debuff))
            elif 4 < value <= 11:
                self._append_bullet(certain_buff(value - 4, self.start_x, y, self.assets.buff))
