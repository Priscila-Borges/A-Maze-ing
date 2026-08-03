from parser import parse_config
from maze import Maze, Constructor


def main() -> None:
    config_data = parse_config("config.txt")
    grid = Maze(config_data.width, config_data.height)
    builder = Constructor(
        grid, config_data.maze_entry[0], config_data.maze_entry[1]
    )
    builder.generate()
    print(grid.render())


if __name__ == "__main__":
    main()
