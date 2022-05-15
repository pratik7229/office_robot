#!/usr/bin/env python
# # license removed for brevity
#
# import rospy
# from std_msgs.msg import Int32, Float32, Bool
#
# # Brings in the SimpleActionClient
# import actionlib
# # Brings in the .action file and messages used by the move base action
# from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
# from user_interface.msg import navigation
#
# cords = [0.0, 0.0]
# counter = 0
#
# class navigation_goals:
#     def __init__(self):
#         rospy.init_node('movebase_client_py')
#         rospy.Subscriber('/navigation_cord', navigation, self.navigation_cb)
#
#     def active_cb(self):
#         rospy.loginfo('goal pose being processed')
#
#     def feedback_cb(self,feedback):
#         rospy.loginfo('Current Location {}'.format(feedback))
#
#     def done_cb(self,status, result):
#         if status == 1:
#             rospy.loginfo("goal reached")
#         if status == 2 or status == 8:
#             rospy.loginfo("goal cancelled")
#         if status == 4:
#             rospy.loginfo('goal aborted')
#
#     def movebase_client(self):
#
#         client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
#         client.wait_for_server()
#
#         goal = MoveBaseGoal()
#         goal.target_pose.header.frame_id = "map"
#         goal.target_pose.header.stamp = rospy.Time.now()
#         goal.target_pose.pose.position.x = 0.5
#         goal.target_pose.pose.orientation.w = 1.0
#
#         client.send_goal(goal)
#         wait = client.wait_for_result()
#         if not wait:
#             rospy.logerr("Action server not available!")
#             rospy.signal_shutdown("Action server not available!")
#         else:
#             return client.get_result()
#
#
#        # Sends the goal to the action server.
#         client.send_goal(goal, self.done_cb, self.active_cb, self.feedback_cb)
#         # if counter == 1000:
#         #     counter += 1
#         #     client.cancelAllGoals()
#        # Waits for the server to finish performing the action.
#         wait = client.wait_for_result()
#        # If the result doesn't arrive, assume the Server is not available
#         if not wait:
#             rospy.logerr("Action server not available!")
#             rospy.signal_shutdown("Action server not available!")
#         else:
#         # Result of executing the action
#             return client.get_result()
#
#     def navigation_cb(self,msg):
#         cords[0] = msg.X
#         cords[1] = msg.Y
#
#     def main_action(self):
#
#         result = self.movebase_client()
#         if result:
#             rospy.loginfo("Goal execution done!")
#
# # If the python node is executed as main process (sourced directly)
# if __name__ == '__main__':
#     ng = navigation_goals()
#     r = rospy.Rate(60)
#     while not rospy.is_shutdown():
#         ng.main_action()
#         r.sleep()
#
#
#
# #!/usr/bin/env python
# # license removed for brevity
#
# import rospy
# import actionlib
# from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
#
#
# def active_cb():
#     rospy.loginfo('goal pose being processed')
#
#
# def feedback_cb(feedback):
#     rospy.loginfo('Current Location {}'.format(feedback))
#
#
# def done_cb(status, result):
#     if status == 1:
#         rospy.loginfo("goal reached")
#     if status == 2 or status == 8:
#         rospy.loginfo("goal cancelled")
#     if status == 4:
#         rospy.loginfo('goal aborted')
#
#
# def movebase_client():
#
#     client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
#     client.wait_for_server()
#
#     goal = MoveBaseGoal()
#     goal.target_pose.header.frame_id = "map"
#     goal.target_pose.header.stamp = rospy.Time.now()
#     goal.target_pose.pose.position.x = 0.5
#     goal.target_pose.pose.orientation.w = 1.0
#     client.send_goal(goal, done_cb, active_cb, feedback_cb)
#
#     wait = client.wait_for_result()
#     if not wait:
#         rospy.logerr("Action server not available!")
#         rospy.signal_shutdown("Action server not available!")
#     else:
#         return client.get_result()
#
# if __name__ == '__main__':
#     try:
#         rospy.init_node('movebase_client_py')
#         result = movebase_client()
#         if result:
#             rospy.loginfo("Goal execution done!")
#     except rospy.ROSInterruptException:
#         rospy.loginfo("Navigation test finished.")

import rospy
from std_msgs.msg import Int32, Float32, Bool, String
from user_interface.msg import navigation, appMsg
from comm_firebase.msg import call_rec_name
from Confirmation_window import ConfWindow

