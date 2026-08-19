# Built-in modules
import curses
from typing import Literal


MenuPositions = Literal["center", "left"]


class Menu:
    """Store menu content and manage the currently selected action."""

    def __init__(
                self,
                header: str,
                actions: list[str]
                ) -> None:
        """Initialize a menu with a header and a list of actions."""

        self.header = header
        self.actions = actions
        self.selected_row_idx = 0

    def move_up(self) -> None:
        """Move the selection up by one action when possible."""

        if self.selected_row_idx > 0:
            self.selected_row_idx -= 1

    def move_down(self) -> None:
        """Move the selection down by one action when possible."""

        if self.selected_row_idx < len(self.actions) - 1:
            self.selected_row_idx += 1

    def selected_action(self) -> str:
        """Return the currently selected action."""

        return self.actions[self.selected_row_idx]


class MenuWindow():
    """Display an interactive menu inside a curses window."""

    def __init__(
                self,
                menu: Menu,
                position: MenuPositions,
                screen: curses.window
                ) -> None:
        """Initialize and display a menu panel at the requested position."""

        self.menu = menu
        self.position = position
        self.h, self.w = self.calculate_size(menu)
        self.top, self.left, self.right = self._calculate_position(screen)
        self._create_window()
        self._print_menu()

    @staticmethod
    def calculate_size(
                    menu: Menu
                    ) -> tuple[int, int]:
        """Calculate the panel size required to display the menu."""

        vertical_padding = 6
        horizontal_padding = 4

        menu_win_h: int = len(menu.actions) + vertical_padding
        width_actions: int = max(len(row) for row in menu.actions)
        width_header: int = len(menu.header)
        menu_win_w = max(width_actions, width_header) + horizontal_padding

        return (menu_win_h, menu_win_w)

    def _calculate_position(
                        self,
                        screen: curses.window
                        ) -> tuple[int, int, int]:
        """Calculate the panel position and ensure it fits on the screen."""

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

    def _create_window(
                        self
                        ) -> None:
        """Create and configure the curses window used by the panel."""

        self.window = curses.newwin(self.h, self.w, self.top, self.left)

        self.window.bkgd(" ", curses.color_pair(1))
        self.window.keypad(True)
        self.window.border()
        self.window.refresh()

    def _print_menu(
                    self
                    ) -> None:
        """Draw the menu and highlight the currently selected action."""

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
        """Handle keyboard navigation and return the selected action."""

        self.window.clear()
        self.window.refresh()

        while True:
            self.window.clear()
            self._print_menu()

            key = self.window.getch()

            if key == curses.KEY_UP:
                self.menu.move_up()

            elif key == curses.KEY_DOWN:
                self.menu.move_down()

            elif key in (curses.KEY_ENTER, 10, 13):
                return self.menu.selected_action()

            elif key == 27:
                return None

    def clear(
            self
            ) -> None:
        """Clear the panel window from the screen."""

        self.window.clear()
        self.window.refresh()
