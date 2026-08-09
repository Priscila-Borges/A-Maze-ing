class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells: dict[tuple[int, int], int] = {}

        for x in range(self.width):
            for y in range(self.height):
                self.cells[(x, y)] = 15

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

        for (x, y), value in self.cells.items():
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
