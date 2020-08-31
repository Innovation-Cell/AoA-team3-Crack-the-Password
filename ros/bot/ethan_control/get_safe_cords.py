#! /usr/bin/env python

# import ros stuff
import rospy
import sys
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
import math
from darknet_ros_msgs.msg import BoundingBoxes
from std_msgs.msg import Header
from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from math import sin,cos,pi
import numpy as np
from geometry_msgs.msg import Pose
from std_msgs.msg import Bool
# data = rospy.wait_for_message("/camera/depth/points",PointCloud2)
# gen = list(point_cloud2.read_points(data, field_names=("x", "y", "z"), skip_nans=False))
rospy.init_node("safe_coordinate")
print("waiting")
start = rospy.wait_for_message("/go_to_safe", Bool)
print("started!!")
safe_pixels = rospy.wait_for_message("/darknet_ros/bounding_boxes", BoundingBoxes)
depth_data = rospy.wait_for_message("/camera/depth/points",PointCloud2)
gen = list(point_cloud2.read_points(depth_data, field_names=("x", "y", "z"), skip_nans=False))
bot_pose = rospy.wait_for_message("/odom",Odometry)
send_goal = rospy.Publisher("/move_bot/goal", Pose,queue_size=1)
send_normalize = rospy.Publisher("/normal", Bool,queue_size=1)
goal = Pose()
	# print(safe_pixels.bounding_boxes[0])
	# print(bot_pose)
xmin = safe_pixels.bounding_boxes[0].xmin
ymin = safe_pixels.bounding_boxes[0].ymin
xmax = safe_pixels.bounding_boxes[0].xmax
ymax = safe_pixels.bounding_boxes[0].ymax

a = gen[ymin*1920+xmin-1]
b = gen[ymin*1920+xmax-1]
c = gen[ymax*1920+xmax-1]
d = gen[ymax*1920+xmin-1]
e = gen[(ymax+ymin)/2*1920+(xmin+xmax)/2-1]
quaternion = (
	bot_pose.pose.pose.orientation.x,
	bot_pose.pose.pose.orientation.y,
	bot_pose.pose.pose.orientation.z,
	bot_pose.pose.pose.orientation.w)
euler = transformations.euler_from_quaternion(quaternion)
# p = np.matrix([0,0,0])

x = (e[0])
y = (e[2])
z = (e[1])
angle = euler[2]
matrix = np.matrix([[cos(angle),-sin(angle),0],[sin(angle),cos(angle),0],[0,0,1]])
point  = np.matrix([x+0.2,y+0.0125,-z]).transpose()
f = np.dot(matrix,point)
pose_x = f[0,0]+bot_pose.pose.pose.position.x
pose_y = f[1,0]+bot_pose.pose.pose.position.y
pose_z = f[2,0]+bot_pose.pose.pose.position.z


# print(pose_x,pose_y)
goal.position.x = pose_x- 0.41  #0.41 safe distance from wall 
goal.position.y = pose_y

print(transformations.quaternion_from_euler(0,0,0))
print(goal)
i = 0
while i <10000:
	i +=1
	send_goal.publish(goal)
	send_normalize.publish(True)

# print()
