import random
import time
import curses
from ui.maze_window import MazeWindow
from ui.menu_window import MenuPanel


def quit_action(
                stdscr: curses.window
                ) -> None:

    text = "see ya!"
    y, x = stdscr.getmaxyx()

    stdscr.clear()
    stdscr.bkgd(" ", curses.color_pair(1))
    stdscr.border()
    stdscr.addstr(y // 2, x // 2 - len(text) // 2, text)
    stdscr.refresh()

    time.sleep(1)


def return_action(
                menu_panel: MenuPanel,
                stdscr: curses.window
                ) -> None:

    del menu_panel

    stdscr.touchwin()
    stdscr.refresh()


def change_color_action(
                    maze_win: MazeWindow
                    ) -> None:

    foreground, background = curses.pair_content(1)

    colors = [
        curses.COLOR_RED,
        curses.COLOR_GREEN,
        curses.COLOR_YELLOW,
        curses.COLOR_MAGENTA,
        curses.COLOR_CYAN,
        curses.COLOR_WHITE,
        ]

    if foreground in colors:
        colors.remove(foreground)
    new_foreground = random.choice(colors)
    curses.init_pair(3, new_foreground, background)
    maze_win.color_style = curses.color_pair(3)
    maze_win.print_maze()
    maze_win.print_entry_exit()
    maze_win.print_42()
