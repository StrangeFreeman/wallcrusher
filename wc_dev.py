import random
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#-------------------------------------------------------------------------
# velocity analysis
#-------------------------------------------------------------------------
class VelocityAnalyzer(object):
    def __init__(self, filename: str):
        self.filename = filename
        self.conter = 0
        self.data = {}
        self.headers = []
        
    def fileSetup(self):
        with open(self.filename, 'w', newline='') as file:
            file_witer = csv.writer(file)
            file_witer.writerow(['counter', 'brick_name', 'x', 'y'])
    
    def recorder(self, brick_name: str, x: float, y: float):
        self.conter += 1
        with open(self.filename, 'a', newline='') as file:
            file_writer = csv.writer(file)
            file_writer.writerow([self.conter, brick_name, x, y])
    
    def reader(self):
        try:
            with open(self.filename, 'r', newline='',  encoding='utf-8') as file:
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
                    
                print(f'read file sucessful: {self.filename}')
                
        except FileNotFoundError:
            print(f'file not found: {self.filename}')
        except Exception as e:
            print(f'error: {e}')
    
    def scatterPlotter(self, title: str):
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
        plt.show()   
        
class DynamicScatterPlotter(object):
    def __init__(self, data, title):
        self.data  = data
        self.title = title
        self.index = 0
        self.x = self.data['x']
        self.y = self.data['y']
        self.px = []
        self.py = []
        self.fig, self.ax = plt.subplots()
        self.anime = FuncAnimation(self.fig, self.update, interval = 100)
        
    def update(self, frame):
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
        
    def show(self):
        plt.show()
    
#-------------------------------------------------------------------------
# simple ai test system
#-------------------------------------------------------------------------
class Robot(object):
    def __init__(self, speed, deadzone, delta):
        self.robot_speed = speed
        self.deadzone = deadzone
        self.delta = delta
        
    def control0(self, paddle_x_center, ball_x_center):
        if paddle_x_center < ball_x_center - self.deadzone:
            return self.robot_speed
        elif paddle_x_center > ball_x_center + self.deadzone:
            return (- self.robot_speed)
        else:
            return 0
        
    def control1(self):
        return random.uniform(-self.delta, self.delta)
        
    def detect(self, canvas_width, paddle_x, ball_x_center, paddle_half_width):
        paddle_x_center = paddle_x + paddle_half_width
        if paddle_x_center + self.robot_speed <= 0 + paddle_half_width:
            return paddle_half_width / 2
        elif paddle_x_center - self.robot_speed >= canvas_width - paddle_half_width:
            return - paddle_half_width / 2
        else:
            return self.control0(paddle_x_center, ball_x_center)