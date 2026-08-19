# Built-in modules
import random

# Project modules
from dataclasses import dataclass
from parser import Config, parse_config
from mazegen import Maze, MazeGenerator


@dataclass
class MazeState:
    """Store the current maze, its configuration, and rendered form."""
    config_file: str
    config_data: Config
    maze_string: str
    maze: Maze
    reserved_cells: set[tuple[int, int]]


'''
Moved the write file workflow out of a_maze_ing.py so it can be
reused both at startup and when regenerating a maze from the UI.
'''


def write_output_file(
                    file_path: str,
                    maze: Maze,
                    maze_entry: tuple[int, int],
                    maze_exit: tuple[int, int],
                    path: str = "",
                    ) -> None:

    hex_grid = maze.to_hex_grid()

    lines = [
        hex_grid,
        "",
        f"{maze_entry[0]},{maze_entry[1]}",
        f"{maze_exit[0]},{maze_exit[1]}",
        path,
    ]

    with open(file_path, "w") as file:
        file.write("\n".join(lines))


'''
Moved the maze-building workflow out of a_maze_ing.py so it can be
reused both at startup and when regenerating a maze from the UI.
'''


def build_maze(config_file: str) -> MazeState:
    """Parse the configuration, generate a maze, and return its state."""

    config_data = parse_config(config_file)

    if config_data.seed is not None:
        random.seed(config_data.seed)

    grid = Maze(config_data.width, config_data.height)
    builder = MazeGenerator(
        grid,
        config_data.maze_entry,
        config_data.maze_exit
    )

    builder.generate()

    if not config_data.perfect:
        builder.make_imperfect()

    maze_string = grid.render()

    write_output_file(
                    config_data.output_file,
                    grid,
                    config_data.maze_entry,
                    config_data.maze_exit,
                    ""
                    )

    return MazeState(
            config_file=config_file,
            config_data=config_data,
            maze_string=maze_string,
            maze=grid,
            reserved_cells=builder.reserved_cells
            )


def regenerate_maze(state: MazeState) -> MazeState:
    new_state = build_maze(state.config_file)
    return new_state
