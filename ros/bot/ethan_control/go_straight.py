#! /usr/bin/env python

# import ros stuff
import rospy
from geometry_msgs.msg import Twist, Point
from std_msgs.msg import Bool
rospy.init_node("go_ahead")
vel_pub = rospy.Publisher('/diff_drive_controller/cmd_vel', Twist, queue_size=1)
start_reco = rospy.Publisher("/start_reco",Bool)
vel = Twist()
print("waiting")
start = rospy.wait_for_message("/move_bot/status", Bool)
print("started!!")
finish = False
def clbk(msg):
	global finish
	finish = True

stop_bot = rospy.Subscriber("/stop_bot",Bool,clbk)
rate = rospy.Rate(25)
vel.linear.x = 0.1
while not rospy.is_shutdown():
	vel_pub.publish(vel)
	if finish:
		vel.linear.x = 0
		vel_pub.publish(vel)
		break
	rate.sleep()
i  = 0
while i < 20000:
	start_reco.publish(True)


