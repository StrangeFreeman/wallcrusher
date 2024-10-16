from wc_dev import *
        

# initialize velocity analyzer
bricks_in = VelocityAnalyzer('bricks_in_velocity.csv')
# bricks_out= VelocityAnalyzer('bricks_out_velocity.csv')
# paddle_analyzer = VelocityAnalyzer('paddle_analyze.csv')

bricks_in.reader()
# bricks_out.reader()
# paddle_analyzer.reader()

# bricks_in.scatterPlotter('ball-brick in velocity')
# bricks_out.scatterPlotter('ball-brick out velocity')
# paddle_analyzer.scatterPlotter('ball-paddle out velocity')

dynamic_bricks_in = DynamicScatterPlotter(bricks_in.data, 'bricks_in_velocity.csv')
dynamic_bricks_in.show()
    
    