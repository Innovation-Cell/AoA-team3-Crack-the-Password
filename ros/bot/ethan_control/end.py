#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import MultiArrayDimension
import random
import numpy as np
from math import *
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist, Point
from geometry_msgs.msg import Pose
from std_msgs.msg import Bool
import time
rospy.init_node("end_Script")
print("wating")
start = rospy.wait_for_message("/stick", Bool)
print("started")
time.sleep(20)
send_goal = rospy.Publisher("/move_bot/goal", Pose,queue_size=10)
goal = Pose()
goal.position.x = 4.10	
goal.position.y = -5.00155566646    
goal.orientation.w = 1.00
p=pi
#from ethan_control.msg import Angles

angle=[]
file =  open('/home/vishwajeet/catkin_ws/src/ethan_control/demofile3.txt',"r") 
x = []
y = []
z = []
lines = file.readlines()
for line in lines:
	a = line.split()
	x.append(float(a[2]))
	y.append(float(a[0]))
	z.append(float(a[1]))
code = []
file =  open('/home/vishwajeet/catkin_ws/src/ethan_control/code.txt',"r") 
lines = file.readlines()
for line in lines:
    code.append(float(line))

a_1=0.13 #middle arm length
a_2 = 0.09 # end arm length
a=0.60 # Platform Height
b=0.00 #Camera Holder Angle
# code = [1,5,3,0,7]
def get_angles(x,y,z):
	global a_1,a_2
	q2=  acos( -( (a_1**2 + a_2**2) - (x**2 + y**2 + z**2) )/(2*a_1*a_2))
	q1= atan( (z) / (np.sqrt(x**2 + y**2)) ) + atan( (a_2*(sin(q2)) )/(a_1 +  a_2*(cos(q2)) ) )
	c=  p/2 - q1    #Middle Arm Angle
	d=  q2  # End arm angle
	e=  atan(y/x)  # Disk Angle 
	return c,d,e


if __name__ =="__main__":
    # rospy.init_node("publisher")
    gripper_pub = rospy.Publisher('/platform_state_controller/command',    Float64MultiArray, queue_size=1)
    bot_control_pub = rospy.Publisher('/diff_drive_controller/cmd_vel',Twist,queue_size = 2)
    mat = Float64MultiArray()
    mat.layout.dim.append(MultiArrayDimension())
    mat.layout.dim.append(MultiArrayDimension())
    d1 = 0.025
    d2 = 0.028
    val= max(y)
    y[0] = val
    # y[0] = y[0] - 0.007
    y[0] = 0.044
    pos = []
    for c in code:
    	if c ==0:
    		pos.append([0.09,y[0]-d1*2,0.115+z[0]-d2*2])

    	if c ==1:
    		pos.append([0.09,y[0]-d1*0,0.115+z[0]-d2*0])

    	if c ==2:
    		pos.append([0.09,y[0]-d1*1,0.115+z[0]-d2*0])

    	if c ==3:
    		pos.append([0.09,y[0]-d1*2,0.115+z[0]-d2*0])

    	if c ==4:
    		pos.append([0.09,y[0]-d1*3,0.115+z[0]-d2*0])

    	if c ==5:
    		pos.append([0.09,y[0]-d1*0,0.115+z[0]-d2*1])

    	if c ==6:
    		pos.append([0.09,y[0]-d1*1,0.115+z[0]-d2*1])

    	if c ==7:
    		pos.append([0.09,y[0]-d1*2,0.115+z[0]-d2*1])

    	if c ==8:
    		pos.append([0.09,y[0]-d1*3,0.115+z[0]-d2*1])

    	if c ==9:
    		pos.append([0.09,y[0]-d1*1,0.115+z[0]-d2*2])


    g = x[0]
    for digit in pos:
	    # print(dim)
	    print(digit)
	    c,d,e = get_angles(digit[0],digit[1],digit[2])

	    mat.data = [a,b,c,d,e]
	    # print(x[i],y[i],z[i])
	    k = 0
	    while not rospy.is_shutdown():
	    	
	        k +=1
	        gripper_pub.publish(mat)  
	        if k > 50000:
	           break

print("Pressed")

print("Now you can work!")

