# encoding: utf-8
import numpy as np
from src.physics import *

#-------------------------------------------------------------------------
# draw rectangle
#-------------------------------------------------------------------------
class Box(object):
    def __init__(self, pygame, canvas, name, rect, color, hp) -> None:
        self.pygame = pygame
        self.canvas = canvas
        self.name = name
        self.rect = rect
        self.color = color
        self.hp = hp
        self.hp_limit = hp
        self.visible = True   
#-------------------------------------------------------------------------
# draw circle
#-------------------------------------------------------------------------
class Circle(object):
    def __init__(self, pygame, canvas, name, pos, radius, color) -> None:
        self.pygame = pygame
        self.canvas = canvas
        self.name = name
        self.pos = pos
        self.radius = radius
        self.color = color
        self.visible = True
            
class Paddle(Box):
    #-------------------------------------------------------------------------
    # constructive
    #   pygame      : pygame
    #   canvas      : canvas.
    #   name        : object name
    #   rect        : [(upper left corner) x, y, width, height]
    #   color       : color
    #   hp          : health point
    #   hp_limit    : health point max limit
    #   coordinates : [x + velocity[0], y + velocity[1]]
    #-------------------------------------------------------------------------
    def __init__(self, pygame, canvas, name, rect, color, hp, coordinates) -> None:
        super().__init__(pygame, canvas, name, rect, color, hp)
        self.coordinates = coordinates
    #-------------------------------------------------------------------------
    # update
    #-------------------------------------------------------------------------
    def update(self) -> None:
        self.rect[0] = self.coordinates[0]
    #-------------------------------------------------------------------------
    # display
    #-------------------------------------------------------------------------
    def display(self) -> None:
        self.pygame.draw.rect(self.canvas, self.color, self.rect) 

class Brick(Box):
    #-------------------------------------------------------------------------
    # constructive
    #   pygame      : pygame
    #   canvas      : canvas.
    #   name        : object name
    #   rect        : [(upper left corner) x, y, width, height]
    #   color       : color
    #   hp          : health point
    #   hp_limit    : health point max limit
    #   bounding_box: min_point = [x,y], max_point = [x + width, y + height]
    #-------------------------------------------------------------------------
    def __init__(self, pygame, canvas, name, rect, color, hp) -> None:
        super().__init__(pygame, canvas, name, rect, color, hp)
        self.bounding_box = BoundingBox([self.rect[0], self.rect[1]], 
                                        [self.rect[0] + self.rect[2], self.rect[1] + self.rect[3]])
    #-------------------------------------------------------------------------
    # display
    #-------------------------------------------------------------------------
    def display(self) -> None:
        self.pygame.draw.rect(self.canvas, self.color, self.rect)

class Bricks(object):
    #-------------------------------------------------------------------------
    # constructive
    #   width       : brick width
    #   height      : brick height
    #   num_limmit  : bricks num limmit
    #   row_limmit  : bricks row    limmit
    #   col_limmit  : bricks column limmit
    #   row_space   : bricks row    space
    #   col_space   : bricks column space
    #   num         : bricks number
    #   list        : bricks list
    #-------------------------------------------------------------------------
    def __init__(self, pygame, width: int, height: int, num_limmit, row_limmit, col_limmit, row_space, col_space) -> None:
        self.pygame = pygame
        self.width = width
        self.height = height
        self.num_limmit = num_limmit
        self.row_limmit = row_limmit
        self.col_limmit = col_limmit
        self.row_space = row_space
        self.col_space = col_space
        
        self.color_gray_block = (20, 31, 23)
        
        self.num = 0
        self.list = []
        
    #-------------------------------------------------------------------------
    # bricks list initulize
    #-------------------------------------------------------------------------   
    def listInit(self, canvas) -> None:
        start = [70, 60]
        temp = [0, 0]
        for i in range(0, self.num_limmit):
            if i % self.row_limmit == 0:
                temp[0] = 0
                temp[1] += self.height + self.col_space
            self.list.append(
                Brick(
                    pygame = self.pygame,
                    canvas = canvas,
                    name = "brick_" + str(i),
                    rect = [
                        start[0] + temp[0],
                        start[1] + temp[1],
                        self.width,
                        self.height,
                    ],
                    color = self.color_gray_block,
                    hp = 1
                )
            )
            temp[0] += self.width + self.row_space
            self.num += 1
        self.bvh_tree = build_bvh(bricks = self.list)
    #-------------------------------------------------------------------------
    # reset
    #-------------------------------------------------------------------------
    def reset(self) -> None:
        for brick in self.list:
            brick.color = self.color_gray_block
            brick.hp = brick.hp_limit
            brick.visible = True
        self.num = self.num_limmit
    #-------------------------------------------------------------------------
    # display
    #-------------------------------------------------------------------------
    def display(self) -> None:
        for brick in self.list:
            if brick.visible:
                brick.display()

