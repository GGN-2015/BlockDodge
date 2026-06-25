from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pygame

from .constants import BLACK, BUTTON_BG, BUTTON_BORDER, BUTTON_TEXT, LIGHT_GREEN, ORANGE_RED


def make_font(size: int, bold: bool = False) -> pygame.font.Font:
    names = [
        "Microsoft YaHei UI",
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "Arial Unicode MS",
        "Arial",
    ]
    font_name = pygame.font.match_font(names, bold=bold)
    return pygame.font.Font(font_name, size)


def draw_text(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
    pos: tuple[int, int],
    *,
    center: bool = False,
    max_width: int | None = None,
    line_gap: int = 6,
    background: tuple[int, int, int, int] | None = None,
) -> pygame.Rect:
    if max_width is None:
        rendered = font.render(text, True, color)
        rect = rendered.get_rect()
        if center:
            rect.center = pos
        else:
            rect.topleft = pos
        if background is not None:
            bg = pygame.Surface((rect.width + 16, rect.height + 12), pygame.SRCALPHA)
            bg.fill(background)
            surface.blit(bg, (rect.x - 8, rect.y - 6))
        surface.blit(rendered, rect)
        return rect

    lines: list[str] = []
    for paragraph in text.splitlines():
        if not paragraph:
            lines.append("")
            continue
        current = ""
        for ch in paragraph:
            trial = current + ch
            if font.size(trial)[0] <= max_width or not current:
                current = trial
            else:
                lines.append(current)
                current = ch
        lines.append(current)
    line_height = font.get_linesize()
    width = max((font.size(line)[0] for line in lines), default=0)
    height = len(lines) * line_height + max(0, len(lines) - 1) * line_gap
    x, y = pos
    if background is not None:
        bg = pygame.Surface((width + 20, height + 16), pygame.SRCALPHA)
        bg.fill(background)
        surface.blit(bg, (x - 10, y - 8))
    cursor_y = y
    for line in lines:
        if line:
            surface.blit(font.render(line, True, color), (x, cursor_y))
        cursor_y += line_height + line_gap
    return pygame.Rect(x, y, width, height)


@dataclass(slots=True)
class Button:
    rect: pygame.Rect
    text: str
    action: Callable[[], None]
    enabled: bool = True
    visible: bool = True

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        if not self.visible:
            return
        mouse = pygame.mouse.get_pos()
        base = (232, 232, 232) if self.rect.collidepoint(mouse) and self.enabled else BUTTON_BG
        if not self.enabled:
            base = (220, 220, 220)
        pygame.draw.rect(surface, base, self.rect)
        pygame.draw.rect(surface, BUTTON_BORDER, self.rect, 1)
        color = BUTTON_TEXT if self.enabled else (120, 120, 120)
        draw_text(surface, self.text, font, color, self.rect.center, center=True)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if (
            self.visible
            and self.enabled
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        ):
            self.action()
            return True
        return False


def active_color(is_active: bool, kind: str = "buff") -> tuple[int, int, int] | None:
    if not is_active:
        return None
    return LIGHT_GREEN if kind == "buff" else ORANGE_RED


def draw_status_label(
    surface: pygame.Surface,
    text: str,
    pos: tuple[int, int],
    font: pygame.font.Font,
    *,
    active: bool = False,
    kind: str = "buff",
) -> pygame.Rect:
    rendered = font.render(text, True, BLACK)
    rect = rendered.get_rect(topleft=pos)
    color = active_color(active, kind)
    if color:
        pygame.draw.rect(surface, color, rect.inflate(8, 4))
    surface.blit(rendered, rect)
    return rect
