import curses
import time

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
                stdscr: curses.window,
                window: curses.window
                ) -> None:

    window.clear()
    window.refresh()
    del window

    stdscr.touchwin()
    stdscr.refresh()

