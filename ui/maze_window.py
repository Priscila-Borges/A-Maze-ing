import curses
from ui.menu_window import MenuPanel
from maze_builder import MazeState


class MazeWindow():

    CELL_H = 2
    CELL_W = 4

    def __init__(
            self,
            maze_panel: MenuPanel,
            state: MazeState,
            screen: curses.window
            ) -> None:

        self.state = state
        self.maze_string = self.state.maze_string

        self.h, self.w = MazeWindow.calculate_size(
                                                self.state.config_data.height,
                                                self.state.config_data.width
                                                )
        self.top, self.left, self.right = self.calculate_position(
                                                                maze_panel,
                                                                screen
                                                                )
        self.color_style = curses.color_pair(1)
        self.create_window()
        self.print_maze()
        self.print_entry_exit()
        self.print_42()

    @classmethod
    def calculate_size(
                    cls,
                    maze_h: int,
                    maze_w: int
                    ) -> tuple[int, int]:

        grid_h = maze_h * cls.CELL_H + 1
        grid_w = maze_w * cls.CELL_W + 1
        maze_win_h = grid_h + cls.CELL_H
        maze_win_w = grid_w + cls.CELL_W

        return (maze_win_h, maze_win_w)

    def calculate_position(
                        self,
                        maze_panel: MenuPanel,
                        screen: curses.window
                        ) -> tuple[int, int, int]:

        screen_h, screen_w = screen.getmaxyx()
        padding = 1

        top = (screen_h - self.h)//2
        left = (
                maze_panel.right
                + (screen_w - maze_panel.right)//2
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

    def create_window(
                    self
                    ) -> None:

        self.window = curses.newwin(self.h, self.w, self.top, self.left)

        self.window.bkgd(" ", curses.color_pair(1))
        self.window.keypad(True)
        self.window.border()
        self.window.refresh()

    def print_maze(
                self
                ) -> None:

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

    def print_entry_exit(
                self
                ) -> None:

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

    def print_42(
                self
                ) -> None:

        pattern = self.state.reserved_cells

        for cell in pattern:
            y = (cell[1] + 1) * self.CELL_H
            x = (cell[0] + 1) * self.CELL_W - 1
            self.window.addstr(y, x, "   ", curses.color_pair(2))
        self.window.refresh()
