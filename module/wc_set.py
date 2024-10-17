# encoding: utf-8
import numpy as np
from typing import Tuple

#-------------------------------------------------------------------------
# draw rectangle
#-------------------------------------------------------------------------
class Box(object):
    #-------------------------------------------------------------------------
    # Constructive
    #   pygame    : pygame
    #   canvas    : canvas.
    #   name      : object name
    #   rect      : position, size, [upper left corner x, y, width, height]
    #   color     : color
    #-------------------------------------------------------------------------
    def __init__(self, pygame, canvas, name, rect, color):
        self.pygame = pygame
        self.canvas = canvas
        self.name = name
        self.rect = rect
        self.color = color

        self.visible = True
        
    #-------------------------------------------------------------------------
    # update
    #-------------------------------------------------------------------------
    def update(self):
        if(self.visible):
            self.pygame.draw.rect( self.canvas, self.color, self.rect)

#-------------------------------------------------------------------------
# draw circle
#-------------------------------------------------------------------------
class Circle(object):
    #-------------------------------------------------------------------------
    # Constructive
    #   pygame  : pygame
    #   canvas  : canvas
    #   name    : object name
    #   pos     : center of the circle [x, y]
    #   radius  : size
    #   color   : color    
    #-------------------------------------------------------------------------
    def __init__( self, pygame, canvas, name, pos, radius, color):
        self.pygame = pygame
        self.canvas = canvas
        self.name = name
        self.pos = pos
        self.radius = radius
        self.color = color
        
        self.visible = True

    #-------------------------------------------------------------------------
    # update
    #-------------------------------------------------------------------------
    def update(self):
        if(self.visible):
            self.pygame.draw.circle( self.canvas, self.color, self.pos , self.radius)
            
#-------------------------------------------------------------------------
# set basic game parameters 1
#-------------------------------------------------------------------------
    
class Game(object):
    def __init__(self, canvas_width: int, canvas_height: int, paddle_width: int, paddle_height: int, ball_radius: int, brick_width: int, brick_height: int, speed: int) -> None:
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.paddle_width = paddle_width
        self.paddle_height = paddle_height
        self.ball_radius = ball_radius
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.speed = speed
 
#-------------------------------------------------------------------------
# set basic game parameters 2
#-------------------------------------------------------------------------       
class PlayGround0(Game):
    def __init__(self, canvas_width: int, canvas_height: int, paddle_width: int, paddle_height: int, ball_radius: int, brick_width: int, brick_height: int, speed: int, brick_x: int, brick_y: int, brick_num_limmit: int, brick_row_limmit: int, brick_col_limmit: int, brick_row_space: int, brick_col_space: int) -> None:
        super().__init__(canvas_width, canvas_height, paddle_width, paddle_height, ball_radius, brick_width, brick_height, speed)
        self.brick_x = brick_x
        self.brick_y = brick_y
        self.brick_num_limmit = brick_num_limmit
        self.brick_row_limmit = brick_row_limmit
        self.brick_col_limmit = brick_col_limmit
        self.brick_row_space = brick_row_space
        self.brick_col_space = brick_col_space
        
    def banner(self) -> None:
        banner = '''
██████╗ ██╗      █████╗ ██╗   ██╗ ██████╗ ██████╗  ██████╗ ██╗   ██╗███╗   ██╗██████╗ 
██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝██╔════╝ ██╔══██╗██╔═══██╗██║   ██║████╗  ██║██╔══██╗
██████╔╝██║     ███████║ ╚████╔╝ ██║  ███╗██████╔╝██║   ██║██║   ██║██╔██╗ ██║██║  ██║
██╔═══╝ ██║     ██╔══██║  ╚██╔╝  ██║   ██║██╔══██╗██║   ██║██║   ██║██║╚██╗██║██║  ██║
██║     ███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║██████╔╝
╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝ 
        '''
        print(banner)
    
    def getYesNo(self, prompt: str, default: str) -> Tuple[bool, bool]:
        if default.lower() == 'y':
            prompt = f"{prompt}(Y/n) "
        else:
            prompt = f"{prompt}(y/N) "

        user_input = input(prompt).strip().lower()
        if user_input == '':
            user_input = default.lower()
        
        return user_input in ['yes', 'y'], user_input in ['no', 'n']
    
    def inputParameters(self, prompt: str, default: str) -> bool:
        user_input = input(f"{prompt}({default}) ")
        return int(user_input) if user_input != '' else default
    
    def setParameters(self, flag) -> None:
        self.parameters = {
            'canvas_width': self.canvas_width,
            'canvas_height': self.canvas_height,
            'paddle_width': self.paddle_width,
            'paddle_height': self.paddle_height,
            'ball_radius': self.ball_radius,
            'brick_x': self.brick_x,
            'brick_y': self.brick_y,
            'brick_num_limmit': self.brick_num_limmit,
            'brick_row_limmit': self.brick_row_limmit,
            'brick_col_limmit': self.brick_col_limmit,
            'brick_row_space': self.brick_row_space,
            'brick_col_space': self.brick_col_space,
            'brick_width': self.brick_width,
            'brick_height': self.brick_height,
            'speed': self.speed
        }
        
        if flag == 'set':
            for key in self.parameters:
                self.parameters[key] = self.inputParameters(key, self.parameters[key])
                
        self.updateParameter()
    
    def updateParameter(self) -> None:
        self.canvas_width = self.parameters['canvas_width']
        self.canvas_height = self.parameters['canvas_height']
        self.paddle_width = self.parameters['paddle_width']
        self.paddle_height = self.parameters['paddle_height']
        self.ball_radius = self.parameters['ball_radius']
        self.brick_width = self.parameters['brick_width']
        self.brick_height = self.parameters['brick_height']
        self.speed = self.parameters['speed']
        self.brick_x = self.parameters['brick_x']
        self.brick_y = self.parameters['brick_y']
        self.brick_num_limmit = self.parameters['brick_num_limmit']
        self.brick_row_limmit = self.parameters['brick_row_limmit']
        self.brick_col_limmit = self.parameters['brick_col_limmit']
        self.brick_row_space = self.parameters['brick_row_space']
        self.brick_col_space = self.parameters['brick_col_space']
    
    def preSetup(self) -> Tuple[bool, bool]:
        self.banner()
        auto = False
        is_yes, is_no = self.getYesNo('Custom setting?', 'n')
        if is_yes:
            self.setParameters('set')
            is_continue_yes, is_continue_no = self.getYesNo('Continue?', 'y')
            if is_continue_yes:
                auto_on, auto_off = self.getYesNo('Auto Mode?', 'y')
                if auto_on:
                    return True, True 
                elif auto_off:
                    return True, False
            elif is_continue_no:
                return self.preSetup()
        elif is_no:
            self.setParameters('default')
            return True, False

