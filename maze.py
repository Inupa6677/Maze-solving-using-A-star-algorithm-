import random
from queue import PriorityQueue
import tkinter as tk

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = []

    def generate_the_maze(self):
        for i in range(self.rows):
            row = ['.'] * self.cols
            self.maze.append(row)

        # Randomly select a starting node within the first 2 columns
        start_node = (random.randint(0, 1), random.randint(0, self.rows - 1))
        self.maze[start_node[1]][start_node[0]] = 'S'

        # Randomly select an ending node within the last 2 columns
        end_node = (random.randint(self.cols - 2, self.cols - 1), random.randint(0, self.rows - 1))
        self.maze[end_node[1]][end_node[0]] = 'E'

        # Randomly select 4 barrier nodes
        barrier_nodes = set()
        while len(barrier_nodes) < 4:
            barrier_node = (random.randint(0, self.cols - 1), random.randint(0, self.rows - 1))

            if (
                    barrier_node != start_node
                    and barrier_node != end_node
                    and self.maze[barrier_node[1]][barrier_node[0]] != '#'
            ):
                barrier_nodes.add(barrier_node)
                self.maze[barrier_node[1]][barrier_node[0]] = '#'

        return start_node, end_node, barrier_nodes

    # printing the maze
    def print_maze(self):
        for row in self.maze:
            print(' '.join(row))

    # checking neighbors for travelling
    def get_neighbors(self, node):
        i, j = node
        neighbors = [
            (i - 1, j),  # up
            (i + 1, j),  # down
            (i, j - 1),  # left
            (i, j + 1),  # right
            (i - 1, j - 1),  # top-left (diagonal)
            (i - 1, j + 1),  # top-right (diagonal)
            (i + 1, j - 1),  # bottom-left (diagonal)
            (i + 1, j + 1),  # bottom-right (diagonal)
        ]
        return [
            (x, y) for x, y in neighbors if 0 <= x < self.rows and 0 <= y < self.cols and self.maze[y][x] != '#'
        ]

# a star implementation
class AStarSearch:
    def __init__(self, maze):
        self.maze = maze
        self.start_node, self.end_node, _ = maze.generate_the_maze()

    # calculating the manhattan distance
    def calculate_manhattan_distance(self, node1, node2):
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

    # calculating heuristic value
    def calculate_heuristic_value(self, node, goal):
        return self.calculate_manhattan_distance(node, goal)

    # calculating total cost
    def calculate_g_cost(self, current, start):
        return abs(current[0] - start[0]) + abs(current[1] - start[1])

    # A star search algorithm calculating the costs
    def a_star_search(self):
        open_set = PriorityQueue()
        open_set.put((0, self.start_node))
        came_from = {}
        cost_so_far = {self.start_node: 0}

        while not open_set.empty():
            current_cost, current_node = open_set.get()

            if current_node == self.end_node:
                break

            for neighbor in self.maze.get_neighbors(current_node):
                new_cost = cost_so_far[current_node] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heuristic = self.calculate_heuristic_value(neighbor, self.end_node)
                    g_cost = self.calculate_g_cost(neighbor, self.start_node)
                    priority = new_cost + heuristic
                    open_set.put((priority, neighbor))
                    came_from[neighbor] = current_node

        # Reconstruct the path and calculate total cost
        path = [self.end_node]
        total_cost = 0
        while path[-1] != self.start_node:
            total_cost += 1
            path.append(came_from[path[-1]])
        path.reverse()
        # returning the total cost
        return path, total_cost

# gui class
class GUI:
    # setting the gui
    def __init__(self, master, maze_instance):
        self.master = master
        self.maze_instance = maze_instance
        self.canvas_size = 400
        self.cell_size = self.canvas_size // maze_instance.cols
        self.canvas = tk.Canvas(master, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()
        self.draw_maze()

    # draw the maze in gui (starting nodes ending nodes and barriers)
    def draw_maze(self):
        for i in range(self.maze_instance.rows):
            for j in range(self.maze_instance.cols):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                if self.maze_instance.maze[i][j] == '#':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='black')
                elif self.maze_instance.maze[i][j] == 'S':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='green')
                elif self.maze_instance.maze[i][j] == 'E':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='red')
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white')

    # drawing the final path of maze
    def draw_final_path(self, path):
        for i in range(1, len(path) - 1):
            node = path[i]
            x, y = node
            x1, y1 = x * self.cell_size, y * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='yellow')
            self.master.update()
            self.master.after(500)  # Delay of 500 milliseconds
            self.canvas.update()

        print("Path drawing completed!")


# usage
maze_instance = Maze(rows=6, cols=6)
a_star_search_instance = AStarSearch(maze_instance)
final_path, total_cost = a_star_search_instance.a_star_search()

# Print the generated maze
maze_instance.print_maze()

# Print the final path and total cost
print("Final Path:")
print(final_path)
print("Total Cost:", total_cost)

root = tk.Tk()
gui_instance = GUI(root, maze_instance)
gui_instance.draw_final_path(final_path)
root.mainloop()




