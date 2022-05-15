#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32, Float32, Bool
from sensor_msgs.msg import Range
from user_interface.srv import sensorCheck, sensorCheckResponse
class sensor_data:
    def __init__(self):

        # all the subscribers and publishers here
        # Subscribers
        rospy.init_node('sensor_data', anonymous=False)                     # node name as sensor data
        self.srv = rospy.Service('/sensor_status_check', sensorCheck, self.sensor_cb)
        rospy.Subscriber('/BatteryCharge', Float32, self.battery_callback)  # battery topic
        rospy.Subscriber('/pushed', Bool, self.emergency_callback)  # emsrgency stop switch topic
        rospy.Subscriber('/IR_front_left', Bool, self.ir1_callback)  # ir sensor front
        rospy.Subscriber('/IR_front_right', Bool, self.ir2_callback)  # ir sensor back
        rospy.Subscriber('/ultrasound_back', Range, self.ultrasonic1_cb)  # ultrasonic sensor front
        rospy.Subscriber('/ultrasound_front', Range, self.ultrasonic2_cb)  # ultrasonic sensor back

        # publishers
        self.lock = rospy.Publisher('/lock', Bool, queue_size=10)

        # all the variables 
        self.battery = 0.0                                                    # battery percentage
        self.emergency_stop = True                                             # emergency stop button status
        self.ultrasonic = [0.0, 0.0]                                        # [Front, back] distance values
        self.ir_sensor = [False, False]                                     # [Front, back] boolean values
        self.lock_CO = False                                                # close or open the lock
        

    # all the call back functions  
    def battery_callback(self, msg):
        self.battery = msg.data
    
    def emergency_callback(self, msg):
        self.emergency_stop = msg.data
    
    def ir1_callback(self, msg):
        self.ir_sensor[0] = msg.data
    
    def ir2_callback(self, msg):
        self.ir_sensor[1] = msg.data
    
    def ultrasonic1_cb(self, msg):
        self.ultrasonic[0] = msg.range
    
    def ultrasonic2_cb(self, msg):
        self.ultrasonic[1] = msg.range
    
    def subscribe_topics(self):
        rospy.Subscriber('/BatteryCharge', Float32, self.battery_callback)          # battery topic
        rospy.Subscriber('/pushed', Bool, self.emergency_callback)      # emsrgency stop switch topic
        rospy.Subscriber('/IR_front_left', Bool, self.ir1_callback)                  # ir sensor front   
        rospy.Subscriber('/IR_front_right', Bool, self.ir2_callback)                  # ir sensor back
        rospy.Subscriber('/ultrasound_back', Range,self.ultrasonic1_cb)         # ultrasonic sensor front
        rospy.Subscriber('/ultrasound_front', Range,self.ultrasonic2_cb)         # ultrasonic sensor back
        print('inside subscribe topic')
    def check_sensors(self):
        if self.battery <= 8.0 or self.ir_sensor[0] == True or self.ir_sensor[1] == True or self.ultrasonic[0] <= 50.0 or self.ultrasonic[1] <= 50.0 or self.emergency_stop == False:
            status = "ok"
        else:
            status = "not ok"
        return status


    def sensor_cb(self, request):
        self.subscribe_topics()
        status = self.check_sensors()
        print("got {} from client".format(request.check))
        print("responding with {}" .format(status))
        
        if request.check == "Check_sensors":
            resp = sensorCheckResponse()
            resp.sensor_status = status
        return resp

    # publish the data from this function
    def publish_data(self):
        self.lock.publish(self.lock_CO)



if __name__=='__main__':
    mw = sensor_data()
    r = rospy.Rate(60)
    while not rospy.is_shutdown():
        r.sleep()