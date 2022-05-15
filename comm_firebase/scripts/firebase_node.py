#!/usr/bin/env python

import rospy
from user_interface.msg import appMsg
import csv
from firebase_comm import communicate, send_mode
from std_msgs.msg import Int32
# this script receives caller name and receiver name from app and then it matches it with the
# name in the csv file and gets the x,y location of receiver and caller and send it to
# the behaviour planner

class firebase:
    def __init__(self):
        rospy.init_node('app_data', anonymous=False)

        self.goal = rospy.Publisher('/navigation_goal', appMsg, queue_size=10)
        rospy.Subscriber('/Mode', Int32, self.mode_callback)
        self.pub_nav = appMsg()
        self.pub_nav.name_pickup = ''
        self.pub_nav.xt = 0
        self.pub_nav.yt = 0
        self.pub_nav.name_deliver = ''
        self.pub_nav.xg = 0
        self.pub_nav.yg = 0
        self.mode = 0  # in which mode the robot is in
        self.previous_mode = 0
        self.names = ["", ""]  # this will be names coming from the Google firebase
        self.prev_names = ['', '']
        self.nav_goal = self.read_csv_file()

    def read_csv_file(self):
        file = open('/home/pratik/office_rbt_ws/src/comm_firebase/scripts/location.csv')
        file_data = csv.reader(file)
        rows = []
        for row in file_data:
            a = row[0].replace(" ", "")
            row[0] = a
            rows.append(row)
        return rows

    def mode_callback(self, msg):
        self.mode = msg.data

    def match_data(self, goal):
        goal_convert = []
        #print(self.nav_goal)
        try:
            for i in range(len(self.nav_goal)):

                for j in range(len(goal)):
                    a = self.nav_goal[i][0].capitalize()
                    b = goal[j].capitalize()
                    print(self.nav_goal[i][0], goal[j])
                    # print(a,b)
                    if a == b:
                        goal_convert.append(self.nav_goal[i])
                    # if self.nav_goal[i][0] == goal[j]:
                    #     goal_convert.append(self.nav_goal[i])
            return goal_convert
        except:
            print('no match found')
            return goal_convert

    def convert(self, goal):
        if goal:
            goal[0] = goal[0].replace(" ", "")
            goal[1] = goal[1].replace(" ", "")
            return goal
        else:
            return goal

    def app_data(self):
        # print(self.nav_goal)
        self.names = communicate()
        # print(self.names)
        goal = self.convert(self.names)
        # print(goal)
        if self.names:
            # commented part is for getting new data only once from fire base node
            goal = self.match_data(goal)

            # self.convert(goal)
            print(goal)
            self.publish(goal)
            self.prev_names = self.names
            # self.counter += 1
            # print(self.counter)
            # print('previous names = {}'.format(self.prev_names))

        if self.mode != self.previous_mode:
            # print("current mode is {} and prev mode is {} ".format(self.mode, self.previous_mode))
            # sends mode only when it is changed
            send_mode(self.mode)
            self.previous_mode = self.mode


    def publish(self, give_take):
        self.pub_nav.name_pickup = str(give_take[0][0])
        self.pub_nav.xt = float(give_take[0][1])
        self.pub_nav.yt = float(give_take[0][2])
        self.pub_nav.name_deliver = str(give_take[1][0])
        self.pub_nav.xg = float(give_take[1][1])
        self.pub_nav.yg = float(give_take[1][2])
        self.goal.publish(self.pub_nav)


if __name__ == '__main__':
    fb = firebase()
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        fb.app_data()
        # print('I am here')
        r.sleep()
