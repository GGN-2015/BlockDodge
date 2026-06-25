from __future__ import annotations

import shutil
from dataclasses import dataclass

from .constants import RESOURCE_DIR, USER_DATA_DIR, USER_RANK_FILE


@dataclass(slots=True)
class RankItem:
    name: str
    score: int


def ensure_rank_file() -> None:
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not USER_RANK_FILE.exists():
        source = RESOURCE_DIR / "rank.txt"
        shutil.copyfile(source, USER_RANK_FILE)


def read_rank_items() -> list[RankItem]:
    ensure_rank_file()
    items: list[RankItem] = []
    for line in USER_RANK_FILE.read_text(encoding="utf-8").splitlines():
        fields = line.split(",")
        if len(fields) != 2:
            continue
        name = fields[0].strip()
        try:
            score = int(fields[1].strip())
        except ValueError:
            continue
        items.append(RankItem(name, score))
    return items


def add_or_update_rank_item(name: str, score: int) -> None:
    ensure_rank_file()
    items = read_rank_items()
    found = False
    for item in items:
        if item.name == name:
            item.score = max(item.score, score)
            found = True
            break
    if not found:
        items.append(RankItem(name, score))
    items.sort(key=lambda item: item.score, reverse=True)
    USER_RANK_FILE.write_text(
        "".join(f"{item.name}, {item.score}\n" for item in items),
        encoding="utf-8",
    )
