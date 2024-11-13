# encoding: utf-8
import pygame
from pygame.locals import *
from src.game import *
from src.env_dev import *
from analysis.wc_plot import *
from ml.robot import *

# initialize the game environment
game = PlayGround0(
    canvas_width    = 800,
    canvas_height   = 600,
    paddle_width    = 100,
    paddle_height   = 24,
    ball_radius     = 8,
    brick_width     = 58,
    brick_height    = 16,
    brick_num_limmit= 99,
    brick_row_limmit= 11,
    brick_col_limmit= 9,
    brick_row_space = 2,
    brick_col_space = 2,
    speed           = 8)
game.running = game.preSetup()
# initialize ai
baten = Robot(
    speed = 16, 
    deadzone = game.paddle.rect[2] / 4,
    delta = game.paddle.rect[2] / 2)
# initialize analysis system
bricks_in = VelocityAnalyzer("bricks_in_velocity.csv")
bricks_out = VelocityAnalyzer("bricks_out_velocity.csv")
paddle_analyzer = VelocityAnalyzer("paddle_out_velocity.csv")
tree_graph = visualize_bvh(game.bricks.bvh_tree)
tree_graph.render("analysis/bvh_tree", format="png", view=False)
# initialize game
game.gameReset()

# -------------------------------------------------------------------------
# main loop
# -------------------------------------------------------------------------
while game.running:
    # clear screen
    game.canvas.fill(game.color_gray)
    # game type event
    game.typeEvent()
    # if have entered auto mode
    if game.auto_flag and game.game_mode:
        game.paddle.coordinates[0] += baten.control0(
            paddle_x_center = game.paddle.coordinates[0] + (game.paddle.rect[2] / 2), 
            ball_x_center   = game.ball.pos[0])
    # -------------------------------------------------------------------------
    # Paddle
    # -------------------------------------------------------------------------        
    if not game.auto_flag:
        tmp = 0
    else:
        tmp = baten.control1()
    game.paddleControl(auto = tmp)
    # update paddle
    game.paddle.update()
    # -------------------------------------------------------------------------
    # Bricks
    # -------------------------------------------------------------------------
    game.brickControl2()
    if game.bricks.num <= 0:
        game.gameReset()
    # -------------------------------------------------------------------------
    # Ball
    # -------------------------------------------------------------------------
    game.ballControl()
    # update ball
    game.ball.update(game.ball.coordinates)
    
    # -------------------------------------------------------------------------
    # Display
    # -------------------------------------------------------------------------
    # display paddle
    game.paddle.display()
    # display bricks
    game.bricks.display()
    # display ball
    game.ball.display()
    # display FPS
    game.showFont("FPS:" + str(int(game.clock.get_fps())), 8, 4, game.color_gray_block)
    # display the number of bricks
    game.showFont("BRICKS:" + str(game.bricks.num), 8, 20, game.color_gray_block)
    # display score
    game.showFont("SCORE:" + str(game.stylish.score), 8, 36, game.color_gray_block)
    # display sp
    game.showFont(str(game.stylish.sp), 8, 52, game.color_gray_block)
    
    # update screen
    pygame.display.update()
    game.clock.tick(60)
