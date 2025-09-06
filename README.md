# Maze Generator & Visualizer

Hey! I semi-vibecoded this application to generate random mazes and visualize shortest path algorithms (A*, Dijkstra, Breadth-first Search) using Pygame.


## Features

- Generates random mazes of customizable size
- Visualizes A*, Dijkstra, and BFS algorithms step-by-step

## Algorithm Differences

- **A\***: Uses both the cost so far and a heuristic (estimated distance to the target) to find the shortest path efficiently. It is usually the fastest and most direct for grid mazes.
- **Dijkstra**: Explores all possible paths from the start, always expanding the lowest-cost node first. It guarantees the shortest path but does not use any heuristic, so it may explore more nodes than A*.
- **Breadth-First Search (BFS)**: Explores all nodes at the current distance before moving further. It finds the shortest path in an unweighted maze but is less efficient than A* and Dijkstra for large grids.

## Usage

Run the main program:

```bash
python main.py
```

- Click "Regenerate" to create a new maze.
- Click an algorithm button to visualize its search and shortest path.

