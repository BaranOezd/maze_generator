import pygame
import time

from maze_generator import Maze
from maze_solver import MazeSolver

class MazeVisualizer:
    COLORS = {
        "A*": (0, 0, 255),
        "Dijkstra": (0, 128, 0),
        "Breadth-First Search": (255, 0, 0),
        "Depth-First Search": (128, 0, 128),
        "Greedy Best First": (255, 128, 0),
        "A*_path": (0, 0, 128),
        "Dijkstra_path": (0, 64, 0),
        "Breadth-First Search_path": (128, 0, 0),
        "Depth-First Search_path": (64, 0, 64),
        "Greedy Best First_path": (128, 64, 0),
    }
    MARGIN = 20
    BUTTON_HEIGHT = 50
    FIXED_WIDTH = 800
    FIXED_HEIGHT = 800
    GAP = 20

    ALGORITHMS = [
        "A*", "Dijkstra", "Breadth-First Search", "Depth-First Search", "Greedy Best First"
    ]

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
        # Draw continuous line for search progress with improved fading effect
        if lines:
            for ((y1, x1), (y2, x2)) in lines:
                x1c = margin + x1 * cell_size + cell_size // 2
                y1c = margin + y1 * cell_size + cell_size // 2
                x2c = margin + x2 * cell_size + cell_size // 2
                y2c = margin + y2 * cell_size + cell_size // 2
                base_color = self.COLORS.get(algo_name, (0, 180, 255))
                pygame.draw.line(screen, base_color, (x1c, y1c), (x2c, y2c), 4)
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
        # Draw algorithm selection buttons and regenerate button in the same row
        algo_buttons = []
        algo_count = len(self.ALGORITHMS)
        total_buttons = algo_count + 1  # +1 for regenerate

        # Calculate button width dynamically to fit all buttons in the row
        available_width = width - 2 * self.margin - (total_buttons - 1) * 6
        button_widths = []
        font = pygame.font.SysFont(None, 20)
        min_button_width = 70
        max_button_width = 140

        # Measure text width for each button, clamp to min/max, then scale if needed
        labels = ["Regenerate"] + self.ALGORITHMS
        for label in labels:
            text_width = font.size(label)[0] + 24  # padding
            button_widths.append(max(min_button_width, min(text_width, max_button_width)))

        total_buttons_width = sum(button_widths) + (total_buttons - 1) * 6
        scale = 1.0
        if total_buttons_width > available_width:
            scale = available_width / total_buttons_width
            button_widths = [int(w * scale) for w in button_widths]

        button_height_algo = 32
        button_y = height - button_height_algo - 8
        rect_x = self.margin

        # Draw regenerate button first
        regen_rect = pygame.Rect(rect_x, button_y, button_widths[0], button_height_algo)
        pygame.draw.rect(screen, (0, 120, 255), regen_rect, border_radius=10)
        text = font.render("Regenerate", True, (255, 255, 255))
        text_rect = text.get_rect(center=regen_rect.center)
        screen.blit(text, text_rect)
        algo_buttons.append((regen_rect, "Regenerate"))
        rect_x += button_widths[0] + 6

        # Draw algorithm buttons
        for i, algo in enumerate(self.ALGORITHMS):
            color = self.COLORS.get(algo, (100, 100, 100))
            bw = button_widths[i + 1]
            rect = pygame.Rect(rect_x, button_y, bw, button_height_algo)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            algo_text = font.render(algo, True, (255, 255, 255))
            algo_text_rect = algo_text.get_rect(center=rect.center)
            screen.blit(algo_text, algo_text_rect)
            algo_buttons.append((rect, algo))
            rect_x += bw + 6

        # Draw algorithm name and time below the maze
        if algo_name and elapsed is not None:
            info_font = pygame.font.SysFont(None, 40)
            info_text = f"{algo_name}: {elapsed/1000:.2f} s"
            info_render = info_font.render(info_text, True, (0, 0, 0))
            info_rect = info_render.get_rect(center=(width // 2, height - button_height - self.GAP // 2))
            screen.blit(info_render, info_rect)
        pygame.display.flip()
        return algo_buttons[0][0], algo_buttons[1:]  # return regenerate button and algo buttons separately

    def run(self):
        maze = self.maze
        solver = MazeSolver(maze)
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze")
        maze.setup()
        button_rect, algo_buttons = self.draw_maze(screen)
        # algo_buttons[0] is regenerate, algo_buttons[1:] are algorithms

        running = True
        show_search = False
        search_algo = None
        search_interrupt = False  # Flag to interrupt search

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    search_interrupt = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        maze.setup()
                        button_rect, algo_buttons = self.draw_maze(screen)
                        show_search = False
                        search_algo = None
                        search_interrupt = True
                    else:
                        for rect, algo in algo_buttons:
                            if rect.collidepoint(event.pos):
                                show_search = True
                                search_interrupt = True
                                search_algo = algo
            if show_search and search_algo:
                visited = set()
                lines = []
                prev = None
                start_time = time.time()
                # Algorithm selection
                if search_algo == "A*":
                    steps = solver.astar_steps()
                elif search_algo == "Dijkstra":
                    steps = solver.dijkstra_steps()
                elif search_algo == "Breadth-First Search":
                    steps = solver.bfs_steps()
                elif search_algo == "Depth-First Search":
                    steps = solver.dfs_steps()
                elif search_algo == "Greedy Best First":
                    steps = solver.greedy_best_first_steps()
                else:
                    steps = []
                running_search = True
                search_interrupt = False  # Reset interrupt for this search
                for step in steps:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            running_search = False
                            search_interrupt = True
                            break
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            # Check if any algo button is clicked
                            for rect, algo in algo_buttons:
                                if rect.collidepoint(event.pos):
                                    search_algo = algo
                                    search_interrupt = True
                                    break
                            if button_rect.collidepoint(event.pos):
                                maze.setup()
                                button_rect, algo_buttons = self.draw_maze(screen)
                                show_search = False
                                search_algo = None
                                search_interrupt = True
                    if not running_search or search_interrupt:
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
                # If interrupted by another algo, start it immediately
                if search_interrupt and running and search_algo:
                    continue
                show_search = False
                search_algo = None
        pygame.quit()