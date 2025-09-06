import random

class Maze:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self._init_walls()
        self._init_start_target()

    def _init_walls(self) -> None:
        self.H = [[True for _ in range(self.cols)] for _ in range(self.rows + 1)]
        self.V = [[True for _ in range(self.cols + 1)] for _ in range(self.rows)]

    def _init_start_target(self) -> None:
        self.target = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
        border_cells = [(0, i) for i in range(self.cols)] + \
                       [(self.rows - 1, i) for i in range(self.cols)] + \
                       [(i, 0) for i in range(1, self.rows - 1)] + \
                       [(i, self.cols - 1) for i in range(1, self.rows - 1)]
        self.start = random.choice(border_cells)
        sy, sx = self.start
        if sy == 0:
            self.H[0][sx] = False
        elif sy == self.rows - 1:
            self.H[self.rows][sx] = False
        elif sx == 0:
            self.V[sy][0] = False
        elif sx == self.cols - 1:
            self.V[sy][self.cols] = False

    def generate(self) -> None:
        stack = []
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        start_y = random.randint(0, self.rows - 1)
        start_x = random.randint(0, self.cols - 1)
        stack.append((start_y, start_x))
        visited[start_y][start_x] = True
        while stack:
            y, x = stack[-1]
            neighbors = []
            # Check each direction for unvisited neighbors
            if y > 0 and not visited[y-1][x]:
                neighbors.append(('N', y-1, x))
            if y < self.rows-1 and not visited[y+1][x]:
                neighbors.append(('S', y+1, x))
            if x > 0 and not visited[y][x-1]:
                neighbors.append(('W', y, x-1))
            if x < self.cols-1 and not visited[y][x+1]:
                neighbors.append(('E', y, x+1))
            if neighbors:
                direction, ny, nx = random.choice(neighbors)
                # Remove wall between current and neighbor
                if direction == 'N':
                    self.H[y][x] = False
                elif direction == 'S':
                    self.H[y+1][x] = False
                elif direction == 'W':
                    self.V[y][x] = False
                elif direction == 'E':
                    self.V[y][x+1] = False
                visited[ny][nx] = True
                stack.append((ny, nx))
            else:
                stack.pop()

    def setup(self) -> None:
        self._init_walls()
        self.generate()
        self._init_start_target()

    def neighbors(self, y: int, x: int) -> list[tuple[int, int]]:
        nbrs = []
        # Check each direction for open passage
        if y > 0 and not self.H[y][x]:
            nbrs.append((y-1, x))
        if y < self.rows-1 and not self.H[y+1][x]:
            nbrs.append((y+1, x))
        if x > 0 and not self.V[y][x]:
            nbrs.append((y, x-1))
        if x < self.cols-1 and not self.V[y][x+1]:
            nbrs.append((y, x+1))
        return nbrs
