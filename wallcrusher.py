# encoding: utf-8

import pygame
from pygame.locals import *
from wc_set import *
import numpy as np

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
        bricks.visivle = True
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
    dy = - playground.speed

# initialize the game environment
playground = PlayGround0(800, 600, 100, 24, 8, 58, 16, 8, 70, 60, 99, 11, 9, 2, 2)
running = True

# color
color_gray = (107, 130, 114)
color_gray_block = (20, 31, 23)

# game state
# 0: waiting for start
# 1: the game is running
game_mode = 0

# pygame initialize
pygame.init()
# show title
pygame.display.set_caption("破磚傳奇WallCrusher")
# create canvas size
canvas = pygame.display.set_mode((playground.canvas_width, playground.canvas_height))
# clock
clock = pygame.time.Clock()
# set font
font = pygame.font.SysFont("simsunnsimsun", 18)

# initialize paddle
paddle_x = 0
paddle_y = playground.canvas_height - 48
paddle = Box(pygame, canvas, "paddle", [paddle_x, paddle_y, playground.paddle_width, playground.paddle_height], color_gray_block)

# initialize bricks
brick_num = 0
brick_w = 0
brick_h = 0
bricks_list = []

for i in range(0, playground.brick_num_limmit):
    if (i % playground.brick_row_limmit) == 0:
        brick_w = 0
        brick_h =  brick_h + playground.brick_height + playground.brick_col_space
    bricks_list.append(
        Box(
            pygame,
            canvas,
            "brick_" + str(i),
            [brick_w + playground.brick_x, brick_h + playground.brick_y, playground.brick_width, playground.brick_height],
            color_gray_block,
        )
    )
    brick_w = brick_w + playground.brick_width + playground.brick_row_space
    brick_num += 1

# initialize ball
ball_x = paddle_x
ball_y = paddle_y
ball = Circle(pygame, canvas, "ball", [ball_x, ball_x], playground.ball_radius, color_gray_block)

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
        # determine mouse position
        if event.type == pygame.MOUSEMOTION:
            paddle_x = pygame.mouse.get_pos()[0] - (playground.paddle_width/2)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_mode == 0:
                game_mode = 1

    # -------------------------------------------------------------------------
    # Paddle
    # -------------------------------------------------------------------------
    # friction pre processing
    upper_paddle = [paddle_x, paddle_y, playground.paddle_width, playground.paddle_height + 100]
    # collision response - ball hits paddle
    if not isCollision(ball.pos[0], ball.pos[1], upper_paddle, playground.ball_radius):
        f_x = paddle_x
            
    if isCollision(ball.pos[0], ball.pos[1], paddle.rect, playground.ball_radius):
        # ball friction
        delta_x = paddle_x - f_x
        velocity = np.array([dx + delta_x, -dy])
        # limit operation
        velocity = np.clip(velocity, -playground.speed, playground.speed)
        dx = velocity[0]
        # ball bounce
        dy = velocity[1]
        
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
        if bricks.visivle:
            is_collision, velocity= collisionResponse(ball.pos, playground.ball_radius, velocity, bricks.rect, 8)
            if is_collision:
                dx, dy = velocity
            
                bricks.visivle = False
                brick_num -= 1
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
    # 1:if game is running
    elif game_mode == 1:
        ball_x += dx
        ball_y += dy
        # determine whether death
        if ball_y + dy > playground.canvas_height - ball.radius or ball_x + dx > playground.canvas_width + 2 or ball_x + dx < -2:
            game_mode = 0
            resetVelocity()
        # right or left wall collision
        if ball_x + dx >= playground.canvas_width - (ball.radius * 2) or ball_x + dx <= (ball.radius * 2):
            dx = -dx
        # up ro down wall collision
        if ball_y + dy > playground.canvas_height - ball.radius or ball_y + dy < ball.radius:
            dy = -dy
        ball.pos[0] = ball_x
        ball.pos[1] = ball_y

    # update ball
    ball.update()

    # display FPS
    showFont("FPS:" + str(int(clock.get_fps())), 8, 2, color_gray_block)
    # display the number of bricks
    showFont("BRICKS:" + str(brick_num), 8, 20, color_gray_block)

    # update screen
    pygame.display.update()
    clock.tick(60)

# exit game
pygame.quit()
quit()
