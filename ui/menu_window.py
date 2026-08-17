import curses
from typing import Literal


MenuPositions = Literal["center", "left"]


class Menu:
    def __init__(
                self,
                header: str,
                actions: list[str]
                ) -> None:

        self.header = header
        self.actions = actions
        self.selected_row_idx = 0

    def move_up(self) -> None:
        if self.selected_row_idx > 0:
            self.selected_row_idx -= 1

    def move_down(self) -> None:
        if self.selected_row_idx < len(self.actions) - 1:
            self.selected_row_idx += 1

    def selected_action(self) -> str:
        return self.actions[self.selected_row_idx]


class MenuPanel():
    def __init__(
                self,
                menu: Menu,
                position: MenuPositions,
                screen: curses.window
                ) -> None:

        self.menu = menu
        self.position = position
        self.h, self.w = self.calculate_size(menu)
        self.top, self.left, self.right = self.calculate_position(screen)
        self.create_window()
        self.print_menu()

    @staticmethod
    def calculate_size(
                    menu: Menu
                    ) -> tuple[int, int]:

        vertical_padding = 6
        horizontal_padding = 4

        panel_h: int = len(menu.actions) + vertical_padding
        width_actions: int = max(len(row) for row in menu.actions)
        width_header: int = len(menu.header)
        panel_w = max(width_actions, width_header) + horizontal_padding

        return (panel_h, panel_w)

    def calculate_position(
                        self,
                        screen: curses.window
                        ) -> tuple[int, int, int]:

        screen_h, screen_w = screen.getmaxyx()
        padding = 2

        if self.position == "center":
            top = screen_h//2 - self.h//2
            left = screen_w//2 - self.w//2
            right = screen_w//2 + self.w//2

        elif self.position == "left":
            top = screen_h//2 - self.h//2
            left = padding
            right = left + self.w

        if (
            top < 0
            or left < 0
            or right > screen_w
            or top + self.h > screen_h
            or left + self.w > screen_w
            or right + padding > screen_w
                ):
            raise ValueError(
                        "Terminal size changed. The layout no longer fits.\n"
                        )

        else:
            return (top, left, right)

    def create_window(
                        self
                        ) -> None:

        self.window = curses.newwin(self.h, self.w, self.top, self.left)

        self.window.bkgd(" ", curses.color_pair(1))
        self.window.keypad(True)
        self.window.border()
        self.window.refresh()

    def print_menu(
                    self
                    ) -> None:

        self.window.border()
        x = self.w//2 - len(self.menu.header)//2
        y = 1
        self.window.addstr(y, x, self.menu.header)

        for idx, row in enumerate(self.menu.actions):
            x = self.w//2 - len(row)//2
            y = self.h//2 - len(self.menu.actions)//2 + idx

            if idx == self.menu.selected_row_idx:
                self.window.addstr(y, x, row, curses.color_pair(2))
            else:
                self.window.addstr(y, x, row)

        self.window.refresh()

    def navigate_menu(
                        self
                        ) -> str | None:

        self.window.clear()
        self.window.refresh()

        while True:
            self.window.clear()
            self.print_menu()

            key = self.window.getch()

            if key == curses.KEY_UP:
                self.menu.move_up()

            elif key == curses.KEY_DOWN:
                self.menu.move_down()

            elif key in (curses.KEY_ENTER, 10, 13):
                return self.menu.selected_action()

            elif key == 27:
                return None

    def clear(self) -> None:
        self.window.clear()
        self.window.refresh()