class Ball(Circle):
    #-------------------------------------------------------------------------
    # constructive
    #   pygame      : pygame
    #   canvas      : canvas.
    #   name        : object name
    #   pos         : [x, y]
    #   color       : color
    #   coordinates : [x + velocity[0], y + velocity[1]]
    #   bounding_box: min_point = [x - radius, y - radius], max_point = [x + radius, y + radius]
    #-------------------------------------------------------------------------
    def __init__(self, pygame, canvas, name, pos, radius, color, coordinates) -> None:
        super().__init__(pygame, canvas, name, pos, radius, color)
        self.coordinates = coordinates
        self.bounding_box = BoundingBox([self.pos[0] - self.radius, self.pos[1] - self.radius],
                                        [self.pos[0] + self.radius, self.pos[1] + self.radius])
    #-------------------------------------------------------------------------
    # update
    #-------------------------------------------------------------------------
    def update(self, coordinates: list) -> None:
        self.pos = coordinates
        self.bounding_box = BoundingBox([self.pos[0] - self.radius, self.pos[1] - self.radius],
                                        [self.pos[0] + self.radius, self.pos[1] + self.radius])
    #-------------------------------------------------------------------------
    # display
    #-------------------------------------------------------------------------
    def display(self) -> None:
        self.pygame.draw.circle(self.canvas, self.color, self.pos , self.radius)
#-------------------------------------------------------------------------
# speed and velocity
#-------------------------------------------------------------------------    
class Velocity(object):
    def __init__(self, speed: int) -> None:
        self.speed = speed
        self.reset()
        
    def update(self, velocity: np) -> None:
        self.velocity = velocity
        
    def reset(self) -> None:
        self.velocity = np.array([self.speed, -self.speed])
    
    def fix(self, velocity: np) -> None:
        fix = [
            np.array([self.speed ,self.speed]),
            np.array([-self.speed,self.speed]),
            np.array([-self.speed,-self.speed]),
            np.array([self.speed ,-self.speed]),
        ]
        norm = np.linalg.norm(velocity)
        velocity_norm = velocity / norm
        max = -1
        for i in fix:
            dev = np.dot(velocity_norm, i)
            if dev > max:
                max = dev
                ans = i
        self.velocity = ans

#-------------------------------------------------------------------------
# score related
#-------------------------------------------------------------------------
class Stylish(object):
    #-------------------------------------------------------------------------
    # constructive
    #   cp              : crush point
    #   sp              : canvas.
    #   score           : object name
    #   stylish_output  : [(upper left corner) x, y, width, height]
    #-------------------------------------------------------------------------
    def __init__(self) -> None:
        self.cp = 0
        self.sp = 0
        self.score = 0
        self.stylish_output = ''
        
    def stylish(self) -> str:
        self.stylish_rank = [
            (lambda x:        x < 10 , 5      , ''),
            (lambda x:  10 <= x < 27 , 5 * 2, 'Dismal'),
            (lambda x:  27 <= x < 45 , 5 * 3, 'Crazu'),
            (lambda x:  45 <= x < 66 , 5 * 4, 'Badass'),
            (lambda x:  66 <= x < 81 , 5 * 5, 'Apocalyptic'),
            (lambda x:  81 <= x < 100, 5 * 6, 'Savage'),
            (lambda x: 100 <= x < 127, 5 * 7, 'SickSkills'),
            (lambda x: 127 <= x      , 5 * 8, 'SmokinSexyStyle'),
        ]
        for condition, score, output in self.stylish_rank:
            if condition(self.sp):
                self.score += score 
                self.stylish_output = output