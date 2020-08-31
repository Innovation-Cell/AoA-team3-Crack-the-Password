#! /usr/bin/env python
 
# import ros stuff
import rospy
import sys
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Point
from std_msgs.msg import Bool
a = 3
b = 3
c = 3
def clbk_laser(msg):
    global a,b,c
    a = msg.ranges[300]
    b = msg.ranges[359]
    c = msg.ranges[418]
    # print(b)

rospy.init_node("test")
print("waiting")
vel_pub = rospy.Publisher('/diff_drive_controller/cmd_vel', Twist, queue_size=1)
vel = Twist()
sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
start = rospy.wait_for_message("/stick", Bool)
print("started")

while not rospy.is_shutdown():
    vel.linear.x = 0.05
    vel.angular.z = (c-a)*20
    vel_pub.publish(vel)
vel.linear.x = 0
vel.angular.z = 0
vel_pub.publish(vel)
print("done")

rospy.spin()