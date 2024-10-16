# encoding: utf-8
import pygame
from pygame.locals import *
import numpy as np
from wc_set import *
from wc_dev import *



# -------------------------------------------------------------------------
# function: display words
# -------------------------------------------------------------------------
def showFont(text, x, y, color):
    global canvas
    text = font.render(text, True, color)
    canvas.blit(text, (x, y))

# -------------------------------------------------------------------------
# function: initial game
# -------------------------------------------------------------------------
def resetGame():
    # 宣告使用全域變數
    global game_mode, brick_num, bricks_list

    # 磚塊
    for bricks in bricks_list:
        # 磚塊顏色
        bricks.color = color_gray_block
        # 開啟磚塊
        bricks.visible = True
    # 0:等待開球
    game_mode = 0
    # 磚塊數量
    brick_num = playground.brick_num_limmit
    # 移動速度
    resetVelocity()

# -------------------------------------------------------------------------
# function: initial velocity
# -------------------------------------------------------------------------
def resetVelocity():
    global dx, dy
    dx = playground.speed
    dy = -playground.speed



# initialize the game environment
playground = PlayGround0(800, 600, 100, 24, 8, 58, 16, 8, 70, 60, 99, 11, 9, 2, 2)
running, auto_flag = playground.preSetup()

# color
color_gray = (107, 130, 114)
color_gray_block = (20, 31, 23)

# game state
# 0: waiting for start
# 1: the game is running
game_mode = 0

# pygame initialize
pygame.init()
# display title
pygame.display.set_caption("破磚傳奇WallCrusher playground_version")
# create canvas size
canvas = pygame.display.set_mode((playground.canvas_width, playground.canvas_height))
# clock
clock = pygame.time.Clock()
# set font
font = pygame.font.SysFont("simsunnsimsun", 22)

# initialize paddle
paddle_x = playground.paddle_width / 2
paddle_y = playground.canvas_height - 48
paddle = Box(
    pygame,
    canvas,
    "paddle",
    [paddle_x, paddle_y, playground.paddle_width, playground.paddle_height],
    color_gray_block,
)

# initialize bricks
brick_num = 0
brick_w = 0
brick_h = 0
bricks_list = []
for i in range(0, playground.brick_num_limmit):
    if (i % playground.brick_row_limmit) == 0:
        brick_w = 0
        brick_h = brick_h + playground.brick_height + playground.brick_col_space
    bricks_list.append(
        Box(
            pygame,
            canvas,
            "brick_" + str(i),
            [
                brick_w + playground.brick_x,
                brick_h + playground.brick_y,
                playground.brick_width,
                playground.brick_height,
            ],
            color_gray_block,
        )
    )
    brick_w = brick_w + playground.brick_width + playground.brick_row_space
    brick_num += 1

# initialize ball
ball_x = paddle_x
ball_y = paddle_y
ball = Circle(
    pygame, canvas, "ball", [ball_x, ball_x], playground.ball_radius, color_gray_block
)

# initialize stylih system
little_baten = Stylish(0, 0)
# initialize ai
baten = Robot(16, paddle.rect[2] / 4, paddle.rect[2] / 2)

# initialize analysis system
bricks_in = VelocityAnalyzer('bricks_in_velocity.csv')
bricks_out= VelocityAnalyzer('bricks_out_velocity.csv')
paddle_analyzer = VelocityAnalyzer('paddle_analyze.csv')
bricks_in.fileSetup()
bricks_out.fileSetup()
paddle_analyzer.fileSetup()

# initialize game
resetGame()

