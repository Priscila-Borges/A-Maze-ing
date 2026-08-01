from parser import parse_config
from maze import Maze, Constructor

def main():
	config_data = parse_config("config.txt")
	test_maze = Maze(config_data.width, config_data.height)
	builder = Constructor(test_maze, config_data.maze_entry[0], config_data.maze_entry[1])
	builder.generate()
	
	test_maze.print_matrix()


if __name__ == "__main__":
	main()