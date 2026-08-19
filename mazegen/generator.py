import random
import sys
from mazegen.maze import Maze


class MazeGenerator:
    def __init__(
        self, maze: Maze, entry: tuple[int, int], exit: tuple[int, int]
    ) -> None:
        self.maze = maze
        self.entry = entry
        self.exit = exit
        self.reserved_cells = self._get_42_cells()
        self.visited: set[tuple[int, int]] = {entry}
        self.stack: list[tuple[int, int]] = [entry]
        self.ways = {
            "N": (0, -1, 1, 4),
            "E": (1, 0, 2, 8),
            "S": (0, 1, 4, 1),
            "W": (-1, 0, 8, 2),
        }

        for x, y in self.reserved_cells:
            self.visited.add((x, y))

    def _get_42_cells(self) -> set[tuple[int, int]]:
        """Returns the set of (x, y) coordinates forming the '42' logo.
        Omits the logo and logs to stderr if the grid is too small or if
        the entry/exit points collide with the pattern.
        """
        if self.maze.width < 7 or self.maze.height < 5:
            print(
                "Error: Maze size is too small for '42' pattern. "
                "Omitting pattern.",
                file=sys.stderr,
            )
            return set()

        cx = self.maze.width // 2
        cy = self.maze.height // 2

        # Offsets relative to center (dx, dy)
        offsets = [
            # Digit '4'
            (-3, -2),
            (-3, -1),
            (-3, 0),
            (-2, 0),
            (-1, 0),
            (-1, 1),
            (-1, 2),
            # Digit '2'
            (1, -2),
            (2, -2),
            (3, -2),
            (3, -1),
            (1, 0),
            (2, 0),
            (3, 0),
            (1, 1),
            (1, 2),
            (2, 2),
            (3, 2),
        ]

        reserved = set()
        for dx, dy in offsets:
            cell_x = cx + dx
            cell_y = cy + dy

            if (
                0 <= cell_x < self.maze.width
                and 0 <= cell_y < self.maze.height
            ):
                reserved.add((cell_x, cell_y))

        if self.entry in reserved or self.exit in reserved:
            print(
                "Error: Entry or exit point collides with '42' pattern. "
                "Omitting pattern.",
                file=sys.stderr,
            )
            return set()

        return reserved

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
            (0, 0),  # top-left
            (self.maze.width - 1, 0),  # top-right
            (0, self.maze.height - 1),  # bottom-left
            (self.maze.width - 1, self.maze.height - 1),  # bottom-right
            (center_x, center_y),  # center
        ]

        for x, y in key_cells:
            self._open_random_wall(x, y)

    def _create_loops(self) -> None:
        """Randomly knocks down interior walls to create loops."""
        for x in range(self.maze.width - 1):
            for y in range(self.maze.height - 1):
                if random.random() < 0.15:
                    self._open_random_wall(x, y)

    def _remove_dead_ends(self) -> None:
        """Repeatedly finds cells with 3 walls intact and opens one side
        until none remain.
        """
        has_dead_ends = True

        while has_dead_ends:
            has_dead_ends = False
            for x in range(self.maze.width):
                for y in range(self.maze.height):
                    if (x, y) in self.reserved_cells:
                        continue
                    if self._count_walls(x, y) == 3:
                        if self._open_random_wall(x, y):
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

    def _is_3x3_fully_open(self, bx: int, by: int) -> bool:
        """Checks if a 3x3 block starting at top-left corner (bx, by)
        has no internal walls.
        """
        east_wall = 2
        south_wall = 4

        for col in range(3):
            for row in range(3):
                cell_walls = self.maze.cells[(bx + col, by + row)]

                # Check East wall for the first 2 columns
                if col < 2 and (cell_walls & east_wall):
                    return False

                # Check South wall for the first 2 rows
                if row < 2 and (cell_walls & south_wall):
                    return False

        return True  # All internal walls are gone

    def _creates_3x3_open_area(
        self, x: int, y: int, nx: int, ny: int
    ) -> bool:
        """Checks if opening the wall between (x, y) and (nx, ny) forms
        any 3x3 open area.
        """
        # Find overlapping 3x3 block origins (bx, by) based on wall direction
        if nx != x:  # Horizontal movement
            col_range = (x - 1, x)
            row_range = (y - 2, y - 1, y)
        else:  # Vertical movement
            col_range = (x - 2, x - 1, x)
            row_range = (y - 1, y)

        for bx in col_range:
            for by in row_range:
                # Skip blocks that spill outside maze boundaries
                if (
                    0 <= bx
                    and (bx + 2) < self.maze.width
                    and 0 <= by
                    and (by + 2) < self.maze.height
                ):
                    if self._is_3x3_fully_open(bx, by):
                        return True

        return False

    def _open_random_wall(self, x: int, y: int) -> bool:
        """Attempts to break a CLOSED wall between (x, y) and a neighbor
        without creating a 3x3 room.
        """
        if (x, y) in self.reserved_cells:
            return False

        directions = list(self.ways.keys())
        random.shuffle(directions)

        for direction in directions:
            dx, dy, curr_bit, n_bit = self.ways[direction]
            nx, ny = x + dx, y + dy

            # Skip invalid neighbors or walls that are already open
            if not (0 <= nx < self.maze.width and 0 <= ny < self.maze.height):
                continue
            if (nx, ny) in self.reserved_cells:
                continue

            is_wall_closed = bool(self.maze.cells[(x, y)] & curr_bit)
            if not is_wall_closed:
                continue

            # Tentatively open the wall
            self.maze.cells[(x, y)] &= ~curr_bit
            self.maze.cells[(nx, ny)] &= ~n_bit

            # Check rule violation & rollback if necessary
            if self._creates_3x3_open_area(x, y, nx, ny):
                self.maze.cells[(x, y)] |= curr_bit  # Restore wall
                self.maze.cells[(nx, ny)] |= n_bit  # Restore wall
                continue

            # Success! Wall stays open
            return True

        return False
