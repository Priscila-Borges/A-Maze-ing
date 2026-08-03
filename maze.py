import random


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.maze: dict[tuple[int, int], int] = {}

        for x in range(self.width):
            for y in range(self.height):
                self.maze[(x, y)] = 15

    def render(self) -> str:
        grid_height = self.height * 2 + 1
        grid_width = self.width * 2 + 1

        grid = []
        for grid_y in range(grid_height):
            row = []
            for grid_x in range(grid_width):
                if grid_x % 2 != 0:
                    row.append("   ")
                else:
                    row.append(" ")
            grid.append(row)

        for y in range(self.height + 1):
            for x in range(self.width + 1):
                grid[y * 2][x * 2] = "+"

        for (x, y), value in self.maze.items():
            grid_y = y * 2 + 1
            grid_x = x * 2 + 1

            if value & 1:
                grid[grid_y - 1][grid_x] = "---"
            if value & 2:
                grid[grid_y][grid_x + 1] = "|"
            if value & 4:
                grid[grid_y + 1][grid_x] = "---"
            if value & 8:
                grid[grid_y][grid_x - 1] = "|"

        lines = []
        for row in grid:
            lines.append("".join(row))

        return "\n".join(lines)


class Constructor:
    def __init__(self, maze: Maze, start_x: int, start_y: int) -> None:
        self.maze = maze
        self.start_x = start_x
        self.start_y = start_y
        self.visited: set[tuple[int, int]] = {(start_x, start_y)}
        self.stack: list[tuple[int, int]] = [(start_x, start_y)]
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

                self.maze.maze[(curr_x, curr_y)] &= ~curr_bit
                self.maze.maze[(neighbor_x, neighbor_y)] &= ~n_bit

                self.visited.add((neighbor_x, neighbor_y))
                self.stack.append((neighbor_x, neighbor_y))

            else:
                self.stack.pop()