class Behavoiur_planner:
    def __init__(self):
        rospy.init_node('Behavoiur_planner', anonymous=False)
        # publishers
        self.lock = rospy.Publisher('/lock', Bool, queue_size=10)
        self.speech = rospy.Publisher('/speech', String, queue_size=10)
        self.mode = rospy.Publisher('/Mode', Int32, queue_size=10)
        self.nav = rospy.Publisher('/navigation_cord', navigation, queue_size=10)
        self.pub_nav = navigation()
        self.pub_nav.name = ''
        self.pub_nav.X = 0
        self.pub_nav.Y = 0
        self.csv_data = 0

        # subscribers
        rospy.Subscriber('/lock', Bool, self.lock_cb)
        rospy.Subscriber('/navigation_goal', appMsg, self.navigation_cb)  # goal from firebase node
        rospy.Subscriber('/stop_signal', Bool, self.local_plan_cb)  # stop signal from local planner
        rospy.Subscriber('/navigation_status', String, self.nav_status_cb)  # navigation status form nav_goal
        rospy.Subscriber('/BatteryCharge', Float32, self.battery_callback)  # battery topic from teensy
        rospy.Subscriber('/pushed', Bool, self.emergency_callback)  # emergency stop switch topic from teensy
        rospy.Subscriber('/face_recognized', String, self.face_detection_cb)  # from face recognition

        # all the variables
        self.state = 0
        self.battery = 0.0  # battery percentage
        self.emergency_stop = True  # emergency stop button status
        self.lock_CO = False  # close or open the lock
        self.navigation = [0, 0, 0, 0]
        self.name = ['', '']
        self.navigation_previous = [0, 0, 0, 0]
        self.name_previous = ['', '']
        self.counter = 0
        self.nav_status = ''
        self.origin = [0.0, 0.0]
        self.error = 0
        self.path_abort = False
        self.face = ""
        self.got_confirmation = False
        self.go = 0
        self.prev_mode = 0
        self.say = ""
        self.lock_stat = False
        self.lock_stat_prev = False
        self.lock_used = False

    def lock_cb(self,msg):
        self.lock_stat = msg.data
        if self.lock_stat:
            self.lock_used = True

        #print(self.lock_stat)

    def face_detection_cb(self, msg):
        self.face = msg.data

    def local_plan_cb(self, msg):
        self.path_abort = msg.data

    def navigation_cb(self, msg):
        self.name[0] = msg.name_pickup
        self.navigation[0] = msg.xt
        self.navigation[1] = msg.yt
        self.name[1] = msg.name_deliver
        self.navigation[2] = msg.xg
        self.navigation[3] = msg.yg

    def nav_status_cb(self, msg):
        self.nav_status = msg.data

    def battery_callback(self, msg):
        self.battery = msg.data

    def emergency_callback(self, msg):
        self.emergency_stop = msg.data

    def print_data(self):
        # print(self.nav_status)
        print(self.state)

    def main_control(self):
        # self.print_data()
        print(self.lock_used)
        if self.lock_stat:
            self.lock_used = True

        # print("lock status is {}".format(self.lock_stat))
        # print("lock_CO is {}".format(self.lock_CO))
        # print("current nav status {} ".format(self.nav_status))
        # if self.battery <= 8.0:
        #     self.error = 1
        # # abort every thing and go to state 4 Home
        #
        # if not self.emergency_stop:
        #     # abort all
        #     pass
        # print("new name {} old name {} ".format(self.name, self.name_previous))
        # print('main_control_loop')

        if self.state == 0:
            # if lock is used say open lock
            # print("lock status is {}".format(self.lock_stat))
            # print("lock_CO is {}".format(self.lock_CO))
            self.got_confirmation = ConfWindow()
            if self.lock_stat:
                self.lock_used = True

            if self.got_confirmation:
                self.say = "Thankyou For Confirmation" + self.face
                self.speech.publish(self.say)
                self.got_confirmation = False
                # self.nav_status = ""
                self.state = 1

        elif self.state == 1:
            print("lock used {}".format(self.lock_used))
            if self.lock_used:
                self.say = "please find your document in Locker"
                self.speech.publish(self.say)

            self.got_confirmation = ConfWindow()
            if self.got_confirmation:
                self.say = "Thankyou For Confirmation" + self.face
                self.speech.publish(self.say)
                self.counter += 1
                # print(self.counter)
                if self.counter > 20:
                    self.state = 2
                    self.counter = 0
                self.say = "Your Document will be delivered soon"
                self.speech.publish(self.say)
                self.got_confirmation = False
                # self.name_previous = self.name
                # print('I am in face got confirmation')
                self.state = 6
        self.publish()

    def publish(self):
        if self.state != self.prev_mode:
            self.prev_mode = self.state
            self.mode.publish(self.state)


        self.nav.publish(self.pub_nav)


if __name__ == '__main__':
    pln = Behavoiur_planner()
    r = rospy.Rate(60)
    while not rospy.is_shutdown():
        pln.main_control()
        r.sleep()
