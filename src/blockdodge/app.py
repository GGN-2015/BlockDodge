from __future__ import annotations

import os
from enum import Enum, auto
from typing import Any

import pygame

from .assets import Assets
from .constants import (
    BLACK,
    CONTROL_PANEL_HEIGHT,
    GAME_AREA_HEIGHT,
    GAME_AREA_WIDTH,
    LEVEL_BULLET_SPEED,
    LEVEL_INTERVAL,
    LOGIC_TICK_MS,
    MAIN_TICK_MS,
    RANDOM_BULLET_SPEED,
    RANDOM_INTERVAL,
    TRACK_LENGTH,
    TRACK_NUMBER,
    DRAW_TICK_MS,
    TRANSMITTER_TICK_MS,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from .effects import Buff, Debuff, Final, lose_efficacy
from .ime import disable_ime_for_pygame_window
from .rank import add_or_update_rank_item, read_rank_items
from .state import GameState
from .transmitter import Transmitter
from .ui import Button, draw_status_label, draw_text, make_font


class Screen(Enum):
    MENU = auto()
    GAME = auto()


class Mode(Enum):
    LEVEL = 0
    RANDOM = 1


class BlockDodgeApp:
    def __init__(self, username: str = "") -> None:
        os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
        pygame.init()
        pygame.key.set_repeat(180, 80)
        try:
            pygame.mixer.init()
            self.audio_enabled = True
        except pygame.error:
            self.audio_enabled = False

        pygame.display.set_caption("德克萨斯送快递")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.ime_disabled = disable_ime_for_pygame_window()
        self.clock = pygame.time.Clock()
        self.assets = Assets.load()
        self.state = GameState()
        self.transmitter = Transmitter(TRACK_NUMBER, GAME_AREA_WIDTH, self.assets, LEVEL_INTERVAL)

        self.username = username
        self.if_record = bool(username)
        self.current_screen = Screen.MENU
        self.mode = Mode.LEVEL
        self.help_page = 0
        self.running = True
        self.message: tuple[str, int] | None = None
        self.tk_root: Any | None = None
        self.rank_window: Any | None = None
        self.rank_tree: Any | None = None
        self.background_x = 0
        self.frame_index = 0
        self.game_canvas = pygame.Surface((GAME_AREA_WIDTH, GAME_AREA_HEIGHT))

        self.logic_accum = 0
        self.transmitter_accum = 0
        self.main_accum = 0
        self.draw_accum = 0
        self.input_accum = 0
        self.w_key_was_down = False
        self.s_key_was_down = False
        self.w_key_is_down = False
        self.s_key_is_down = False
        self.vertical_hold_direction = 0

        self.menu_font = make_font(30)
        self.button_font = make_font(17)
        self.status_font = make_font(23)
        self.score_font = make_font(42)
        self.help_font = make_font(21)
        self.pause_font = make_font(110)

        self.menu_buttons: list[Button] = []
        self.game_buttons: list[Button] = []
        self._build_buttons()

    def _build_buttons(self) -> None:
        self.menu_buttons = [
            Button(pygame.Rect(100, 200, 200, 70), "关卡模式", self.start_level_mode),
            Button(pygame.Rect(100, 300, 200, 70), "随机模式", self.start_random_mode),
            Button(pygame.Rect(100, 400, 200, 70), "帮助", self.toggle_help),
            Button(pygame.Rect(100, 500, 200, 70), "退出", self.quit),
        ]
        y = GAME_AREA_HEIGHT + 18
        self.game_buttons = [
            Button(pygame.Rect(58, y, 101, 42), "开始游戏", self.toggle_pause),
            Button(pygame.Rect(281, y, 101, 42), "重置", self.reset_game),
            Button(pygame.Rect(524, y, 103, 42), "排行榜", self.show_rank),
            Button(pygame.Rect(759, y - 2, 88, 44), "返回", self.back_to_menu),
        ]

    @property
    def start_button(self) -> Button:
        return self.game_buttons[0]

    def quit(self) -> None:
        self.running = False

    def start_level_mode(self) -> None:
        self.mode = Mode.LEVEL
        self.state.bullet_speed_base = LEVEL_BULLET_SPEED
        self.state.interval_base = LEVEL_INTERVAL
        self.state.bullet_speed = LEVEL_BULLET_SPEED
        self.transmitter.set_interval(LEVEL_INTERVAL)
        self.reset_game()
        self.transmitter.load_track("demo2.txt")
        self._set_music(self.assets.music_path)
        self.current_screen = Screen.GAME

    def start_random_mode(self) -> None:
        self.mode = Mode.RANDOM
        self.state.bullet_speed_base = RANDOM_BULLET_SPEED
        self.state.interval_base = RANDOM_INTERVAL
        self.state.bullet_speed = RANDOM_BULLET_SPEED
        self.transmitter.set_interval(RANDOM_INTERVAL)
        self.reset_game()
        self.transmitter.load_random_track(TRACK_LENGTH)
        self._set_music(self.assets.endless_music_path)
        self.current_screen = Screen.GAME

    def _set_music(self, path: str) -> None:
        if not self.audio_enabled:
            return
        try:
            pygame.mixer.music.load(path)
        except pygame.error:
            self.audio_enabled = False

    def _play_music(self) -> None:
        if self.audio_enabled:
            pygame.mixer.music.play(-1)

    def _stop_music(self) -> None:
        if self.audio_enabled:
            pygame.mixer.music.stop()

    def toggle_help(self) -> None:
        self.help_page = (self.help_page + 1) % 3
        help_button = self.menu_buttons[2]
        if self.help_page == 0:
            help_button.text = "帮助"
            help_button.rect.topleft = (100, 400)
            for index in [0, 1, 3]:
                self.menu_buttons[index].visible = True
        elif self.help_page == 1:
            help_button.text = "下一页"
            help_button.rect.topleft = (1025, 675)
            for index in [0, 1, 3]:
                self.menu_buttons[index].visible = False
        else:
            help_button.text = "返回"
            help_button.rect.topleft = (1025, 675)

    def toggle_pause(self) -> None:
        if self.state.pause:
            self.state.pause = False
            self.start_button.text = "暂停"
            if not self.state.first_start:
                self.state.effect_resume()
            if self.state.first_start:
                if self.mode == Mode.LEVEL:
                    self.start_button.enabled = False
                self.state.first_start = False
                self._play_music()
            return
        self.state.pause = True
        self.start_button.text = "继续"
        self.state.effect_pause()

    def reset_game(self) -> None:
        self._stop_music()
        self.background_x = 0
        self.frame_index = 0
        self.state.pause = True
        self.state.first_start = True
        self.state.win_message = None
        self.state.effect_stop()
        self.state.reset_runtime()
        self.state.player.reset()
        self.transmitter.reset()
        self.logic_accum = 0
        self.transmitter_accum = 0
        self.main_accum = 0
        self.draw_accum = 0
        self.input_accum = 0
        self.w_key_was_down = False
        self.s_key_was_down = False
        self.w_key_is_down = False
        self.s_key_is_down = False
        self.vertical_hold_direction = 0
        self.start_button.text = "开始游戏"
        self.start_button.enabled = True
        if self.mode == Mode.LEVEL:
            self.transmitter.set_interval(LEVEL_INTERVAL)
            self.transmitter.load_track("demo2.txt")
        else:
            self.transmitter.set_interval(RANDOM_INTERVAL)
            self.transmitter.load_random_track(TRACK_LENGTH)

    def back_to_menu(self) -> None:
        self.state.effect_stop()
        self.reset_game()
        self.current_screen = Screen.MENU

    def show_rank(self) -> None:
        if self._show_rank_window():
            return
        self.message = ("排行榜窗口不可用", 2500)

    def run(self) -> int:
        while self.running:
            dt = self.clock.tick(120)
            dt = min(dt, 50)
            self._poll_tk()
            self._handle_events()
            self._handle_pressed_keys()
            if self.current_screen == Screen.GAME:
                self._update_game(dt)
            self._draw()
        self._stop_music()
        self._destroy_tk()
        pygame.quit()
        return 0

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                continue
            if event.type == pygame.KEYDOWN:
                self._handle_key(event)
            elif event.type == pygame.WINDOWFOCUSGAINED:
                self.ime_disabled = disable_ime_for_pygame_window()
                self._reset_vertical_input()
            elif event.type in (pygame.KEYUP, pygame.WINDOWFOCUSLOST):
                if event.type == pygame.KEYUP:
                    direction = self._vertical_key_direction(event)
                    if direction < 0:
                        self.w_key_is_down = False
                    elif direction > 0:
                        self.s_key_is_down = False
                else:
                    self._reset_vertical_input()
            if self.current_screen == Screen.MENU:
                for button in self.menu_buttons:
                    if button.handle_event(event):
                        break
            elif self.current_screen == Screen.GAME:
                for button in self.game_buttons:
                    if button.handle_event(event):
                        break

    def _handle_key(self, event: pygame.event.Event) -> None:
        if self.current_screen != Screen.GAME or self.state.pause:
            return
        direction = self._vertical_key_direction(event)
        if direction < 0:
            self.w_key_is_down = True
            self._move_player_vertical(-1)
        elif direction > 0:
            self.s_key_is_down = True
            self._move_player_vertical(1)

    def _handle_pressed_keys(self) -> None:
        if self.current_screen != Screen.GAME or self.state.pause:
            self._reset_vertical_input()
            return
        pressed = pygame.key.get_pressed()
        w_down = self.w_key_is_down or pressed[pygame.K_w] or pressed[pygame.K_UP]
        s_down = self.s_key_is_down or pressed[pygame.K_s] or pressed[pygame.K_DOWN]
        if w_down and not self.w_key_was_down:
            self._move_player_vertical(-1)
        if s_down and not self.s_key_was_down:
            self._move_player_vertical(1)
        if w_down and not s_down:
            self.vertical_hold_direction = -1
        elif s_down and not w_down:
            self.vertical_hold_direction = 1
        elif not w_down and not s_down:
            self.vertical_hold_direction = 0
        self.w_key_was_down = w_down
        self.s_key_was_down = s_down

    def _vertical_key_direction(self, event: pygame.event.Event) -> int:
        key_name = getattr(event, "unicode", "").lower()
        key_label = pygame.key.name(event.key).lower()
        scancode = getattr(event, "scancode", None)
        if event.key in (pygame.K_w, pygame.K_UP) or key_name == "w" or key_label == "w" or scancode in (26, 82):
            return -1
        if event.key in (pygame.K_s, pygame.K_DOWN) or key_name == "s" or key_label == "s" or scancode in (22, 81):
            return 1
        return 0

    def _reset_vertical_input(self) -> None:
        self.w_key_was_down = False
        self.s_key_was_down = False
        self.w_key_is_down = False
        self.s_key_is_down = False
        self.vertical_hold_direction = 0

    def _move_player_vertical(self, direction: int, *, reset_input_timer: bool = True) -> None:
        if direction < 0:
            self.state.player.move_up()
            self.w_key_was_down = True
        elif direction > 0:
            self.state.player.move_down()
            self.s_key_was_down = True
        if reset_input_timer:
            self.input_accum = 0

    def _update_game(self, dt: int) -> None:
        self.logic_accum += dt
        self.transmitter_accum += dt
        self.main_accum += dt
        self.draw_accum += dt
        self.input_accum += dt

        while self.vertical_hold_direction and self.input_accum >= 180:
            self._move_player_vertical(self.vertical_hold_direction, reset_input_timer=False)
            self.input_accum -= 180

        while self.draw_accum >= DRAW_TICK_MS:
            self._animation_tick()
            self.draw_accum -= DRAW_TICK_MS

        while self.transmitter_accum >= TRANSMITTER_TICK_MS:
            self.transmitter.transmitter_check(self.state.pause)
            self.transmitter_accum -= TRANSMITTER_TICK_MS

        while self.logic_accum >= LOGIC_TICK_MS:
            self._logic_tick()
            self.logic_accum -= LOGIC_TICK_MS

        while self.main_accum >= MAIN_TICK_MS:
            self._main_timer_count()
            self.main_accum -= MAIN_TICK_MS
        self._tick_effect_clocks(dt)

        if self.message is not None:
            text, remaining = self.message
            remaining -= dt
            self.message = (text, remaining) if remaining > 0 else None

    def _animation_tick(self) -> None:
        if self.state.first_start or self.state.pause:
            return
        self.background_x += 5
        if self.background_x > 4156:
            self.background_x = 0
        self.frame_index = (self.frame_index + 1) % len(self.assets.player_frames)

    def _logic_tick(self) -> None:
        block = self.state.player
        if block.win:
            self._handle_win()
            return
        if self.state.pause:
            return
        for index, bullet in enumerate(self.transmitter.bullets):
            if bullet is None:
                continue
            bullet.move(self.state)
            if bullet.leave_screen():
                self.transmitter.bullets[index] = None
                continue
            if block.magnet and isinstance(bullet, Buff) and bullet.meet_with(block):
                bullet.cause_effect(block, self.state, self.transmitter)
                self.transmitter.bullets[index] = None
                continue
            if bullet.collides_with(block):
                if self._collides_judge(index, bullet):
                    self._game_over()
                    break

    def _collides_judge(self, index: int, bullet: Bullet) -> bool:
        block = self.state.player
        if bullet.damage_type == 0:
            if block.bullet_ignore:
                self.transmitter.bullets[index] = None
                return False
            if block.shield_capacity > 0:
                block.shield_capacity -= 1
                self.transmitter.bullets[index] = None
                return False
            return True
        if bullet.damage_type == 1:
            if not block.effect_ignore and isinstance(bullet, Buff):
                bullet.cause_effect(block, self.state, self.transmitter)
            self.transmitter.bullets[index] = None
            return False
        if bullet.damage_type == 2:
            if not block.effect_ignore and isinstance(bullet, Debuff):
                bullet.cause_effect(block, self.state, self.transmitter)
            self.transmitter.bullets[index] = None
            return False
        if bullet.damage_type == 3 and isinstance(bullet, Final):
            bullet.cause_effect(block, self.state, self.transmitter)
            block.win = True
        return False

    def _handle_win(self) -> None:
        if self.if_record:
            add_or_update_rank_item(self.username, self.state.score)
        self.state.player.win = False
        self.state.effect_stop()
        self.reset_game()
        self._show_message_box("You Win!")

    def _game_over(self) -> None:
        self.state.effect_stop()
        self.reset_game()
        self._show_message_box("Game Over")

    def _main_timer_count(self) -> None:
        if self.state.pause:
            return
        self.state.score += self.state.score_step
        block = self.state.player
        checks = {
            "magnet": block.magnet,
            "timeslack": self.state.bullet_speed < self.state.bullet_speed_base and block.timeslack,
            "invincibility": block.effect_ignore and block.bullet_ignore,
            "sprint": self.state.bullet_speed > self.state.bullet_speed_base and block.effect_ignore and block.bullet_ignore,
            "fearless": block.fearless,
            "quick": block.quick,
        }
        for name, active in checks.items():
            if active and self.state.display_times[name] > 0:
                self.state.display_times[name] -= 500
            else:
                self.state.display_times[name] = 0
        for name in ["defense", "pure", "brave", "goodluck", "shield"]:
            if self.state.display_times[name] > 0:
                self.state.display_times[name] -= 250
            else:
                self.state.display_times[name] = 0
        self.state.active_bullets = sum(1 for bullet in self.transmitter.bullets if bullet is not None)

    def _tick_effect_clocks(self, elapsed_ms: int) -> None:
        expired: list[str] = []
        for name, effect_clock in self.state.effect_clocks.items():
            if not effect_clock.active:
                continue
            effect_clock.remaining_ms -= elapsed_ms
            if effect_clock.remaining_ms <= 0:
                expired.append(name)
        for name in expired:
            clock = self.state.effect_clocks.pop(name, None)
            if clock is not None:
                lose_efficacy(clock.on_elapsed, self.state, self.transmitter)

    def _draw(self) -> None:
        if self.current_screen == Screen.MENU:
            self._draw_menu()
        else:
            self._draw_game()
        if self.message is not None:
            self._draw_message(self.message[0])
        pygame.display.flip()

    def _draw_menu(self) -> None:
        main_scaled = pygame.transform.smoothscale(self.assets.main_page, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(main_scaled, (0, 0))
        if self.help_page == 1:
            text = (
                "\t又是平常的一天，德克萨斯身为企鹅物流的员工，又要去派送快递了！\n\n"
                "但是今天的路上依旧不那么太平啊，就像是误入了什么游戏一样，一把把刀剑从前面飞来！\n\n"
                "作为一名尖兵，躲过这些自然是易如反掌，但是有时候也会遇到不明确的BUFF与DEBUFF，让人措手不及！\n\n"
                "请你和德克萨斯合作，将快递安全送到目的地吧！\n\n"
                "\t使用W向上移动，S向下移动。\n\n作者：Aidan, Xuanfly\n\nSpecial Thanks：GGN_2015"
            )
            draw_text(self.screen, text, self.help_font, BLACK, (100, 100), max_width=600, background=(255, 255, 255, 200))
        elif self.help_page == 2:
            text = (
                "BUFF\n\n"
                "1. 护盾SHIELD。具有层数，可抵消一次子弹。\n"
                "2. 磁铁MAGNET。具有持续时间，在持续时间内可以吸收经过的 3 条赛道的 BUFF。\n"
                "3. 回防DEFENSE。一次性效果，若方块后方有位置，则退到当前赛道的后一个位置，并无敌小段时间。\n"
                "4. 缓时TIMESLACK。具有持续时间，持续时间内发射物速度变慢。\n"
                "5. 无敌INVINCIBILITY。具有持续时间，持续时间内抵消所有子弹和特殊道具。\n"
                "6. 净化PURE。一次性效果，清空所有已获得的特殊效果。\n"
                "7. 冲刺SPRINT。具有持续时间，持续时间内获得磁铁和无敌并加速游戏时间。\n\n"
                "DEBUFF\n\n"
                "1. 勇猛BRAVE。一次性效果，若方块前方有位置，则前进到当前赛道的前一个位置，并无敌小段时间。\n"
                "2. 无畏FEARLESS。具有持续时间，持续时间内子弹数量变多。\n"
                "3. 强运GOODLUCK。一次性效果，立刻发射 3 个并排的未知效果。\n"
                "4. 迅捷QUICK。具有持续时间，持续时间内发射物速度变快。\n"
                "5. 夜行NIGHTWALK。具有持续时间，持续时间内游戏画面黑白闪烁。"
            )
            draw_text(self.screen, text, self.help_font, BLACK, (50, 20), max_width=950, background=(255, 255, 255, 200))
        for button in self.menu_buttons:
            button.draw(self.screen, self.menu_font)

    def _draw_game(self) -> None:
        self.screen.fill(WHITE)
        self._draw_game_area()
        self._draw_status_panel()
        self._draw_controls()

    def _draw_game_area(self) -> None:
        if not self.state.first_start and self.state.pause:
            self.screen.blit(self.game_canvas, (0, 0))
            draw_text(self.screen, "PAUSE", self.pause_font, BLACK, (300, 200))
            return
        crop_rect = pygame.Rect(self.background_x, 0, GAME_AREA_WIDTH, GAME_AREA_HEIGHT)
        self.game_canvas.blit(self.assets.background_all, (0, 0), crop_rect)
        pygame.draw.rect(self.game_canvas, BLACK, pygame.Rect(0, 0, GAME_AREA_WIDTH, GAME_AREA_HEIGHT), 1)

        frame = self.assets.player_frames[self.frame_index]
        self.state.player.draw(self.game_canvas, frame)
        for bullet in self.transmitter.bullets:
            if bullet is not None:
                bullet.draw(self.game_canvas)
        self.screen.blit(self.game_canvas, (0, 0))

    def _draw_controls(self) -> None:
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(0, GAME_AREA_HEIGHT, GAME_AREA_WIDTH, CONTROL_PANEL_HEIGHT))
        for button in self.game_buttons:
            button.draw(self.screen, self.button_font)

    def _draw_status_panel(self) -> None:
        x = GAME_AREA_WIDTH + 10
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(GAME_AREA_WIDTH, 0, WINDOW_WIDTH - GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
        d = self.state.display_times
        draw_status_label(self.screen, "强运", (x + 33, 19), self.status_font, active=d["goodluck"] > 0, kind="debuff")
        draw_status_label(self.screen, "勇猛", (x + 65, 83), self.status_font, active=d["brave"] > 0, kind="debuff")
        draw_status_label(self.screen, "净化", (x + 75, 46), self.status_font, active=d["pure"] > 0)
        draw_status_label(self.screen, "回防", (x + 6, 64), self.status_font, active=d["defense"] > 0)
        draw_status_label(self.screen, "护盾", (x + 6, 124), self.status_font, active=d["shield"] > 0)
        draw_text(self.screen, str(self.state.player.shield_capacity), self.status_font, BLACK, (x + 84, 124))
        rows = [
            ("磁铁", "magnet", 156, "buff"),
            ("缓时", "timeslack", 189, "buff"),
            ("无敌", "invincibility", 221, "buff"),
            ("冲刺", "sprint", 253, "buff"),
            ("无畏", "fearless", 284, "debuff"),
            ("迅捷", "quick", 316, "debuff"),
            ("夜行", "nightwalk", 348, "debuff"),
        ]
        for label, key, y, kind in rows:
            draw_status_label(self.screen, label, (x + 6, y), self.status_font, active=d[key] // 1000 > 0, kind=kind)
            draw_text(self.screen, f"{d[key] // 1000}s", self.status_font, BLACK, (x + 84, y))
        draw_text(self.screen, "分数", self.status_font, BLACK, (x + 56, 420))
        draw_text(self.screen, str(self.state.score), self.score_font, BLACK, (x + 80, 480), center=True)

    def _draw_message(self, text: str) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        self.screen.blit(overlay, (0, 0))
        draw_text(self.screen, text, self.pause_font, BLACK, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), center=True)

    def _ensure_tk_root(self) -> Any | None:
        if self.tk_root is not None:
            return self.tk_root
        try:
            import tkinter as tk

            self.tk_root = tk.Tk()
            self.tk_root.withdraw()
            return self.tk_root
        except Exception:
            self.tk_root = None
            return None

    def _poll_tk(self) -> None:
        if self.tk_root is None:
            return
        try:
            self.tk_root.update_idletasks()
            self.tk_root.update()
        except Exception:
            self.tk_root = None
            self.rank_window = None
            self.rank_tree = None

    def _destroy_tk(self) -> None:
        if self.tk_root is None:
            return
        try:
            self.tk_root.destroy()
        except Exception:
            pass
        self.tk_root = None
        self.rank_window = None
        self.rank_tree = None

    def _show_message_box(self, text: str) -> None:
        root = self._ensure_tk_root()
        if root is None:
            self.message = (text, 2500)
            return
        try:
            from tkinter import messagebox

            messagebox.showinfo("", text, parent=root)
        except Exception:
            self.message = (text, 2500)

    def _show_rank_window(self) -> bool:
        root = self._ensure_tk_root()
        if root is None:
            return False
        try:
            import tkinter as tk
            from tkinter import ttk

            if self.rank_window is None or not self.rank_window.winfo_exists():
                self.rank_window = tk.Toplevel(root)
                self.rank_window.title("排行榜")
                self.rank_window.geometry("714x468")
                self.rank_window.resizable(True, True)
                self.rank_tree = ttk.Treeview(
                    self.rank_window,
                    columns=("Name", "Score"),
                    show="headings",
                    height=15,
                )
                self.rank_tree.heading("Name", text="Name")
                self.rank_tree.heading("Score", text="Score")
                self.rank_tree.column("Name", width=150, anchor="w")
                self.rank_tree.column("Score", width=120, anchor="center")
                self.rank_tree.place(x=181, y=0, width=332, height=468)
                self.rank_window.protocol("WM_DELETE_WINDOW", self.rank_window.destroy)
            assert self.rank_tree is not None
            for item in self.rank_tree.get_children():
                self.rank_tree.delete(item)
            for rank_item in read_rank_items():
                self.rank_tree.insert("", "end", values=(rank_item.name, rank_item.score))
            self.rank_window.deiconify()
            self.rank_window.lift()
            return True
        except Exception:
            return False


def ask_username() -> str:
    try:
        import tkinter as tk
        from tkinter import simpledialog

        root = tk.Tk()
        root.withdraw()
        username = simpledialog.askstring("提示", "请输入您的用户名：", parent=root)
        root.destroy()
        return username or ""
    except Exception:
        return ""


def main() -> int:
    username = ask_username()
    return BlockDodgeApp(username).run()
