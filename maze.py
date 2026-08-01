import random

class Maze:
	def __init__(self, width: int, height: int) -> None:
		self.width = width
		self.height = height
		self.maze: dict[tuple[int, int], int] = {}

		for x in range(self.width):
			for y in range(self.height):
				self.maze[(x, y)] = 15

	def print_matrix(self) -> None:
		for y in range(self.height):
			row = [self.maze[(x, y)] for x in range(self.width)]
			print(row)
	

class Constructor:
	def __init__(self, maze: Maze, start_x: int, start_y: int) -> None:
		self.maze = maze
		self.start_x = start_x
		self.start_y = start_y
		self.visited: set[tuple[int, int]] = {(start_x, start_y)}
		self.stack: list[tuple[int, int]] = [(start_x, start_y)]
		self.directions = {
			'N': (0, -1, 1, 4),
			'E': (1, 0, 2, 8),
			'S': (0, 1, 4, 1),
			'W': (-1, 0, 8, 2),
		}


	#DFS algorithm to open the walls and create the maze
	def generate(self) -> None:
		while self.stack:
			curr_x, curr_y = self.stack[-1]
			neighbors = []

			for name, (dir_x, dir_y, curr_bit, neighbor_bit) in self.directions.items():
				neighbor_x, neighbor_y = curr_x + dir_x, curr_y + dir_y

				if 0 <= neighbor_x < self.maze.width and 0 <= neighbor_y < self.maze.height:
					if (neighbor_x, neighbor_y) not in self.visited:
						neighbors.append((neighbor_x, neighbor_y, curr_bit, neighbor_bit))

			if neighbors:
				neighbor_x, neighbor_y, curr_bit, neighbor_bit = random.choice(neighbors)

				self.maze.maze[(curr_x, curr_y)] &= ~curr_bit
				self.maze.maze[(neighbor_x, neighbor_y)] &= ~neighbor_bit

				self.visited.add((neighbor_x, neighbor_y))
				self.stack.append((neighbor_x, neighbor_y))

			else:
				self.stack.pop()

