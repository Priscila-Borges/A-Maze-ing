import curses
import ui.actions
from ui.maze_window import MazeWindow
from ui.menu_window import Menu
from ui.menu_window import MenuPanel
from maze_builder import build_maze
from maze_builder import MazeState
from maze_builder import write_output_file
from maze_builder import regenerate_maze

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


def validate_layout(
                    state: MazeState,
                    menu: Menu,
                    screen: curses.window
                    ) -> None:

    """Check that the menu and maze fit inside the current terminal.

    Raises a ValueError with the maximum supported maze dimensions
    when the current layout is too large for the terminal.
    """

    screen_h, screen_w = screen.getmaxyx()

    maze_panel_h, maze_panel_w = MenuPanel.calculate_size(menu)

    spacing = 2
    cell_h = MazeWindow.CELL_H
    cell_w = MazeWindow.CELL_W

    border_h = cell_h
    border_w = cell_w

    maze_h = state.config_data.height
    maze_w = state.config_data.width

    maze_win_h, maze_win_w = MazeWindow.calculate_size(maze_h, maze_w)

    required_screen_h = max(maze_panel_h, maze_win_h) + spacing * 2
    required_screen_w = maze_win_w + maze_panel_w + spacing * 3

    available_screen_h = (screen_h - spacing * 2)
    available_screen_w = (screen_w - maze_panel_w - spacing * 3)

    max_maze_h = (available_screen_h - border_h - 1) // cell_h
    max_maze_w = (available_screen_w - border_w - 1) // cell_w

    if required_screen_h > screen_h or required_screen_w > screen_w:

        message = (
            "\nMaze:\n  "
            "Current size:                "
            f"h = {state.config_data.height}   and    "
            f"w = {state.config_data.width}\n"
            "  Max size for this terminal:  "
            f"h = {max_maze_h}   and    "
            f"w = {max_maze_w}\n"
            )

        raise ValueError(
            "The UI layout does not fit in the terminal. "
            "Change terminal size or change maze dimensions.\n"
            f"{message}"
            )


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


def run_main_screen(main_menu: Menu,
                    maze_menu: Menu,
                    state: MazeState,
                    screen: curses.window,
                    ) -> None:

    """Run the main menu and coordinate navigation between screens.

    Handles the "Generate maze" and "Quit" actions from the main menu,
    and processes "Return", "Regenerate", and "Quit" results from the
    maze screen.
    """

    main_panel = MenuPanel(main_menu, "center", screen)

    while True:                                     # MAIN LOOP
        selection = main_panel.navigate_menu()
        main_panel.clear()

        if selection == "Generate maze":
            while True:                               # MAZE LOOP
                result = run_maze_screen(maze_menu, state, screen)

                if result == "Quit":
                    return
                elif result == "Return":
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
            ui.actions.quit_action(screen)
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

    maze_panel = MenuPanel(maze_menu, "left", screen)
    maze_win = MazeWindow(maze_panel, state, screen)

    while True:
        selection = maze_panel.navigate_menu()

        if selection == "Solve":
            pass
        elif selection == "Regenerate":
            return "Regenerate"
        elif selection == "Change wall color":
            ui.actions.change_color_action(maze_win)
            continue
        elif selection == "Return":
            ui.actions.return_action(maze_panel, screen)
            return "Return"
        elif selection is None or selection == "Quit":
            ui.actions.quit_action(screen)
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
