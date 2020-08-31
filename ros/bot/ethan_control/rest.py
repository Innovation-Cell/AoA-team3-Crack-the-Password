#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import MultiArrayDimension
import random
import numpy as np
from math import *
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates


def callback(msg):
    # if len(msg.transforms)<2:
    #     print(msg.transforms[0].transform.translation)
    print(msg.pose[1])
    # print(dir(msg.transforms[0]))
   
    # print("yo")

if __name__ =="__main__":
    rospy.init_node("publisher")
    gripper_pub = rospy.Publisher('/platform_state_controller/command', Float64MultiArray, queue_size=1)
    bot_control_pub = rospy.Publisher('/diff_drive_controller/cmd_vel',Twist,queue_size = 2)
    mat = Float64MultiArray()
    mat.layout.dim.append(MultiArrayDimension())
    mat.layout.dim.append(MultiArrayDimension())
    mat.data = [0.0,pi/2,0.001,0.001,0.001]
    i = 0
    while not rospy.is_shutdown():
        i +=1
        gripper_pub.publish(mat)  
        if i > 50000:
            break

print("Now you can work!")


