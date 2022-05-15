#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Int32
from face_detection import *
from user_interface.msg import navigation

class face_recognition:
	def __init__(self):
		# initialize the node with name speech recognition
		rospy.init_node('face_recognition', anonymous=False)


		# subscriber
		# write the subscriber for goal reached or not node
		rospy.Subscriber('/navigation_cord', navigation, self.navigation_cb)   # from beharviour planner only name
		rospy.Subscriber('/Mode', Int32, self.mode_cb)
		# Publisher
		self.face_found = rospy.Publisher("/face_recognized", String, queue_size=10)


		# all variables
		self.name = ""	 # stores the name of person of which face is recognized
		self.mode = 0

	def mode_cb(self,msg):
		self.mode = msg.data

	def navigation_cb(self, msg):
		self.name = msg.name

	def face_recognizer(self):

		name = ''
		if self.mode == 1 or self.mode == 4:
			name = fd.face_detect()
		else:
			print('mode {} '.format(self.mode))
		print("name got : {}, name want {}".format(self.name, name))
		if self.name == name:
			self.publish_name(name)
		else:
			print('searching person')
		print(name)
		if name:
			self.publish_name(name)


	def publish_name(self, name):
		self.face_found.publish(name)



if __name__=='__main__':
	sr = face_recognition()
	fd = face_rec()
	r = rospy.Rate(60)

	while not rospy.is_shutdown():
		sr.face_recognizer()
		r.sleep()