from maze_generator import Maze
from maze_visualizer import MazeVisualizer

def main():
    m = Maze(50, 50)
    MazeVisualizer(m).run()

if __name__ == "__main__":
    main()
