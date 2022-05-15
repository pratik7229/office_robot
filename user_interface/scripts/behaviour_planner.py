#!/usr/bin/env python

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
        self.lock_used = False

    def lock_cb(self,msg):
        self.lock_stat = msg.data
        if self.lock_stat:
            self.lock_used = True

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
        print("lock status is {}".format(self.lock_stat))
        print("lock_CO is {}".format(self.lock_CO))
        print("lock_used is {}".format(self.lock_used))

    def main_control(self):
        self.print_data()
        if self.lock_stat:
            self.lock_used = True
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

            if self.name[0] != self.name_previous[0] or self.name[1] != self.name_previous[1]:
                # print('got new task')
                self.pub_nav.name = self.name[0]
                self.pub_nav.X = self.navigation[0]
                self.pub_nav.Y = self.navigation[1]
                # self.name_previous = self.name       # this line has an logical issue
                # print(self.name[0], self.navigation[0], self.navigation[1])
                # counter is only for checking
                # print(self.counter)
                # self.counter += 1
                # if self.counter > 3000:
                #     self.state = 1
                #     # print('I am above name previous')
                #     # self.name_previous = self.name
                #     self.counter = 0
                if self.nav_status == 'status3':
                    self.nav_status = ""
                    self.state = 1
            else:
                print(" no new entry got")
                # print('waiting for task')

        elif self.state == 1:
            # scan the face if detected person is person of pickup
            # greet the person by
            # "hi professor how may I help you"
            # take the document and confirm received
            # change state to state 2
            if self.face.lower() == self.name[0].lower():
                self.say = self.face + "How may I help you"
                self.speech.publish(self.say)
                # greet the person and ask him the document
                # connect to UI

                # this counter is for buffer for speech recognition script
                self.counter += 1
                # print(self.counter)
                if self.counter > 20:
                    self.state = 2
                    self.counter = 0

        elif self.state == 2:
            # if lock is used say open lock
            self.got_confirmation = ConfWindow()
            if self.lock_stat:
                self.say = "opening Lock"
                self.speech.publish(self.say)
                self.lock_used = True

            if self.got_confirmation:
                self.say = "Thankyou For Confirmation" + self.face
                self.speech.publish(self.say)
                self.got_confirmation = False
                # self.nav_status = ""
                self.state = 3
        elif self.state == 3:
            self.pub_nav.name = self.name[1]
            self.pub_nav.X = self.navigation[2]
            self.pub_nav.Y = self.navigation[3]
            # print(self.name[1], self.navigation[2], self.navigation[3])

            # counter is only for checking
            # self.counter += 1
            # print(self.counter)
            # if self.counter > 5000:
            #     self.state = 4
            #     self.counter = 0
            if self.nav_status == 'status3':
                self.nav_status = ""
                self.state = 4
            # if self.nav_status == 'Goal execution done!':
            #     self.state = 4
        elif self.state == 4:
            # scan the face if detected person is person of delivery
            # greet the person by
            # "hi professor I have a document for you"
            # give the document and if the confirmation received
            # change state to state 4
            # print("name got : {}, name want {}".format(self.face, self.name[1]))
            if self.face.lower() == self.name[1].lower():
                self.say = self.face + "I have a document for you"
                self.speech.publish(self.say)
                rospy.sleep(5)
                # greet the person and ask him the document
                if self.lock_used:
                    self.say = "please find your document in Locker"
                    self.speech.publish(self.say)
                # connect to UI
                self.state = 5
                # print('I am in face scan')

        elif self.state == 5:
            print("i am in state 5")

            # rospy.sleep(5)
            self.got_confirmation = ConfWindow()
            if self.got_confirmation:
                self.say = "Thankyou For Confirmation" + self.face
                self.speech.publish(self.say)
                self.counter += 1
                # print(self.counter)
                if self.counter > 20:
                    self.state = 2
                    self.counter = 0
                self.say = "Thankyou for Comfirmation"
                self.speech.publish(self.say)
                self.got_confirmation = False
                self.lock_used = False
                # self.name_previous = self.name
                # print('I am in face got confirmation')
                self.state = 6
        elif self.state == 6:
            # go home
            self.pub_nav.X = 2  # self.origin[0] + 0.1
            self.pub_nav.Y = 0  # self.origin[1] + 0.1
            # print('returning to home', self.origin)
            self.counter += 1
            if self.nav_status == 'status3':
                self.nav_status = ""
                self.state = 7    # stop and go to stay at home location
            # print(self.counter)
            # if self.counter > 500:
            #     self.state = 0
            #     self.counter = 0
            #     # print('I am in state 4 if counter is {}'.format(self.counter))

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
