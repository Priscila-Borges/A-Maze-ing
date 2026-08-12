import random
import sys
from parser import parse_config
from mazegen.maze import Maze
from mazegen.generator import MazeGenerator
from display import start_display


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


def main() -> None:
    if len(sys.argv) != 2:
        print("Error: Missing configuration file.", file=sys.stderr)
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        config_data = parse_config(config_file)

        if config_data.seed is not None:
            random.seed(config_data.seed)

        grid = Maze(config_data.width, config_data.height)
        builder = MazeGenerator(grid, config_data.maze_entry)

        builder.generate()

        if not config_data.perfect:
            builder.make_imperfect()

        maze_string = grid.render()
        # print(maze_string)
        start_display(config_data, maze_string)

        write_output_file(
            file_path=config_data.output_file,
            maze=grid,
            maze_entry=config_data.maze_entry,
            maze_exit=config_data.maze_exit,
            path="",
        )

    except FileNotFoundError:
        print(f"Error: File '{config_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print("Error: Permission denied when reading"
              f" '{config_file}'.", file=sys.stderr)
        sys.exit(1)
    except ValueError as err:
        print(f"Configuration Error: {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"Unexpected Error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
