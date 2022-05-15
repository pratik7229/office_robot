#!/usr/bin/env python
import rospy
from firebase_comm import communicate
from comm_firebase.msg import call_rec_name


class fire_base_com:
    def __init__(self):
        # initialize the node with name speech recognition
        rospy.init_node('communication', anonymous=False)

        # publisher
        self.names = rospy.Publisher('/names_to_work', call_rec_name, queue_size=10)
        self.pub_name = call_rec_name()
        self.pub_name.caller = ""
        self.pub_name.receiver = ""

        # all variables
        self.name = ["", ""]  # stores the name of person of which face is recognized

    def communicater(self):
        name = communicate()
        self.pub_name.receiver = "atharva"
        self.publish_name()
        print(name)

    def publish_name(self):
        self.names.publish(self.pub_name)


if __name__ == '__main__':
    fc = fire_base_com()
    r = rospy.Rate(60)
    while not rospy.is_shutdown():
        fc.communicater()
        r.sleep()
