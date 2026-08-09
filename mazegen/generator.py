import random
from mazegen.maze import Maze


class MazeGenerator:
    def __init__(self, maze: Maze, entry: tuple[int, int]) -> None:
        self.maze = maze
        self.entry = entry
        self.visited: set[tuple[int, int]] = {entry}
        self.stack: list[tuple[int, int]] = [entry]
        self.ways = {
            "N": (0, -1, 1, 4),
            "E": (1, 0, 2, 8),
            "S": (0, 1, 4, 1),
            "W": (-1, 0, 8, 2),
        }

    # DFS algorithm to open the walls and create perfect maze
    def generate(self) -> None:
        while self.stack:
            curr_x, curr_y = self.stack[-1]
            neighbors = []

            for name, (dir_x, dir_y, curr_bit, n_bit) in self.ways.items():
                neighbor_x, neighbor_y = curr_x + dir_x, curr_y + dir_y

                if (
                    0 <= neighbor_x < self.maze.width
                    and 0 <= neighbor_y < self.maze.height
                ):
                    if (neighbor_x, neighbor_y) not in self.visited:
                        neighbors.append(
                            (neighbor_x, neighbor_y, curr_bit, n_bit)
                        )

            if neighbors:
                neighbor_x, neighbor_y, curr_bit, n_bit = random.choice(
                    neighbors
                )

                self.maze.cells[(curr_x, curr_y)] &= ~curr_bit
                self.maze.cells[(neighbor_x, neighbor_y)] &= ~n_bit

                self.visited.add((neighbor_x, neighbor_y))
                self.stack.append((neighbor_x, neighbor_y))

            else:
                self.stack.pop()

    def make_imperfect(self) -> None:
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if random.random() < 0.10:
                    direction = random.choice(["E", "S"])
                    dir_x, dir_y, curr_bit, n_bit = self.ways[direction]

                    neighbor_x = x + dir_x
                    neighbor_y = y + dir_y

                    if (
                        0 <= neighbor_x < self.maze.width
                        and 0 <= neighbor_y < self.maze.height
                    ):

                        self.maze.cells[(x, y)] &= ~curr_bit
                        self.maze.cells[(neighbor_x, neighbor_y)] &= ~n_bit
