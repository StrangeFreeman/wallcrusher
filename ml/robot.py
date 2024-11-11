# encoding: utf-8
import random

#-------------------------------------------------------------------------
# simple ai test system
#-------------------------------------------------------------------------
class Robot(object):
    def __init__(self, speed: int, deadzone: int, delta: int) -> None:
        self.robot_speed = speed
        self.deadzone = deadzone
        self.delta = delta
        
    def control0(self, paddle_x_center: int, ball_x_center: int) -> int:
        if paddle_x_center < ball_x_center - self.deadzone:
            return self.robot_speed
        elif paddle_x_center > ball_x_center + self.deadzone:
            return (- self.robot_speed)
        else:
            return 0
        
    def control1(self) -> float:
        return random.uniform(-self.delta, self.delta)
        