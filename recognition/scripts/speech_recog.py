#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Int32
from functions import wishMe

class speech_detection:
	def __init__(self):
		# initialize the node with name speech recognition
		rospy.init_node('speech_detection', anonymous=False)
		
		
		# subscriber
		rospy.Subscriber('/speech', String, self.speech_cb)
		rospy.Subscriber('/Mode', Int32, self.mode_cb)
		# write the subscriber for goal reached or not node


		# Publisher
		

		# all variables
		self.name = ""	 # stores the name of person of which face is recognized
		self.face_found = ""
		self.counter = 0
		self.prev_name = ""
		self.mode = 0
		self.speak_type = ""
		self.speak = ""
	# all callback functions

	def mode_cb(self,msg):
		self.mode = msg.data

	def speech_cb(self, msg):
		self.speak = msg.data

	def speech_out(self):
		# if self.name != "":
		# 	if self.prev_name != self.name:
		# 		self.counter = 0
		# 		if self.counter == 0:
		# 			wishMe(self.name, self.mode)
		# 			self.counter += 1
		# 			self.prev_name = self.name
		# # self.counter = 0
		# if self.counter == 0:
		# 	wishMe(self.name, self.mode)
		# 	self.counter = 1
		# 	self.prev_name = self.name
		print(self.mode)
		if self.speak != "":
			if self.prev_name != self.speak:
				self.counter = 0
				if self.counter == 0:
					wishMe(self.speak, self.mode)
					self.counter += 1
					self.prev_name = self.speak


if __name__=='__main__':
	sr = speech_detection()
	r = rospy.Rate(60)

	while not rospy.is_shutdown():
		sr.speech_out()
		r.sleep()