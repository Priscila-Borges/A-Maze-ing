# Built-in modules
import curses

# Project modules
from maze_builder import MazeState
from ui.menu_window import MenuWindow


class MazeWindow():
    """Display the maze and its visual elements inside a curses window."""

    CELL_H = 2
    CELL_W = 4

    def __init__(
            self,
            maze_menu_win: MenuWindow,
            state: MazeState,
            screen: curses.window
            ) -> None:
        """Initialize and display the maze window beside the menu panel."""

        self.state = state
        self.maze_string = self.state.maze_string

        self.h, self.w = MazeWindow.calculate_size(
                                                self.state.config_data.height,
                                                self.state.config_data.width
                                                )
        self.top, self.left, self.right = self._calculate_position(
                                                                maze_menu_win,
                                                                screen
                                                                )
        self.color_style = curses.color_pair(1)
        self._create_window()
        self._print_maze()
        self._print_entry_exit()
        self._print_42()

    def redraw(self) -> None:
        self._print_maze()
        self._print_entry_exit()
        self._print_42()

    @classmethod
    def calculate_size(
                    cls,
                    maze_h: int,
                    maze_w: int
                    ) -> tuple[int, int]:
        """Calculate the window size required to display the maze."""

        grid_h = maze_h * cls.CELL_H + 1
        grid_w = maze_w * cls.CELL_W + 1
        maze_win_h = grid_h + cls.CELL_H
        maze_win_w = grid_w + cls.CELL_W

        return (maze_win_h, maze_win_w)

    @classmethod
    def calculate_max_size(
                        cls,
                        available_h: int,
                        available_w: int
                        ) -> tuple[int, int]:
        """Calculate the maximal maze size to display on this window."""

        max_grid_h = available_h - cls.CELL_H
        max_grid_w = available_w - cls.CELL_W
        max_maze_h = (max_grid_h - 1)//cls.CELL_H
        max_maze_w = (max_grid_w - 1)//cls.CELL_W

        return (max_maze_h, max_maze_w)

    def _calculate_position(
                        self,
                        maze_menu_win: MenuWindow,
                        screen: curses.window
                        ) -> tuple[int, int, int]:
        """Calculate the maze window position and ensure it fits on screen."""

        screen_h, screen_w = screen.getmaxyx()
        padding = 1

        top = (screen_h - self.h)//2
        left = (
                maze_menu_win.right
                + (screen_w - maze_menu_win.right)//2
                - self.w//2
                - padding
                )
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
                        "Terminal size changed. The maze no longer fits.\n"
                        )

        else:
            return (top, left, right)

    def _create_window(
                    self
                    ) -> None:
        """Create and configure the curses window used to display the maze."""

        self.window = curses.newwin(self.h, self.w, self.top, self.left)

        self.window.bkgd(" ", curses.color_pair(1))
        self.window.keypad(True)
        self.window.border()
        self.window.refresh()

    def _print_maze(
                self
                ) -> None:
        """Draw the maze walls inside the maze window."""

        y_axis_walls = self.CELL_H//2
        x_axis_walls = self.CELL_W//2

        maze_lines = self.maze_string.splitlines()
        for y, line in enumerate(maze_lines):
            self.window.addstr(
                            y_axis_walls + y,
                            x_axis_walls,
                            line,
                            self.color_style
                            )

        self.window.refresh()

    def _print_entry_exit(
                self
                ) -> None:
        """Draw the maze entry and exit markers at their cell positions."""

        y_axis_path = self.CELL_H
        x_axis_path = self.CELL_W - 1

        self.entry_x, self.entry_y = self.state.config_data.maze_entry
        self.exit_x, self.exit_y = self.state.config_data.maze_exit

        y_maze_entry = y_axis_path + self.entry_y * self.CELL_H
        x_maze_entry = x_axis_path + self.entry_x * self.CELL_W

        y_maze_exit = y_axis_path + self.exit_y * self.CELL_H
        x_maze_exit = x_axis_path + self.exit_x * self.CELL_W

        self.window.addstr(y_maze_entry,
                           x_maze_entry,
                           "^-^",
                           curses.color_pair(2)
                           )
        self.window.addstr(y_maze_exit,
                           x_maze_exit,
                           "T^T",
                           curses.color_pair(2)
                           )
        self.window.refresh()

    def _print_42(
                self
                ) -> None:
        """Highlight the cells reserved for the 42 pattern."""

        pattern = self.state.reserved_cells

        for cell in pattern:
            y = (cell[1] + 1) * self.CELL_H
            x = (cell[0] + 1) * self.CELL_W - 1
            self.window.addstr(y, x, "   ", curses.color_pair(2))
        self.window.refresh()
