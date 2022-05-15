#!/usr/bin/env python
# license removed for brevity

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from user_interface.msg import navigation
from std_msgs.msg import String, Bool


cords = [0.0, 0.0]
counter = 0

class navigation_goals:
    def __init__(self):
        rospy.init_node('movebase_client_py')
        rospy.Subscriber('/navigation_cord', navigation, self.navigation_cb)   # comes from behaviour planner X,Y location
        rospy.Subscriber('/stop_signal', Bool, self.local_plan_cb)      # comes from local planner
        self.navigation_msg = rospy.Publisher('/navigation_status', String, queue_size=10)  # goes to behaviour planner
        self.nav_status = ""
        self.path_abort = False
        self.counter = 0
        self.move = 0
        self.client = 0
        self.goal = 0
    def local_plan_cb(self, msg):
        self.path_abort = msg.data
        if self.path_abort:
            self.client.cancel_goal()
        else:
            self.client.send_goal(self.goal, self.done_cb, self.active_cb, self.feedback_cb)

    def active_cb(self):
        # print('I am in active cb')
        # rospy.loginfo('goal pose being processed')
        pass

    def feedback_cb(self,feedback):
        pass
        # here you get the current location of the robot
        # print('I am in feedback_cb')
        # self.counter +=1
        # print(self.counter)
        # if self.counter >200:
        #     self.move.cancel_goal()

        # rospy.loginfo('Current Location {}'.format(feedback))

    def done_cb(self,status, result):
        # print('I am in done _cb')
        if status == 1:
            self.nav_status = "status1"
            self.publish()
            self.nav_status = ""
            rospy.loginfo("goal reached")
        if status == 2 or status == 8:
            self.nav_status = "goal cancelled"
            self.publish()
            self.nav_status = ""
            self.publish()
            rospy.loginfo("goal cancelled")
        if status == 3:
            self.nav_status = "status3"
            self.publish()
            self.nav_status = ""
            self.publish()
        if status == 4:
            self.nav_status = "status4"
            self.publish()
            self.nav_status = ""
            self.publish()
            rospy.loginfo('goal aborted')

    def movebase_client(self):
        # cords[0] = 4
        # cords[1] = 5
        print(cords)
        # cords[0] = -4.59300374985
        # cords[1] = -3.32144927979
        # x = -4.59300374985
        # y =  -3.32144927979

        if cords[0] != 0 or cords[1] != 0:
            print("I am in if")
            self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
            self.client.wait_for_server()
            self.move = self.client
            self.goal = MoveBaseGoal()
            self.goal.target_pose.header.frame_id = "map"
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position.x = cords[0]
            self.goal.target_pose.pose.position.y = cords[1]
            self.goal.target_pose.pose.orientation.w = 1.0

            # client.cancel_goal()

            self.client.send_goal(self.goal, self.done_cb, self.active_cb, self.feedback_cb)
            if self.path_abort:
                self.client.cancel_goal()

            wait = self.client.wait_for_result()

            if not wait:
                rospy.logerr("Action server not available!")
                rospy.signal_shutdown("Action server not available!")
            else:
                return self.client.get_result()

    def navigation_cb(self, msg):
        cords[0] = msg.X
        cords[1] = msg.Y

    def main_action(self):
        result = self.movebase_client()
        if result:
            self.nav_status = "Goal execution done!"
            # self.publish()
            # rospy.loginfo("Goal execution done!")

    def publish(self):
        print(self.nav_status)
        self.navigation_msg.publish(self.nav_status)


if __name__ == '__main__':
    ng = navigation_goals()
    r = rospy.Rate(60)
    while not rospy.is_shutdown():
        ng.main_action()
        r.sleep()

# topic s and its functionalities
# /move_base_simple/goal    := we get the current goal using this topic
#/move_base/cancel
# /move_base/current_goal
# /move_base/feedback



# got to goal
# goal reached


# check wheter the node keepes on running when the client hase sent the goal and is in feedback function
