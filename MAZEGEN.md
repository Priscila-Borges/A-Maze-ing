mazegen Documentation
mazegen is a standalone, reusable Python library for creating 2D grid mazes and computing their solutions.

Quickstart Example
Python
import random
from mazegen import Maze, MazeGenerator, MazeSolver

# 1. Set seed for deterministic generation (optional)
random.seed(42)

# 2. Instantiate grid structure with custom dimensions
maze = Maze(width=20, height=15)

# 3. Instantiate generator with entry and exit parameters
generator = MazeGenerator(
    maze=maze,
    entry=(0, 0),
    exit=(19, 14)
)
generator.generate()

# 4. Access raw maze structure
grid_cells = maze.cells

# 5. Compute and access the solution path
solver = MazeSolver(maze, entry=(0, 0), exit=(19, 14))
solution_path = solver.solve()

print(f"Generated a {maze.width}x{maze.height} maze.")
print(f"Solution path step count: {len(solution_path)}")
Custom Parameters
Maze(width: int, height: int): Configures the total grid dimensions.

width: Total number of horizontal columns.

height: Total number of vertical rows.

MazeGenerator(maze: Maze, entry: tuple[int, int], exit: tuple[int, int]):

maze: Target Maze instance to carve.

entry: Starting coordinate tuple (x, y).

exit: Ending coordinate tuple (x, y).

Seed / Reproducibility: Call random.seed(your_seed) before running generator.generate() to produce identical mazes deterministically across runs.

Accessing Structure & Solutions
Grid Structure (maze.cells)
Access raw structural data directly through the maze.cells attribute.

Type: dict[tuple[int, int], int] mapping coordinate pairs (x, y) to 4-bit wall bitmasks.

Bitmask Definitions:

1 (North wall)

2 (East wall)

4 (South wall)

8 (West wall)

Python
# Check wall configurations at entry cell
entry_walls = maze.cells[(0, 0)]
print(f"Cell (0,0) wall bitmask: {entry_walls}")
Solution Path (MazeSolver.solve())
Pass the generated Maze into MazeSolver along with start and exit coordinates to derive a path.

Returns: A list of coordinate tuples [(x1, y1), (x2, y2), ...] representing the sequential path from start to finish.

Python
solver = MazeSolver(maze, entry=(0, 0), exit=(19, 14))
path = solver.solve()

# Example path output: [(0, 0), (0, 1), (1, 1), ..., (19, 14)]
print(f"Start: {path[0]}, Finish: {path[-1]}")