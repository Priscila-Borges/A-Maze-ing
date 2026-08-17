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
        self._open_key_locations()
        self._create_loops()
        self._remove_dead_ends()

    def _open_key_locations(self) -> None:
        center_x = self.maze.width // 2
        center_y = self.maze.height // 2

        key_cells = [
            (0, 0), #top-left
            (self.maze.width -1, 0), #top-right
            (0, self.maze.height -1), #bottom-left
            (self.maze.width -1, self.maze.height -1), #bottom-right
            (center_x, center_y), #center
        ]

        for x, y in key_cells:
            self._open_random_wall(x, y)

    def _create_loops(self) -> None:
        """Randomly knocks down interior walls to create loops."""
        for x in range(self.maze.width - 1):
            for y in range(self.maze.height -1):
                if random.random() < 0.15:
                    self._open_random_wall(x, y)

    def _remove_dead_ends(self) -> None:
        """Repeatedly finds cells with 3 walls intact and opens one side until none remain."""
        has_dead_ends = True

        while has_dead_ends:
            has_dead_ends = False
            for x in range(self.maze.width):
                for y in range(self.maze.height):
                    if self._count_walls(x, y) == 3:
                        self._open_random_wall(x, y)
                        has_dead_ends = True

    def _count_walls(self, x: int, y: int) -> int:
        """Counts how many of the 4 walls are closed for a cell."""
        cell_value = self.maze.cells[(x, y)]
        walls = 0

        if cell_value & 1:
            walls += 1
        if cell_value & 2:
            walls += 1
        if cell_value & 4:
            walls += 1
        if cell_value & 8:
            walls += 1

        return walls

    def _open_random_wall(self, x: int, y: int) -> None:
        """Attempts to break a CLOSED wall between cell (x, y) and a valid neighbor."""
        directions = list(self.ways.keys())
        random.shuffle(directions)

        for direction in directions:
            dx, dy, curr_bit, n_bit = self.ways[direction]
            nx, ny = x + dx, y + dy

            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                if self.maze.cells[(x, y)] & curr_bit:
                    self.maze.cells[(x, y)] &= ~curr_bit
                    self.maze.cells[(nx, ny)] &= ~n_bit
                    break
