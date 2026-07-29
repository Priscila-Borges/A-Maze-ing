from parser import parse_config
from maze import Maze

def main():
	config_data = parse_config("config.txt")
	test1 = Maze(config_data.width, config_data.height)
	print(test1.gen_maze())


if __name__ == "__main__":
	main()