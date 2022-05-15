#!/usr/bin/env python

import rospy
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

class firebase:
    def __init__(self):
        rospy.init_node('app_data', anonymous=False)
        cred = credentials.Certificate("/home/pratik/office_rbt_ws/src/comm_firebase/scripts/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

        self.url = 'https://carryo-bot-6f391-default-rtdb.firebaseio.com/'

        self.time_eclapsed = 0
        self.prev_time = 0

    def app_data(self):


        currentMillis  = rospy.get_time()
        self.time_eclapsed = abs(currentMillis - self.prev_time)
        print(self.time_eclapsed)
        if self.time_eclapsed > 35:
            self.prev_time = currentMillis
            name = db.reference('faculty_name', url=self.url).get()  # get data
            print(name)


if __name__=='__main__':
    fb = firebase()
    r = rospy.Rate(0.5)
    while not rospy.is_shutdown():
        fb.app_data()
        # print('I am here')
        r.sleep()

