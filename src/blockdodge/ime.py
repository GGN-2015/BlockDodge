from __future__ import annotations

import ctypes
import sys

import pygame


def prepare_keyboard_input_for_game_window() -> None:
    """Keep gameplay controls on key events instead of IME text events."""
    pygame.key.stop_text_input()
    for event_type in _text_input_event_types():
        pygame.event.set_blocked(event_type)
    if sys.platform != "win32":
        return
    try:
        window_info = pygame.display.get_wm_info()
        hwnd = window_info.get("window")
        if not hwnd:
            return
        imm32 = ctypes.WinDLL("imm32", use_last_error=True)
        imm32.ImmAssociateContext.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        imm32.ImmAssociateContext.restype = ctypes.c_void_p
        imm32.ImmAssociateContext(ctypes.c_void_p(hwnd), ctypes.c_void_p(0))
    except Exception:
        return


def _text_input_event_types() -> tuple[int, ...]:
    return tuple(
        event_type
        for event_type in (
            getattr(pygame, "TEXTEDITING", None),
            getattr(pygame, "TEXTINPUT", None),
        )
        if event_type is not None
    )
