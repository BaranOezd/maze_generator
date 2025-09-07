# Maze Generator & Visualizer

This application generates random mazes and visualizes shortest path algorithms using Pygame.

## Features

- Generates random mazes of customizable size
- Visualizes multiple algorithms step-by-step:
  - **A\*** (A Star)
  - **Dijkstra**
  - **Breadth-First Search (BFS)**
  - **Depth-First Search (DFS)**
  - **Greedy Best First**
- Interactive UI: regenerate maze, select algorithm
- Distinct colors for each algorithm and its shortest path
- Responsive visualization with animated search progress

## Algorithm Differences

- **A\***: Uses both the cost so far and a heuristic (estimated distance to the target) to find the shortest path efficiently. Usually the fastest and most direct for grid mazes.
- **Dijkstra**: Explores all possible paths from the start, always expanding the lowest-cost node first. Guarantees the shortest path but does not use any heuristic, so it may explore more nodes than A*.
- **Breadth-First Search (BFS)**: Explores all nodes at the current distance before moving further. Finds the shortest path in an unweighted maze but is less efficient than A* and Dijkstra for large grids.
- **Depth-First Search (DFS)**: Explores as far as possible along each branch before backtracking. Does not guarantee the shortest path.
- **Greedy Best First**: Uses only the heuristic (estimated distance to the target) and ignores the cost so far. Fast but does not guarantee the shortest path.

## Usage

Run the main program:

```bash
python main.py
```

- Click "Regenerate" to create a new maze.
- Click an algorithm button to visualize its search and shortest path.