#-------------------------------------------------------------------------
# score related
#-------------------------------------------------------------------------
class Stylish(object):
    def __init__(self, crash_point, stylish_point):
        self.cp = crash_point
        self.sp = stylish_point
        
    def stylish(self):
        self.stylish_rank = {
            'Dismal': 10,
            'Crazy': 27,
            'Badass': 45,
            'Apocalyptic': 66,
            'Savage': 81,
            'SickSkills': 100,
            'SmokinSexyStyle': 127
        }
        if self.sp < 3:        
            return ''
        
        for key in self.stylish_rank:
            if self.sp <= self.stylish_rank[key]:
                return key
            elif self.sp > self.stylish_rank['SmokinSexyStyle']:
                return key



# -------------------------------------------------------------------------
# function: collision detect
# input:
#       x       : x
#       y       : y
#       boxRect : [x, y, width, height]
#       radius  : radius
# -------------------------------------------------------------------------
def isCollision(x, y, boxRect, radius) -> bool:
    if (
        x + radius > boxRect[0]                      # 球和物體左側碰撞檢測 
        and x - radius < boxRect[0] + boxRect[2]     # 球和物體右側碰撞檢測
        and y + radius > boxRect[1]                  # 球和物體下側碰撞檢測
        and y - radius < boxRect[1] + boxRect[3]     # 球和物體上側碰撞檢測
    ):
        return True
    return False

# -------------------------------------------------------------------------
# function: collision detect
# input:
#       x       : x
#       y       : y
#       boxRect : [x, y, width, height]
#        radius  : radius
# -------------------------------------------------------------------------
def isCollision7(x: int, y: int, boxRect: list, radius: int) -> Tuple[bool, np.array]:
    ball_center = np.array([x,y])
    brick_half_extents = np.array([boxRect[2]/2, boxRect[3]/2])   
    brick_center = np.array([boxRect[0], boxRect[1]]) + brick_half_extents
    
    dist = ball_center - brick_center
    # limit operations
    clampd = np.clip(dist, -brick_half_extents, brick_half_extents)
    closest = brick_center + clampd
    dist = closest - ball_center
    
    if np.dot(dist, dist) <= radius ** 2:
        return True, dist
    return False, dist

# -------------------------------------------------------------------------
# function: orthoprojection
# input: numpy array
# -------------------------------------------------------------------------
def vectorProjection(a: np, b: np) -> np:
    divided = np.dot(b, b)
    if divided != 0:
        projection = (np.dot(a, b) / divided) * b
    else:
        projection = np.zeros_like(b)
    return projection

# -------------------------------------------------------------------------
# function: collision response
# -------------------------------------------------------------------------
def collisionResponse(ball_pos: list, radius: int, velocity: np, boxRect: list, max_steps: int) -> Tuple[bool, np.array]:
    dynamic_velocity = np.linalg.norm(velocity)
    try:
        dynamic_velocity = int(dynamic_velocity)
    except:
        dynamic_velocity = 1
    steps = max(1, min(dynamic_velocity, max_steps))
    # steps = max(1, dynamic_velocity)
    sub_velocity = velocity / steps
    sub_ball_pos = ball_pos
    flag = False
    
    for _ in range(steps):
        # ball future position
        sub_ball_pos += sub_velocity
        # collision detect
        f, force = isCollision7(sub_ball_pos[0], sub_ball_pos[1], boxRect, radius)
        if f:
            # correct velocity if collision
            rebound_force = vectorProjection(velocity, force)
            rebound_force = -rebound_force * 2
            velocity = velocity + rebound_force
            flag = True
            break

    return flag, velocity