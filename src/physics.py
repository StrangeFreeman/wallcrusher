# encoding: utf-8
import numpy as np
# -------------------------------------------------------------------------
# function: collision detect
# input:
#       x       : x
#       y       : y
#       boxRect : [x, y, width, height]
#       radius  : radius
# -------------------------------------------------------------------------
def isCollision(ball_pos, boxRect, radius) -> bool:
    if (
        ball_pos[0] + radius > boxRect[0]                      # 球和物體左側碰撞檢測 
        and ball_pos[0] - radius < boxRect[0] + boxRect[2]     # 球和物體右側碰撞檢測
        and ball_pos[1] + radius > boxRect[1]                  # 球和物體下側碰撞檢測
        and ball_pos[1] - radius < boxRect[1] + boxRect[3]     # 球和物體上側碰撞檢測
    ):
        return True
    return False

# -------------------------------------------------------------------------
# BVH tree
# -------------------------------------------------------------------------
class BoundingBox(object):
    #-------------------------------------------------------------------------
    # constructive
    #   min_point   : [x, y]        or [x-r, y-r]
    #   max_point   : [x+w, y+h]    or [x+r, y+r]
    #-------------------------------------------------------------------------
    def __init__(self, min_point: list, max_point: list) -> None:
        self.min_point = min_point
        self.max_point = max_point
        
    def intersect2(self, other, velocity: np) -> bool:
        d_entry = np.array([self.min_point[0] - other.max_point[0], self.min_point[1] - other.max_point[1]])
        d_exit  = np.array([self.max_point[0] - other.min_point[0], self.max_point[1] - other.min_point[1]])
        t_entry = np.zeros(2)
        t_entry = np.zeros(2)
        if velocity[0] < 0: d_entry[0], d_exit[0] = d_exit[0], d_entry[0]
        if velocity[1] < 0: d_entry[1], d_exit[1] = d_exit[1], d_entry[1] 
        for i in range(2):
            if velocity[i] == 0:
                t_entry[i] = -np.inf
                t_exit[i]  =  np.inf
            else:
                t_entry = d_entry / velocity
                t_exit  = d_exit  / velocity  
        entry_time = max(t_entry[0], t_entry[1])
        exit_time  = min( t_exit[0],  t_exit[1])
        if t_entry[0] > t_exit[1] or t_entry[1] > t_exit[0]: return False
        if entry_time >= 1 or exit_time <= 0: return False
        self.collision_time = entry_time
        return True
    
class BVHNode(object):
    #-------------------------------------------------------------------------
    # constructive
    #   bounding_box = min_point, max_point
    #   left         = left  child
    #   right        = right child
    #   brick        = brick
    #-------------------------------------------------------------------------
    def __init__(self, bounding_box, left = None, right = None, brick = None) -> None:
        self.bounding_box = bounding_box
        self.left = left
        self.right = right
        self.brick = brick
        
def build_bvh(bricks: list) -> BVHNode:
    if not bricks:
        return None
    if len(bricks) == 1:
        bounding_box = bricks[0].bounding_box
        return BVHNode(bounding_box, None, None, bricks[0])
    x_range = max(brick.bounding_box.max_point[0] for brick in bricks) - min(brick.bounding_box.min_point[0] for brick in bricks)
    y_range = max(brick.bounding_box.max_point[1] for brick in bricks) - min(brick.bounding_box.min_point[1] for brick in bricks)
    axis = 0 if x_range > y_range else 1
    bricks.sort(key = lambda brick: (brick.bounding_box.min_point[axis] + brick.bounding_box.max_point[axis]) / 2)
    mid = len(bricks) // 2
    left_node = build_bvh(bricks[:mid])
    right_node = build_bvh(bricks[mid:])
    min_point = [min(left_node.bounding_box.min_point[0], right_node.bounding_box.min_point[0]),
                min(left_node.bounding_box.min_point[1], right_node.bounding_box.min_point[1])]
    max_point = [max(left_node.bounding_box.max_point[0], right_node.bounding_box.max_point[0]),
                max(left_node.bounding_box.max_point[1], right_node.bounding_box.max_point[1])]
    bounding_box = BoundingBox(min_point, max_point)
    return BVHNode(bounding_box, left_node, right_node)

# -------------------------------------------------------------------------
# function: bvh tree tracer
# input : 
#           node: BVHNode
#           ball_bounding_box: BoundingBox
#           velocity: numpy array
# -------------------------------------------------------------------------
def bvhTrace2(node: BVHNode, ball_bounding_box: BoundingBox, velocity: np) -> list:
    if node is None:
        return None
    if not node.bounding_box.intersect2(ball_bounding_box, velocity):
        return None
    if node.brick is not None and node.brick.visible:
        return node.brick
    left_collision = bvhTrace2(node.left, ball_bounding_box, velocity)
    if left_collision:
        return left_collision
    return bvhTrace2(node.right, ball_bounding_box, velocity)

def response():
    pass

# -------------------------------------------------------------------------
# function: orthoprojection(project a vector on b vector)
# input : 
#           a: numpy array
#           b: numpy array
# -------------------------------------------------------------------------
def projection(a: np, b: np) -> np:
    divided = np.dot(b, b)
    if divided != 0:
        projection = (np.dot(a, b) / divided) * b
    else:
        projection = np.zeros_like(b)
    return projection

# -------------------------------------------------------------------------
# function: collision response - deflecting
# input : 
#           ball_pos : list
#           box_rect : list
#           velocity : numpy array
# ------------------------------------------------------------------------- 
def deflecting(ball_pos: list, box_rect: list, velocity: np) -> np:
    ball_center = np.array(ball_pos)
    brick_half_extents = np.array([box_rect[2]/2, box_rect[3]/2])   
    brick_center = np.array([box_rect[0], box_rect[1]]) + brick_half_extents
    dist = ball_center - brick_center
    # limit operations
    clampd = np.clip(dist, -brick_half_extents, brick_half_extents)
    closest = brick_center + clampd
    dist = closest - ball_center
    velocity = velocity + (- projection(velocity, dist) * 2)
    return velocity

def deflecting2(ball_pos: list, collision_time: float, velocity: np) -> np:
    ball_center     = np.array(ball_pos)
    collision_point = np.array([ball_pos[0] + velocity[0] * collision_time, ball_pos[1] + velocity[1] * collision_time])
    dist = collision_point - ball_center
    velocity = velocity + (- projection(velocity, dist) * 2)
    print(velocity)
    return velocity