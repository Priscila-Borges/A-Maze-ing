# Built-in modules
import curses

# Project modules
from maze_builder import MazeState
from ui.maze_window import MazeWindow
from ui.menu_window import Menu, MenuWindow


def validate_layout(
                    state: MazeState,
                    maze_menu: Menu,
                    screen: curses.window
                    ) -> None:

    """Check that the menu and maze fit inside the current terminal.

    Raises a ValueError with the maximum supported maze dimensions
    when the current layout is too large for the terminal.
    """

    scr_h, scr_w = screen.getmaxyx()

    menu_win_h, menu_win_w = MenuWindow.calculate_size(maze_menu)

    spacing = MazeWindow.CELL_W

    maze_h = state.config_data.height
    maze_w = state.config_data.width

    maze_win_h, maze_win_w = MazeWindow.calculate_size(
                                                    maze_h,
                                                    maze_w
                                                    )

    required_scr_h = max(menu_win_h, maze_win_h) + spacing * 2
    required_scr_w = maze_win_w + menu_win_w + spacing * 3

    available_h = (scr_h - spacing * 2)
    available_w = (scr_w - menu_win_w - spacing * 3)

    max_maze_h, max_maze_w = MazeWindow.calculate_max_size(
                                                        available_h,
                                                        available_w
                                                        )

    if required_scr_h > scr_h or required_scr_w > scr_w:

        message = (
            "\nTerminal:\n  "
            "Current size:                "
            f"{scr_h}x{scr_w}\n"
            "  Minimal required size:       "
            f"{required_scr_h}x{required_scr_w}\n"
            "\nMaze:\n  "
            "Current size:                "
            f"h = {maze_h}   and    "
            f"w = {maze_w}\n"
            "  Max size for this terminal:  "
            f"h = {max_maze_h}   and    "
            f"w = {max_maze_w}\n"
            )

        raise ValueError(
            "The UI layout does not fit in the terminal. "
            "Change terminal size or change maze dimensions.\n"
            f"{message}"
            )


def initialize_colors(
                    ) -> None:
    """Initialize the color pairs used by the curses interface.

    Uses custom colors when supported by the terminal and falls back
    to standard curses colors otherwise.
    """

    curses.start_color()

    if curses.can_change_color():
        curses.init_color(10, 59, 106, 169)
        curses.init_color(11, 882, 682, 86)
        curses.init_pair(1, 11, 10)
        curses.init_pair(2, 10, 11)

    else:
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)


def initialize_display(
                    screen: curses.window,
                    ) -> None:
    """Draw the main screen background, border, and project titles."""

    h, w = screen.getmaxyx()

    text_top = "Welcome to A-Maze-ing!"
    text_bottom = "Project made by varaniba and pride-ol"
    x_text_top = w//2 - len(text_top)//2
    x_text_bottom = w//2 - len(text_bottom)//2

    screen.clear()
    screen.bkgd(" ", curses.color_pair(1))
    screen.border()
    screen.addstr(0, x_text_top, text_top)
    screen.addstr(h - 1, x_text_bottom, text_bottom)
    screen.refresh()


def draw_maze_coordinates(
                        maze_win: MazeWindow,
                        screen: curses.window
                        ) -> None:
    """Draw the coordinates of the maze's cells next to the maze window."""

    cell_h = maze_win.CELL_H
    cell_w = maze_win.CELL_W

    top = maze_win.top
    left = maze_win.left
    right = maze_win.right

    grid_h = maze_win.h - cell_h - 1
    grid_w = maze_win.w - cell_w - 1
    start_x = left + cell_w
    start_y = top + cell_h

    dx = 0
    step = 1

    for column in range(0, grid_w, cell_w):
        cell = column//cell_w
        if cell % step == 0:
            if cell >= 10:
                dx = 1
            screen.addstr(top - 1, start_x + column - dx, str(cell))

    for row in range(0, grid_h, cell_h):
        cell = row//cell_h
        if cell % step == 0:
            screen.addstr(start_y + row, right + 1, str(cell))

    screen.refresh()


def draw_42_hint(
                state: MazeState,
                screen: curses.window
                ) -> None:
    """Draw a small hint about the hidden 42 pattern."""

    if not state.reserved_cells:
        lines = [
            "Looking for this?",
            "",
            "   4  4   22 ",
            "   4  4  2  2",
            "   4444    2 ",
            "      4   2  ",
            "      4  2222",
            "",
            "Make the maze bigger or "
            "move the entry and exit outside"
            " the pattern to see the 42 pattern!",
        ]

        screen_h, screen_w = screen.getmaxyx()

        start_y = screen_h - len(lines) - 2
        start_x = 2

        for i, line in enumerate(lines):
            try:
                screen.addstr(start_y + i, start_x, line)
            except curses.error:
                pass

        screen.refresh()
