import heapq
from collections import deque

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze

    def dijkstra_steps(self):
        sy, sx = self.maze.start
        ty, tx = self.maze.target
        dist = [[float('inf') for _ in range(self.maze.cols)] for _ in range(self.maze.rows)]
        prev = [[None for _ in range(self.maze.cols)] for _ in range(self.maze.rows)]
        dist[sy][sx] = 0
        heap = [(0, sy, sx)]
        visited = set()
        while heap:
            d, y, x = heapq.heappop(heap)
            if (y, x) in visited:
                continue
            visited.add((y, x))
            yield (y, x, [row[:] for row in prev])
            if (y, x) == (ty, tx):
                break
            for ny, nx in self.maze.neighbors(y, x):
                if dist[ny][nx] > d + 1:
                    dist[ny][nx] = d + 1
                    prev[ny][nx] = (y, x)
                    heapq.heappush(heap, (dist[ny][nx], ny, nx))
        path = []
        cy, cx = ty, tx
        while (cy, cx) != (sy, sx):
            path.append((cy, cx))
            cy, cx = prev[cy][cx]
            if cy is None or cx is None:
                return []
        path.append((sy, sx))
        path.reverse()
        yield ('done', path, prev)

    def astar_steps(self):
        sy, sx = self.maze.start
        ty, tx = self.maze.target
        def heuristic(y, x):
            return abs(y - ty) + abs(x - tx)
        dist = [[float('inf') for _ in range(self.maze.cols)] for _ in range(self.maze.rows)]
        prev = [[None for _ in range(self.maze.cols)] for _ in range(self.maze.rows)]
        dist[sy][sx] = 0
        heap = [(heuristic(sy, sx), 0, sy, sx)]
        visited = set()
        while heap:
            f, d, y, x = heapq.heappop(heap)
            if (y, x) in visited:
                continue
            visited.add((y, x))
            yield (y, x, [row[:] for row in prev])
            if (y, x) == (ty, tx):
                break
            for ny, nx in self.maze.neighbors(y, x):
                if dist[ny][nx] > d + 1:
                    dist[ny][nx] = d + 1
                    prev[ny][nx] = (y, x)
                    heapq.heappush(heap, (dist[ny][nx] + heuristic(ny, nx), dist[ny][nx], ny, nx))
        path = []
        cy, cx = ty, tx
        while (cy, cx) != (sy, sx):
            path.append((cy, cx))
            cy, cx = prev[cy][cx]
            if cy is None or cx is None:
                return []
        path.append((sy, sx))
        path.reverse()
        yield ('done', path, prev)

    def bfs_steps(self):
        sy, sx = self.maze.start
        ty, tx = self.maze.target
        visited = [[False for _ in range(self.maze.cols)] for _ in range(self.maze.rows)]
        prev = [[None for _ in range(self.maze.cols)] for _ in range(self.maze.rows)]
        queue = deque()
        queue.append((sy, sx))
        visited[sy][sx] = True
        while queue:
            y, x = queue.popleft()
            yield (y, x, [row[:] for row in prev])
            if (y, x) == (ty, tx):
                break
            for ny, nx in self.maze.neighbors(y, x):
                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    prev[ny][nx] = (y, x)
                    queue.append((ny, nx))
        path = []
        cy, cx = ty, tx
        while (cy, cx) != (sy, sx):
            path.append((cy, cx))
            cy, cx = prev[cy][cx]
            if cy is None or cx is None:
                return []
        path.append((sy, sx))
        path.reverse()
        yield ('done', path, prev)

    def dfs_steps(self):
        sy, sx = self.maze.start
        ty, tx = self.maze.target
        stack = [(sy, sx)]
        visited = [[False for _ in range(self.maze.cols)] for _ in range(self.maze.rows)]
        prev = [[None for _ in range(self.maze.cols)] for _ in range(self.maze.rows)]
        visited[sy][sx] = True
        while stack:
            y, x = stack.pop()
            yield (y, x, [row[:] for row in prev])
            if (y, x) == (ty, tx):
                break
            for ny, nx in self.maze.neighbors(y, x):
                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    prev[ny][nx] = (y, x)
                    stack.append((ny, nx))
        # Final path
        path = []
        cy, cx = ty, tx
        while (cy, cx) != (sy, sx):
            path.append((cy, cx))
            cy, cx = prev[cy][cx]
            if cy is None or cx is None:
                return []
        path.append((sy, sx))
        path.reverse()
        yield ('done', path, prev)

    def greedy_best_first_steps(self):
        sy, sx = self.maze.start
        ty, tx = self.maze.target
        def heuristic(y, x):
            return abs(y - ty) + abs(x - tx)
        heap = [(heuristic(sy, sx), sy, sx)]
        visited = [[False for _ in range(self.maze.cols)] for _ in range(self.maze.rows)]
        prev = [[None for _ in range(self.maze.cols)] for _ in range(self.maze.rows)]
        visited[sy][sx] = True
        while heap:
            h, y, x = heapq.heappop(heap)
            yield (y, x, [row[:] for row in prev])
            if (y, x) == (ty, tx):
                break
            for ny, nx in self.maze.neighbors(y, x):
                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    prev[ny][nx] = (y, x)
                    heapq.heappush(heap, (heuristic(ny, nx), ny, nx))
        # Final path
        path = []
        cy, cx = ty, tx
        while (cy, cx) != (sy, sx):
            path.append((cy, cx))
            cy, cx = prev[cy][cx]
            if cy is None or cx is None:
                return []
        path.append((sy, sx))
        path.reverse()
        yield ('done', path, prev)
