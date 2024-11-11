# encoding: utf-8
from src.env import *
from src.game import *

#-------------------------------------------------------------------------
# set basic game parameters 2
#-------------------------------------------------------------------------       
class PlayGround0(Game):
    def __init__(self, canvas_width: int, canvas_height: int, paddle_width: int, paddle_height: int, ball_radius: int, brick_width: int, brick_height: int, brick_num_limmit: int, brick_row_limmit: int, brick_col_limmit: int, brick_row_space: int, brick_col_space: int, speed: int) -> None:
        super().__init__(canvas_width, canvas_height, paddle_width, paddle_height, ball_radius, brick_width, brick_height, brick_num_limmit, brick_row_limmit, brick_col_limmit, brick_row_space, brick_col_space, speed)
        self.parameters = {
            'canvas_width': canvas_width,
            'canvas_height': canvas_height,
            'paddle_width': paddle_width,
            'paddle_height': paddle_height,
            'ball_radius': ball_radius,
            # 'brick_x': self.brick_x,
            # 'brick_y': self.brick_y,
            'brick_num_limmit': brick_num_limmit,
            'brick_row_limmit': brick_row_limmit,
            'brick_col_limmit': brick_col_limmit,
            'brick_row_space': brick_row_space,
            'brick_col_space': brick_col_space,
            'brick_width': brick_width,
            'brick_height': brick_height,
            'speed': speed
        }
        
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
    
    def getYesNo(self, prompt: str, default: str) -> bool:
        if default.lower() == 'y':
            prompt = f"{prompt}(Y/n) "
        else:
            prompt = f"{prompt}(y/N) "

        user_input = input(prompt).strip().lower()
        if user_input == '':
            user_input = default.lower()
        
        return user_input in ['yes', 'y']
    
    def inputParameters(self, prompt: str, default: str) -> bool:
        user_input = input(f"{prompt}({default}) ")
        return int(user_input) if user_input != '' else default
    
    def setParameters(self, flag) -> None:
        if flag == 'set':
            for key in self.parameters:
                self.parameters[key] = self.inputParameters(key, self.parameters[key])
                
        self.updateParameter()
        self.title = "破磚傳奇WallCrusher playground ver."
        
        # color
        self.color_gray = (107, 130, 114)
        self.color_gray_block = (20, 31, 23)
        
        # pygame initialize
        pygame.init()
        # display title
        pygame.display.set_caption(self.title)
        # create canvas size
        self.canvas = pygame.display.set_mode((self.canvas_width, self.canvas_height))
        
        self.paddle = Paddle(
            pygame = pygame,
            canvas = self.canvas,
            name = "paddle",
            rect = [self.canvas_width / 2, self.canvas_height - 48, self.paddle_width, self.paddle_height],
            color = self.color_gray_block,
            hp = 3,
            coordinates = [self.canvas_width / 2, self.canvas_height - 48]
        )
        
        self.bricks = Bricks(
            pygame= pygame,
            width = self.brick_width,
            height = self.brick_height,
            num_limmit = self.brick_num_limmit,
            row_limmit = self.brick_row_limmit,
            col_limmit = self.brick_col_limmit,
            row_space = self.brick_row_space,
            col_space = self.brick_col_space
        )
        self.bricks.listInit(self.canvas)
        
        self.ball = Ball(
            pygame = pygame,
            canvas = self.canvas,
            name = "ball",
            pos = [self.paddle.coordinates[0], self.paddle.coordinates[1]],
            radius = self.ball_radius,
            color = self.color_gray_block,
            coordinates = [self.paddle.coordinates[0], self.paddle.coordinates[1]]
        )
        
        self.velocity = Velocity(self.speed)
        self.f_x = None
    
    def updateParameter(self) -> None:
        self.canvas_width = self.parameters['canvas_width']
        self.canvas_height = self.parameters['canvas_height']
        self.paddle_width = self.parameters['paddle_width']
        self.paddle_height = self.parameters['paddle_height']
        self.ball_radius = self.parameters['ball_radius']
        self.brick_width = self.parameters['brick_width']
        self.brick_height = self.parameters['brick_height']
        self.speed = self.parameters['speed']
        # self.brick_x = self.parameters['brick_x']
        # self.brick_y = self.parameters['brick_y']
        self.brick_num_limmit = self.parameters['brick_num_limmit']
        self.brick_row_limmit = self.parameters['brick_row_limmit']
        self.brick_col_limmit = self.parameters['brick_col_limmit']
        self.brick_row_space = self.parameters['brick_row_space']
        self.brick_col_space = self.parameters['brick_col_space']
    
    def preSetup(self) -> bool:
        self.banner()
        q_custom = self.getYesNo('Custom setting?', 'n')
        if not q_custom:
            self.setParameters('default')
            return True
        self.setParameters('set')
        q_continue = self.getYesNo('Continue?', 'y')
        if not q_continue:
            return self.preSetup()
        q_auto = self.getYesNo('Auto Mode?', 'y')
        if q_auto:
            self.auto_flag = True
        return True
    
    def paddleControl(self, auto) -> None:
        upper_paddle = [
            self.paddle.coordinates[0],
            self.paddle.coordinates[1],
            self.paddle.rect[2],
            self.paddle.rect[3] + 50,
        ]
        if not isCollision(self.ball.pos, upper_paddle, self.ball.radius):
            self.f_x = self.paddle.coordinates[0]
        else:
            # random motion
            if self.auto_flag == 1:
                self.paddle.coordinates[0] += auto
        if isCollision(self.ball.pos, self.paddle.rect, self.ball.radius):
            # ball friction
            if self.game_mode:
                delta_x = self.paddle.coordinates[0] - self.f_x
            else:
                delta_x = 0
            velocity = np.array([self.velocity.velocity[0] + 2*delta_x, - self.velocity.velocity[1]])
            velocity = np.clip(velocity, -self.velocity.speed, self.velocity.speed)
            # limit operation
            self.velocity.update(velocity = velocity)
        