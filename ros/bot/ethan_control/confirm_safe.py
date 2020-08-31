#! /usr/bin/env python
 
# import ros stuff
import rospy
import sys
from darknet_ros_msgs.msg import BoundingBoxes
from std_msgs.msg import Bool
safe_pixels = False
from time import sleep
rospy.init_node("check_safe")
def clbk(msg):
	global safe_pixels
	safe_pixels = True
safe = rospy.Subscriber("/darknet_ros/bounding_boxes", BoundingBoxes, clbk)
push = rospy.Publisher("/confirm_safe", Bool)
while not rospy.is_shutdown():
	print("waiting")
	rospy.wait_for_message("/check_safe",Bool)
	print("started")
	sleep(5)
	safe_pixels = False
	i = 0
	while i < 50000:
		i +=1
		print(i)
	push.publish(safe_pixels)
	safe_pixels = False


