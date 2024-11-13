import os
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from graphviz import Digraph

#-------------------------------------------------------------------------
# velocity analysis
#-------------------------------------------------------------------------
class VelocityAnalyzer(object):
    def __init__(self, filename: str) -> None:
        self.file_name = filename
        self.conter = 0
        self.data = {}
        self.headers = []
        self.csv_path = os.path.join('analysis',self.file_name)
        self.fileSetup()
        
    def fileSetup(self) -> None:
        with open(self.csv_path, 'w', newline='') as file:
            file_witer = csv.writer(file)
            file_witer.writerow(['counter', 'brick_name', 'x', 'y'])
    
    def recorder(self, brick_name: str, velocity: list) -> None:
        x, y = velocity
        self.conter += 1
        with open(self.csv_path, 'a', newline='') as file:
            file_writer = csv.writer(file)
            file_writer.writerow([self.conter, brick_name, x, y])
    
    def reader(self) -> None:
        try:
            with open(self.csv_path, 'r', newline='',  encoding='utf-8') as file:
                reader = csv.reader(file)
                self.headers = next(reader)
                
                for header in self.headers:
                    self.data[header] = []
                
                for row in reader:
                    for header, value in zip(self.headers, row):
                        if header in ['counter', 'x', 'y']:
                            try:
                                value = float(value)
                            except ValueError:
                                print(f'warning file value error: can not turn "{value}" in "{header}" to number, set to 0')
                                value = 0.0
                        self.data[header].append(value)
                    
                print(f'read file sucessful: {self.file_name}')
                
        except FileNotFoundError:
            print(f'file not found: {self.file_name}')
        except Exception as e:
            print(f'error: {e}')
    
    def scatterPlotter(self, title: str) -> None:
        self.plot_path = os.path.join('analysis', 'raw_data', 'velocity_plot', title)
        if not self.data or 'x' not in self.data or 'y' not in self.data:
            print(f'file error')
            return
        
        x_value = self.data['x']
        y_value = self.data['y']
        
        plt.scatter(x_value, y_value, alpha=0.27, edgecolors='w')
        plt.title(title)
        plt.xlabel('dx')
        plt.ylabel('dy')
        plt.grid(True)
        plt.savefig(self.plot_path)
        plt.show()   
        
class DynamicScatterPlotter(object):
    def __init__(self, data: dict, title: str) -> None:
        self.data  = data
        self.title = title
        self.index = 0
        self.x = self.data['x']
        self.y = self.data['y']
        self.px = []
        self.py = []
        self.fig, self.ax = plt.subplots()
        self.anime = FuncAnimation(self.fig, self.update, interval = 100)
        
    def update(self, frame) -> None:
        self.index += 1
        try:
            self.px.append(self.x[self.index])
            self.py.append(self.y[self.index])
        except:
            pass
        
        self.ax.clear()
        
        self.ax.set_title(self.title)
        self.ax.set_xlabel('dx')
        self.ax.set_ylabel('dy')
        self.ax.grid(True)   
        self.ax.scatter(self.px, self.py,  c = 'b', alpha = 0.27)
        self.fig.canvas.draw()
        
    def show(self) -> None:
        plt.show()
        
# -------------------------------------------------------------------------
# bvh tree visualize
# -------------------------------------------------------------------------
def visualize_bvh(node, graph=None, node_id=0):
    if graph is None:
        graph = Digraph()
    
    if node.left is None and node.right is None:
        # Leaf node
        graph.node(str(node_id), f"Leaf\nMin: {node.bounding_box.min_point}\nMax: {node.bounding_box.max_point}")
    else:
        # Internal node
        graph.node(str(node_id), f"Node\nMin: {node.bounding_box.min_point}\nMax: {node.bounding_box.max_point}")
        
        # Recursively add children
        left_id = node_id * 2 + 1
        right_id = node_id * 2 + 2
        if node.left:
            graph.edge(str(node_id), str(left_id))
            visualize_bvh(node.left, graph, left_id)
        if node.right:
            graph.edge(str(node_id), str(right_id))
            visualize_bvh(node.right, graph, right_id)
    return graph
    
if __name__ == "__main__":
    # initialize velocity analyzer
    bricks_in = VelocityAnalyzer('bricks_in_velocity.csv')
    bricks_out= VelocityAnalyzer('bricks_out_velocity.csv')
    paddle_analyzer = VelocityAnalyzer('paddle_out_velocity.csv')

    bricks_in.reader()
    bricks_out.reader()
    paddle_analyzer.reader()

    bricks_in.scatterPlotter('ball-brick in velocity')
    bricks_out.scatterPlotter('ball-brick out velocity')
    paddle_analyzer.scatterPlotter('ball-paddle out velocity')

    # dynamic_bricks_in = DynamicScatterPlotter(bricks_in.data, 'bricks_in_velocity.csv')
    # dynamic_bricks_in.show()