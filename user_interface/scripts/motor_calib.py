#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import time



def motor_cabself():
    rospy.init_node('motor_caliberation', anonymous=True)
    motor_linear = rospy.Publisher('/cmd_vel', Twist,queue_size=10)
    rate = rospy.Rate(1)
    motor_speed = Twist()
    while True:
        motor_speed.linear.x = 0.6
        motor_speed.angular.z = 0
        break
    motor_speed.linear.x = 0
    motor_speed.angular.z = 0


motor_cabself()

# battery, 
# class main_window:
#     def __init__(self):
#         rospy.init_node('main_window', anonymous=False)
#         self.twist_now = rospy.Publisher('/cmd_vel', Twist, queue_size=10 )
#         self.linear_x = self.twist_now.Twist.linear_x
#         self.counter = 0
#         self.motor_speed = 0.6
#         self.time_start = 0
#     def motor_clib(self):
#         self.linear_x = 0.6
#         if self.counter == 0:
#             self.twist_now.publish(self.linear_x)
#             self.counter += 1
#         else:
#             self.linear_x = 0
#             self.twist_now.publish(self.linear_x)
# if __name__=='__main__':
#     mw = main_window()
#     r = rospy.Rate(1)
#     while not rospy.is_shutdown():
#         r.sleep()