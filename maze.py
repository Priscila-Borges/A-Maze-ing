import random

class Maze:
	def __init__(self, height, width) -> None:
		self.height = height
		self.width = width	
	
	def gen_maze(self) -> list[[list[int]]]:
		self.maze = []
		for x in range(self.width):
			self.row = []
			for y in range(self.height):
				self.row.append(x)
			self.maze.append(self.row)
		return self.maze

