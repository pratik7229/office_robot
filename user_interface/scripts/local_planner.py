#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32, Float32, Bool
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist

class local_planner:
    def __init__(self):
        rospy.init_node('local_planner', anonymous=False)
        # publishers
        self.motor_control = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.motor_speed = Twist()
        self.motor_speed.linear.x = 0.0
        self.motor_speed.angular.z = 0.0

        self.stop = rospy.Publisher('/stop_signal', Bool, queue_size=10)
        # Subscriber
        rospy.Subscriber('/IR_front_left', Bool, self.ir1_callback)  # ir sensor front
        rospy.Subscriber('/IR_front_right', Bool, self.ir2_callback)  # ir sensor back
        rospy.Subscriber('/ultrasound_back', Range, self.ultrasonic1_cb)  # ultrasonic sensor front
        rospy.Subscriber('/ultrasound_front', Range, self.ultrasonic2_cb)  # ultrasonic sensor back

        self.ultrasonic = [0.0, 0.0]  # [Front, back] distance values
        self.ir_sensor = [False, False]  # [Front, back] boolean values
        self.abort_path = False

    def ir1_callback(self, msg):
        self.ir_sensor[0] = msg.data

    def ir2_callback(self, msg):
        self.ir_sensor[1] = msg.data

    def ultrasonic1_cb(self, msg):
        self.ultrasonic[0] = msg.range

    def ultrasonic2_cb(self, msg):
        self.ultrasonic[1] = msg.range

    def main_control(self):
        if self.ir_sensor[0] and self.ir_sensor[1] and self.ultrasonic[0] > 100 and self.ultrasonic[1] > 100:
            self.abort_path = False
            self.stop.publish(self.abort_path)
        else:
            if not self.ir_sensor[0]:
                # front Ir sensor at fall detected
                self.motor_speed.linear.x = 0.0
                self.motor_speed.angular.z = 0.0
                self.abort_path = True
                self.publish(self.abort_path, self.motor_speed)
            elif not self.ir_sensor[1]:
                # front Ir sensor at fall detected
                self.motor_speed.linear.x = 0.0
                self.motor_speed.angular.z = 0.0
                self.abort_path = True
                self.publish(self.abort_path, self.motor_speed)

            if self.ultrasonic[0] <= 100:
                # front Ir sensor at fall detected
                self.motor_speed.linear.x = 0.0
                self.motor_speed.angular.z = 0.0
                self.abort_path = True
                self.publish(self.abort_path, self.motor_speed)

            elif self.ultrasonic[1] <= 100:
                # front Ir sensor at fall detected
                self.motor_speed.linear.x = 0.0
                self.motor_speed.angular.z = 0.0
                self.abort_path = True
                self.publish(self.abort_path, self.motor_speed)



    def publish(self, path, speed):
        self.stop.publish(path)
        self.motor_control.publish(speed)



if __name__ == '__main__':
    pln = local_planner()
    r = rospy.Rate(60)
    while not rospy.is_shutdown():
        pln.main_control()
        r.sleep()
