import pygame
import time

from maze_generator import Maze
from maze_solver import MazeSolver

class MazeVisualizer:
    COLORS = {
        "A*": (0, 0, 255),
        "Dijkstra": (0, 128, 0),
        "BFS": (255, 0, 0),
        "A*_path": (0, 0, 128),         
        "Dijkstra_path": (0, 64, 0),    
        "BFS_path": (128, 0, 0),        
    }
    MARGIN = 20
    BUTTON_HEIGHT = 50
    FIXED_WIDTH = 800
    FIXED_HEIGHT = 800
    GAP = 20

    def __init__(self, maze: Maze):
        self.maze = maze
        self.width = self.FIXED_WIDTH
        self.height = self.FIXED_HEIGHT + self.BUTTON_HEIGHT + self.GAP
        self.margin = self.MARGIN
        self.button_height = self.BUTTON_HEIGHT
        self.cell_size_x = (self.FIXED_WIDTH - 2 * self.margin) // maze.cols
        self.cell_size_y = (self.FIXED_HEIGHT - 2 * self.margin) // maze.rows
        self.cell_size = min(self.cell_size_x, self.cell_size_y)

    def draw_maze(self, screen, path=None, visited=None, lines=None, algo_name=None, elapsed=None):
        maze = self.maze
        margin = self.margin
        cell_size = self.cell_size
        width = self.width
        height = self.height
        button_height = self.button_height

        screen.fill((255, 255, 255))
        # Draw the target cell
        target_y, target_x = maze.target
        rect_x = margin + target_x * cell_size + 2
        rect_y = margin + target_y * cell_size + 2
        pygame.draw.rect(screen, (255, 0, 0), (rect_x, rect_y, cell_size - 4, cell_size - 4))
        # Draw continuous line for search progress
        line_color = self.COLORS.get(algo_name, (0, 180, 255))
        if lines:
            for (y1, x1), (y2, x2) in lines:
                x1c = margin + x1 * cell_size + cell_size // 2
                y1c = margin + y1 * cell_size + cell_size // 2
                x2c = margin + x2 * cell_size + cell_size // 2
                y2c = margin + y2 * cell_size + cell_size // 2
                pygame.draw.line(screen, line_color, (x1c, y1c), (x2c, y2c), 4)
        # Draw path in distinct color for each algorithm
        if path:
            path_color = self.COLORS.get(f"{algo_name}_path", (0, 0, 128))
            for i in range(1, len(path)):
                py1, px1 = path[i-1]
                py2, px2 = path[i]
                x1c = margin + px1 * cell_size + cell_size // 2
                y1c = margin + py1 * cell_size + cell_size // 2
                x2c = margin + px2 * cell_size + cell_size // 2
                y2c = margin + py2 * cell_size + cell_size // 2
                pygame.draw.line(screen, path_color, (x1c, y1c), (x2c, y2c), 6)
        # Draw horizontal walls
        for y in range(maze.rows + 1):
            for x in range(maze.cols):
                if maze.H[y][x]:
                    x1 = margin + x * cell_size
                    y1 = margin + y * cell_size
                    x2 = margin + (x + 1) * cell_size
                    pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y1), 2)
        # Draw vertical walls
        for y in range(maze.rows):
            for x in range(maze.cols + 1):
                if maze.V[y][x]:
                    x1 = margin + x * cell_size
                    y1 = margin + y * cell_size
                    y2 = margin + (y + 1) * cell_size
                    pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x1, y2), 2)
        # Draw regenerate button
        button_rect = pygame.Rect(margin, height - button_height + 10, (width - 4 * margin) // 4, button_height - 20)
        pygame.draw.rect(screen, (0, 120, 255), button_rect)
        font = pygame.font.SysFont(None, 36)
        text = font.render("Regenerate", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)
        # Draw algorithm selection buttons
        algo_buttons = []
        for i, algo in enumerate(["A*", "Dijkstra", "BFS"]):
            color = self.COLORS[algo]
            rect = pygame.Rect(margin + ((width - 4 * margin) // 4 + margin) * (i+1), height - button_height + 10, (width - 4 * margin) // 4, button_height - 20)
            pygame.draw.rect(screen, color, rect)
            algo_text = font.render(algo, True, (255, 255, 255))
            algo_text_rect = algo_text.get_rect(center=rect.center)
            screen.blit(algo_text, algo_text_rect)
            algo_buttons.append((rect, algo))
        # Draw algorithm name and time below the maze
        if algo_name and elapsed is not None:
            info_font = pygame.font.SysFont(None, 40)
            info_text = f"{algo_name}: {elapsed/1000:.2f} s"
            info_render = info_font.render(info_text, True, (0, 0, 0))
            info_rect = info_render.get_rect(center=(width // 2, height - button_height - self.GAP // 2))
            screen.blit(info_render, info_rect)
        pygame.display.flip()
        return button_rect, algo_buttons

    def run(self):
        maze = self.maze
        solver = MazeSolver(maze)
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze")
        maze.setup()
        button_rect, algo_buttons = self.draw_maze(screen)

        running = True
        show_search = False
        search_algo = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        maze.setup()
                        button_rect, algo_buttons = self.draw_maze(screen)
                        show_search = False
                        search_algo = None
                    else:
                        for rect, algo in algo_buttons:
                            if rect.collidepoint(event.pos):
                                show_search = True
                                search_algo = algo
            if show_search and search_algo:
                visited = set()
                lines = []
                prev = None
                start_time = time.time()
                if search_algo == "A*":
                    steps = solver.astar_steps()
                elif search_algo == "Dijkstra":
                    steps = solver.dijkstra_steps()
                elif search_algo == "BFS":
                    steps = solver.bfs_steps()
                else:
                    steps = []
                running_search = True
                for step in steps:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            running_search = False
                            break
                    if not running_search:
                        break
                    if step[0] == 'done':
                        path = step[1]
                        elapsed = (time.time() - start_time) * 1000
                        self.draw_maze(screen, path=path, visited=visited, lines=lines, algo_name=search_algo, elapsed=elapsed)
                        break
                    y, x, prev_arr = step
                    visited.add((y, x))
                    if prev_arr[y][x] is not None:
                        lines.append(((y, x), prev_arr[y][x]))
                    self.draw_maze(screen, path=None, visited=visited, lines=lines, algo_name=search_algo, elapsed=None)
                    pygame.time.wait(10)
                show_search = False
                search_algo = None
        pygame.quit()