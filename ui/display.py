# Built-in modules
import curses

# Project modules
from maze_builder import MazeState, regenerate_maze
from ui.actions import quit_action, change_color_action
from ui.maze_window import MazeWindow
from ui.menu_window import Menu, MenuWindow
from ui.display_utils import (
                            draw_42_hint,
                            draw_maze_coordinates,
                            initialize_colors,
                            initialize_display,
                            validate_layout
                            )

MENU_HEADER = "Actions:"

MAIN_ACTIONS: list[str] = [
    "Generate maze",
    "Quit"
    ]

MAZE_ACTIONS: list[str] = [
    "Solve",
    "Regenerate",
    "Change wall color",
    "Return",
    "Quit"
    ]


def run_main_screen(
                    main_menu: Menu,
                    maze_menu: Menu,
                    state: MazeState,
                    screen: curses.window,
                    ) -> None:

    """Run the main menu and coordinate navigation between screens.

    Handles the "Generate maze" and "Quit" actions from the main menu,
    and processes "Return", "Regenerate", and "Quit" results from the
    maze screen.
    """

    main_menu_win = MenuWindow(main_menu, "center", screen)

    while True:                                     # MAIN LOOP
        selection = main_menu_win.navigate_menu()
        main_menu_win.clear()

        if selection == "Generate maze":

            while True:                               # MAZE LOOP
                result = run_maze_screen(maze_menu, state, screen)

                if result == "Quit":
                    quit_action(screen)
                    return

                elif result == "Return":
                    initialize_display(screen)
                    break

                elif result == "Regenerate":
                    try:
                        new_state = regenerate_maze(state)
                        validate_layout(
                                        new_state,
                                        maze_menu,
                                        screen
                                        )
                    except ValueError as err:
                        raise ValueError(
                            "Regeneration not possible.\n"
                            f"{err}"
                            )
                    else:
                        state = new_state
                        initialize_display(screen)
                    continue

        elif selection is None or selection == "Quit":
            quit_action(screen)
            return


def run_maze_screen(
                    maze_menu: Menu,
                    state: MazeState,
                    screen: curses.window,
                    ) -> str:

    """Run the maze screen until the user chooses another action.

    Returns the action that requires handling outside the maze screen,
    such as "Regenerate", "Return", or "Quit".
    """

    maze_menu_win = MenuWindow(maze_menu, "left", screen)
    maze_win = MazeWindow(maze_menu_win, state, screen)

    draw_maze_coordinates(maze_win, screen)
    draw_42_hint(state, screen)
    while True:
        selection = maze_menu_win.navigate_menu()

        if selection == "Solve":
            pass

        elif selection == "Regenerate":
            return "Regenerate"

        elif selection == "Change wall color":
            change_color_action(maze_win)
            continue

        elif selection == "Return":
            return "Return"

        elif selection is None or selection == "Quit":
            return "Quit"


def run_display(
                stdscr: curses.window,
                state: MazeState
                ) -> None:

    """Initialize the curses UI and start the main application screen."""

    curses.curs_set(0)

    main_menu = Menu(MENU_HEADER, MAIN_ACTIONS)
    maze_menu = Menu(MENU_HEADER, MAZE_ACTIONS)

    validate_layout(state, maze_menu, stdscr)

    initialize_colors()
    initialize_display(stdscr)

    run_main_screen(main_menu, maze_menu, state, stdscr)


def start_display(
                state: MazeState
                ) -> None:

    """Start the curses interface using curses.wrapper().

    The wrapper initializes curses, creates stdscr, calls run_display(),
    and restores the terminal when the program finishes or raises an error.
    """

    curses.wrapper(run_display, state)