# -------------------------------------------------------------------------
# main loop
# -------------------------------------------------------------------------
while running:
    # clear screen
    canvas.fill(color_gray)

    for event in pygame.event.get():
        # exit game
        if event.type == pygame.QUIT:
            running = False
        # determine button press
        if event.type == pygame.KEYDOWN:
            # determine whether to press the ESC button
            if event.key == pygame.K_ESCAPE:
                running = False
        # determine whether to enter auto mode
        if not auto_flag:
            # determine mouse position
            if event.type == pygame.MOUSEMOTION:
                paddle_x = pygame.mouse.get_pos()[0] - (paddle.rect[2] / 2)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_mode == 0:
                    game_mode = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    print("activate automode")
                    auto_flag = True
        if auto_flag:
            # exit auto mode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_mode == 0:
                    game_mode = 1
                print("switch to manual")
                auto_flag = False
    # if have entered auto mode
    if auto_flag:
        if game_mode == 1:
            paddle_control = baten.detect(
                playground.canvas_width,
                paddle_x,
                ball.pos[0],
                paddle.rect[2] / 2,
            )
            paddle_x += paddle_control
            
    # -------------------------------------------------------------------------
    # Paddle
    # -------------------------------------------------------------------------
    # friction pre processing
    upper_paddle = [
        paddle_x,
        paddle_y,
        paddle.rect[2],
        paddle.rect[3] + 100,
    ]
    # collision response - ball hits paddle
    if not isCollision(ball.pos[0], ball.pos[1], upper_paddle, ball.radius):
        f_x = paddle_x
    else:
        if auto_flag:
            paddle_x += baten.control1()
    if isCollision(ball.pos[0], ball.pos[1], paddle.rect, ball.radius):
        # ball friction
        delta_x = paddle_x - f_x
        velocity = np.array([dx + delta_x, -dy])
        # limit operation
        velocity = np.clip(velocity, -playground.speed, playground.speed)
        dx = velocity[0]
        # ball bounce
        dy = velocity[1]
        # velocity record
        paddle_analyzer.recorder(paddle.name, dx, dy) 
        
    # update paddle
    paddle.rect[0] = paddle_x
    paddle.update()
    
    # -------------------------------------------------------------------------
    # Bricks
    # -------------------------------------------------------------------------
    for bricks in bricks_list:
        # ball velocity
        velocity = np.array([dx, dy])
        # collision response - ball hits bricks
        if bricks.visible:
            is_collision, velocity = collisionResponse(
                ball.pos, ball.radius, velocity, bricks.rect, 8
            )
            if is_collision:
                # velocity record
                bricks_in.recorder(bricks.name, dx, dy)
                # change velocity
                dx, dy = velocity
                bricks.visible = False
                brick_num -= 1
                little_baten.cp += 1
                little_baten.sp += 1
                # velocity record
                bricks_out.recorder(bricks.name, dx, dy)
                
                if brick_num <= 0:
                    resetGame()
                    break
        # update bricks
        bricks.update()
        
    # -------------------------------------------------------------------------
    # Ball
    # -------------------------------------------------------------------------
    # 0:waiting for start
    if game_mode == 0:
        ball.pos[0] = ball_x = paddle.rect[0] + ((paddle.rect[2] - ball.radius) >> 1)
        ball.pos[1] = ball_y = paddle.rect[1] - ball.radius
        if auto_flag:
            game_mode = 1
    # 1:if game is running
    elif game_mode == 1:
        ball_x += dx
        ball_y += dy
        # determine whether death
        if ball_y + dy > playground.canvas_height - ball.radius:
            little_baten.sp = 0
            resetVelocity()
            game_mode = 0
        # temporary handling of the ball flying out of the boundery due to excessive speed
        if ball_x + dx >= playground.canvas_width + ball.radius or ball_x + dx <= - ball.radius:
            resetVelocity()
            game_mode = 0
        # right or left wall collision
        if (
            ball_x + dx >= playground.canvas_width - ball.radius
            or ball_x + dx <= ball.radius
        ):
            dx = -dx
            ball.pos[0] += dx * 2
        # up ro down wall collision
        if (
            ball_y + dy > playground.canvas_height - ball.radius
            or ball_y + dy < ball.radius
        ):
            dy = -dy
            ball.pos[0] += dy * 2
        ball.pos[0] = ball_x
        ball.pos[1] = ball_y
    # update ball
    ball.update()
    
    # display FPS
    showFont("FPS:" + str(int(clock.get_fps())), 8, 4, color_gray_block)
    # display the number of bricks
    showFont("BRICKS:" + str(brick_num), 8, 20, color_gray_block)
    # display score
    showFont("SCORE:" + str(little_baten.cp * 5), 8, 36, color_gray_block)
    # display sp
    showFont(str(little_baten.sp), 8, 52, color_gray_block)
    # showFont(str(little_baten.stylish()), 8, 52, color_gray_block)
    
    # update screen
    pygame.display.update()
    clock.tick(60)
    
# exit game
pygame.quit()
quit()
