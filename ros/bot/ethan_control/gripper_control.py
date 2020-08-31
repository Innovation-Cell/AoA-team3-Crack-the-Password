#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import MultiArrayDimension
import random
import numpy as np
from math import *
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates
p=pi
#from ethan_control.msg import Angles

angle=[]
with open('/home/vishwajeet/catkin_ws/src/ethan_control/Angles.txt',"r") as f:
     for coord in f:
         m=coord.split()
         for i in range(len(m)):
                angle.append(float(m[i]))


a_1=0.13 #middle arm length
a_2 = 0.09 # end arm length
a=0 # Platform Height
b=1.5 #Camera Holder Angle

r=len(angle)//3
for i in range(r):
    x=angle[3*i]
    y=angle[3*i+1] 
    z=angle[3*i+2]

    q2=  acos( ( (a_1**2 + a_2**2) - (x**2 + y**2 + z**2) )/(2*a_1*a_2))
    q1= atan( (z) / (np.sqrt(x**2 + y**2)) ) + atan( (a_2*(sin(q2)) )/(a_1 +  a_2*(cos(q2)) ) )
    c=  p/2 - q1    #Middle Arm Angle
    d=  q2  # End arm angle 
    #print('q1=',q1,'q2=',q2,'c=',c,'d=',d)
    e=  atan(y/x)  # Disk Angle


    def callback(msg):
        print(msg.pose[1])


    if __name__ =="__main__":
        rospy.init_node("publisher")
        gripper_pub = rospy.Publisher('/platform_state_controller/command',    Float64MultiArray, queue_size=1)
        bot_control_pub = rospy.Publisher('/diff_drive_controller/cmd_vel',Twist,queue_size = 2)
        mat = Float64MultiArray()
        mat.layout.dim.append(MultiArrayDimension())
        mat.layout.dim.append(MultiArrayDimension())
        mat.data = [a,b,c,d,e]
        i = 0
        while not rospy.is_shutdown():
            i +=1
            gripper_pub.publish(mat)  
            if i > 10000:
               break
    print("Pressed")
    rospy.sleep(2)

print("Now you can work!")

