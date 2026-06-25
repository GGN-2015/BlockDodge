from __future__ import annotations

import ctypes
import sys

import pygame


def disable_ime_for_pygame_window() -> bool:
    """Disable text input and detach the Windows IME context when possible."""
    pygame.key.stop_text_input()
    if sys.platform != "win32":
        return False
    try:
        window_info = pygame.display.get_wm_info()
        hwnd = window_info.get("window")
        if not hwnd:
            return False
        imm32 = ctypes.WinDLL("imm32", use_last_error=True)
        imm32.ImmAssociateContext.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        imm32.ImmAssociateContext.restype = ctypes.c_void_p
        result = imm32.ImmAssociateContext(ctypes.c_void_p(hwnd), ctypes.c_void_p(0))
        return bool(result)
    except Exception:
        return False
