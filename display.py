import time
import curses
from typing import Literal
from parser import Config
import menu_actions

MenuPosition = Literal["center", "left"]


def initialize_colors(
                    ) -> None:

    curses.start_color()

    if curses.can_change_color():
        curses.init_color(10, 59, 106, 169)
        curses.init_color(11, 882, 682, 86)
        curses.init_pair(1, 11, 10)
        curses.init_pair(2, 10, 11)
        curses.init_pair(3, curses.COLOR_GREEN, 10)
    else:
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)


def create_background(
                    screen: curses.window
                    ) -> None:

    h, w = screen.getmaxyx()

    text_top = "Welcome to A-Maze-ing!"
    text_bottom = "Project made by varaniba and pride-ol"
    x_text_top = w//2 - len(text_top)//2
    x_text_bottom = w//2 - len(text_bottom)//2

    curses.curs_set(0)
    screen.bkgd(" ", curses.color_pair(1))
    screen.border()
    screen.addstr(0, x_text_top, text_top)
    screen.addstr(h - 1, x_text_bottom, text_bottom)
    screen.refresh()

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
                position: MenuPosition,
                screen: curses.window
                ) -> None:

        self.menu = menu
        self.position = position
        self.h, self.w = self.calculate_size(menu.header, menu.actions)
        self.top, self.left, self.right = self.calculate_position(screen)
        self.create_window()

    @staticmethod
    def calculate_size(
                    header: str,
                    actions: list[str]
                    ) -> tuple[int, int]:

        vertical_padding = 6
        horizontal_padding = 4

        height: int = len(actions) + vertical_padding
        width_actions: int = max(len(row) for row in actions)
        width_header: int  = len(header)
        width = max(width_actions, width_header) + horizontal_padding

        return (height, width)

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
            raise ValueError("Terminal is too small to display the program")

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

    def handle_user_input(
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


class MazeWindow():

    def __init__(
            self,
            maze_h: int,
            maze_w: int,
            maze_panel: MenuPanel,
            screen: curses.window
            ) -> None:

        self.h = maze_h + 2
        self.w = maze_w + 2
        self.top, self.left, self.right = self.calculate_position(maze_panel, screen)
        self.create_window()

    def calculate_position(
                        self,
                        maze_panel: MenuPanel,
                        screen: curses.window
                        ) -> tuple[int, int, int]:

        screen_h, screen_w = screen.getmaxyx()
        padding = 1

        top = screen_h//2 - self.h//2
        left = maze_panel.right + screen_w//2 - maze_panel.right//2 - self.w//2 - padding
        right = left + self.w

        if (
            top < 0
            or left < 0
            or right > screen_w
            or top + self.h > screen_h
            or left + self.w > screen_w
            or right + padding > screen_w
            ):
            message = f"top = {top} < 0\nor left = {left} < 0\nor right = {right} > screen_w = {screen_w}\nor top = {top} + h= {self.h} >  screen_h = {screen_h}\nor  left = {left} + w = {self.w }> screen_w = {screen_w}\nor right = {right} + padding = {padding} > screen_w = {screen_w}"
            raise ValueError(f"Limits surpassed\n{message}")

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


def validating_terminal_size(
                            screen: curses.window,
                            config_data: Config,
                            maze_string: str,
                            header: str,
                            actions: list[str],
                            ) -> None:

    screen_h, screen_w = screen.getmaxyx()

    maze_menu_h, maze_menu_w = MenuPanel.calculate_size(header, actions)
    outer_padding = 4
    maze_rows = maze_string.splitlines()
    rendered_h = len(maze_rows)
    rendered_w = max(len(line) for line in maze_rows)

    required_h = rendered_h + outer_padding
    required_w = rendered_w + outer_padding * 2 + maze_menu_w + 2
    max_rendered_h = screen_h - outer_padding
    max_rendered_w = screen_w - outer_padding * 2 - maze_menu_w
    max_input_h = max_rendered_h // 2 - 1
    max_input_w = max_rendered_w // 4 - 1

    if required_h > screen_h or required_w > screen_w:

        message_1 = f"\nTerminal:\n  Current size:   h = {screen_h}   and    w = {screen_w}\n"
        message_2 = f"  Required size:  h = {required_h}   and    w = {required_w}"

        message_3 = f"\nMaze:\n  Current size:                h = {config_data.height}   and    w = {config_data.width}\n"
        message_4 = f"  Max size for this terminal:  h = {max_input_h}   and    w = {max_input_w}\n"
        complete_message = message_1 + message_2 + message_3 + message_4

        raise ValueError(f"Terminal too small. Change terminal size or change maze dimensions.\n{complete_message}")


def run_display(
                stdscr: curses.window,
                config_data: Config,
                maze_string: str
                ) -> None:

    header = "Actions:"

    main_actions: list[str] = [
        "Generate maze",
        "Quit"
        ]

    maze_actions: list[str] = [
        "Solve",
        "Regenerate",
        "Change wall color",
        "Return",
        "Quit"
        ]

    '''
    1. Maze logical size
   width = number of maze cells
    each maze cell takes 4 terminal columns horizontally
   height = number of maze cells
    each cell takes 2 terminal rows vertically

    2. Renderer grid size
    grid_width = width * 2 + 1
    grid_height = height * 2 + 1

    3. Actual curses/terminal size
    rendered_width = width * 4 + 1
        number of terminal columns
    rendered_height = height * 2 + 1
        number of terminal rows
    '''

    validating_terminal_size(stdscr, config_data, maze_string, header, maze_actions)
    initialize_colors()
    create_background(stdscr)

    maze_rows = maze_string.splitlines()
    rendered_h = len(maze_rows)
    rendered_w = max(len(line) for line in maze_rows)

    main_menu = Menu(header, main_actions)
    main_panel = MenuPanel(main_menu, "center", stdscr)

    while True:
        selection = main_panel.handle_user_input()

        main_panel.clear()
        color_style = curses.color_pair(1)

        if selection is None or selection == "Quit":
            menu_actions.quit_action(stdscr)
            return

        if selection == "Generate maze":
            maze_menu = Menu(header, maze_actions)
            maze_panel = MenuPanel(maze_menu, "left", stdscr)
            maze_win = MazeWindow(rendered_h, rendered_w, maze_panel, stdscr)

            for y, line in enumerate(maze_rows):
                maze_win.window.addstr(y + 1, 1, line, color_style)
                maze_win.window.refresh()

            while True:
                maze_selection = maze_panel.handle_user_input()

                if maze_selection == "Solve":
                    pass
                elif maze_selection == "Regenerate":
                    pass
                elif maze_selection == "Change wall color":
                    # color_style = curses.color_pair(3)
                    # y = 0
                    # for y, line in enumerate(maze_rows):
                    #     maze_win.window.addstr(y + 1, 1, line, color_style)
                    #     maze_win.window.refresh()
                    pass
                elif maze_selection == "Return":
                    menu_actions.return_action(stdscr, maze_panel.window)
                    break
                elif maze_selection is None or maze_selection == "Quit":
                    menu_actions.quit_action(stdscr)
                    return


def start_display(
                config_data: Config,
                maze_string: str
                ) -> None:

    try:
        curses.wrapper(run_display, config_data, maze_string)

    except ValueError as err:
        raise ValueError(f"{err}")


    """
    The wrapper:
    1. Starts curses
    2. Creates the main terminal window stdscr
    3. Calls the function run_display(stdscr: curses.window)
    4. Restores the terminal when run_display finishes or crashes.
    """
