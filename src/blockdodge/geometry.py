from __future__ import annotations

from typing import NamedTuple


class Rect(NamedTuple):
    x: int
    y: int
    width: int
    height: int

    def intersects(self, other: "Rect") -> bool:
        return (
            self.x < other.x + other.width
            and self.x + self.width > other.x
            and self.y < other.y + other.height
            and self.y + self.height > other.y
        )
