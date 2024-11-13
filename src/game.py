# encoding: utf-8
import pygame
from pygame.locals import *
from src.env import *

#-------------------------------------------------------------------------
# setting basic game parameters 
#-------------------------------------------------------------------------
class Game(object):
    def __init__(self, canvas_width: int, canvas_height: int, paddle_width: int, paddle_height: int, ball_radius: int, brick_width: int, brick_height: int, brick_num_limmit: int, brick_row_limmit: int, brick_col_limmit: int, brick_row_space: int, brick_col_space: int, speed: int) -> None:
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.title = "破磚傳奇WallCrusher"
        
        # color
        self.color_gray = (107, 130, 114)
        self.color_gray_block = (20, 31, 23)
        
        # pygame initialize
        pygame.init()
        # display title
        pygame.display.set_caption(self.title)
        # create canvas size
        self.canvas = pygame.display.set_mode((self.canvas_width, self.canvas_height))
        # clock
        self.clock = pygame.time.Clock()
        # set font
        self.font = pygame.font.SysFont("simsunnsimsun", 22)
        # game state
        # True: waiting for start
        # False: the game is running
        self.game_mode = False
        # main loop running state
        # True: is running
        # False: quit main loop
        self.running = True
        self.auto_flag = False
        # initialize stylih system
        self.stylish = Stylish()
        
        self.paddle = Paddle(
            pygame      = pygame,
            canvas      = self.canvas,
            name        = "paddle",
            rect        = [canvas_width / 2, canvas_height - 48, paddle_width, paddle_height],
            color       = self.color_gray_block,
            hp          = 3,
            coordinates = [canvas_width / 2, canvas_height - 48]
        )
        
        self.bricks = Bricks(
            pygame      = pygame,
            width       = brick_width,
            height      = brick_height,
            num_limmit  = brick_num_limmit,
            row_limmit  = brick_row_limmit,
            col_limmit  = brick_col_limmit,
            row_space   = brick_row_space,
            col_space   = brick_col_space
        )
        self.bricks.listInit(self.canvas)
        
        self.ball = Ball(
            pygame      = pygame,
            canvas      = self.canvas,
            name        = "ball",
            pos         = [self.paddle.coordinates[0], self.paddle.coordinates[1]],
            radius      = ball_radius,
            color       = self.color_gray_block,
            coordinates = [self.paddle.coordinates[0], self.paddle.coordinates[1]]
        )
        
        self.velocity = Velocity(speed)
        self.f_x = None
    
    def banner(self) -> None:
        banner = '''
██╗    ██╗ █████╗ ██╗     ██╗      ██████╗██████╗ ██╗   ██╗███████╗██╗  ██╗███████╗██████╗ 
██║    ██║██╔══██╗██║     ██║     ██╔════╝██╔══██╗██║   ██║██╔════╝██║  ██║██╔════╝██╔══██╗
██║ █╗ ██║███████║██║     ██║     ██║     ██████╔╝██║   ██║███████╗███████║█████╗  ██████╔╝
██║███╗██║██╔══██║██║     ██║     ██║     ██╔══██╗██║   ██║╚════██║██╔══██║██╔══╝  ██╔══██╗
╚███╔███╔╝██║  ██║███████╗███████╗╚██████╗██║  ██║╚██████╔╝███████║██║  ██║███████╗██║  ██║
 ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

        '''
        print(banner)

    # -------------------------------------------------------------------------
    # function: display words
    # -------------------------------------------------------------------------
    def showFont(self, test, x, y, color) -> None:
        test = self.font.render(test, True, color)
        self.canvas.blit(test, (x,y))

    # -------------------------------------------------------------------------
    # function: initial game
    # -------------------------------------------------------------------------
    def gameReset(self) -> None:
        self.game_mode = False
        self.velocity.reset()
        self.bricks.reset()
    
    #-------------------------------------------------------------------------
    # Main Loop
    #-------------------------------------------------------------------------            
    # -------------------------------------------------------------------------
    # function: type event control
    # -------------------------------------------------------------------------
    def typeEvent(self) -> None:
        for event in pygame.event.get():
            # exit game
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # determine whether to press the ESC button
                self.running = False       
            # manual 
            if event.type == pygame.MOUSEBUTTONDOWN:
                # exit auto mode 
                if self.auto_flag:
                    print("switch to manual")
                    self.auto_flag = False
            if event.type == pygame.MOUSEMOTION:
                if not self.auto_flag:
                    # determine paddle position
                    self.paddle.coordinates[0] = pygame.mouse.get_pos()[0] - (self.paddle.rect[2] / 2)                  
            # auto mode
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                if not self.auto_flag:
                    print("activate automode")
                    self.auto_flag = True
            # start game        
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_mode:
                self.game_mode = True  
            if self.auto_flag and not self.game_mode:
                self.game_mode = True
    #-------------------------------------------------------------------------
    # funtion : paddle edge detect
    #------------------------------------------------------------------------- 
    def paddleEdgeDetect(self) -> int:
        if   self.paddle.coordinates[0] <= 0:
            return 0
        elif self.paddle.coordinates[0] >= self.canvas_width - self.paddle.rect[2]:
            return self.canvas_width - self.paddle.rect[2]
        else:
            return None            
    #-------------------------------------------------------------------------
    # funtion : paddle control
    #------------------------------------------------------------------------- 
    def paddleControl2(self) -> None:
        # paddle edge detect 
        edge = self.paddleEdgeDetect()
        if edge is not None:
            self.paddle.coordinates[0] = edge
        # friction and ball-paddle collision
        upper_paddle = [
            self.paddle.coordinates[0],
            self.paddle.coordinates[1],
            self.paddle.rect[2],
            self.paddle.rect[3] + 50,
        ]
        if not isCollision(self.ball.pos, upper_paddle, self.ball.radius):
            self.f_x = self.paddle.coordinates[0]

        if isCollision(self.ball.pos, self.paddle.rect, self.ball.radius):
            # ball friction
            if self.game_mode:
                delta_x = self.paddle.coordinates[0] - self.f_x
            else:
                delta_x = 0
            velocity = np.array([self.velocity.velocity[0] + 2 * delta_x, - self.velocity.velocity[1]])
            if self.ball.pos[0] + self.ball.radius >= self.paddle.rect[0]: velocity[0] = - velocity[0]
            if self.ball.pos[0] - self.ball.radius <= self.paddle.rect[0] + self.paddle.rect[2]: velocity[0] = - velocity[0]
            # limit operation
            velocity = np.clip(velocity, -self.velocity.speed, self.velocity.speed)
            self.velocity.velocity = velocity
    #-------------------------------------------------------------------------
    # funtion : bricks control = collision control
    #------------------------------------------------------------------------- 
    def brickControl2(self) -> None:
        # collision detect
        target = bvhTrace2(self.bricks.bvh_tree, self.ball.bounding_box, self.velocity.velocity)
        if target:
            # Responses
            self.ball.update([self.ball.pos[0] + self.velocity.velocity[0] * target.bounding_box.collision_time, self.ball.pos[1] + self.velocity.velocity[1] * target.bounding_box.collision_time])
            target.hp -= 1
            if target.hp <= 0:
                self.stylish.cp += 1
                self.stylish.sp += 1
                target.visible = False
                self.bricks.num -= 1 
                self.stylish.stylish()
            # Deflecting
            self.velocity.fix(deflecting(self.ball.pos, target.rect, self.velocity.velocity))
            
    #-------------------------------------------------------------------------
    # funtion : ball control
    #-------------------------------------------------------------------------    
    # 0:waiting for start
    def ballControl(self) -> bool:
        if not self.game_mode:
            self.ball.coordinates = [
                self.paddle.rect[0] + ((self.paddle.rect[2] - self.ball.radius) >> 1), 
                self.paddle.rect[1] - self.ball.radius]
            return None
        # determine whether death
        if self.ball.coordinates[1] + self.velocity.velocity[1] > self.canvas_height - self.ball.radius:
            self.game_mode = False
            self.stylish.sp = 0
            self.paddle.hp -= 1
            self.velocity.reset()
        # right or left wall collision
        if self.ball.coordinates[0] + self.velocity.velocity[0] >= self.canvas_width - self.ball.radius:
            self.velocity.velocity[0] = - self.velocity.velocity[0]
        
        if self.ball.coordinates[0] + self.velocity.velocity[0] <= self.ball.radius:
            self.velocity.velocity[0] = - self.velocity.velocity[0]
        # up wall collision
        if self.ball.coordinates[1] + self.velocity.velocity[1] < self.ball.radius:
            self.velocity.velocity[1] = - self.velocity.velocity[1]
        self.ball.coordinates = list(np.array(self.ball.coordinates) + self.velocity.velocity)
