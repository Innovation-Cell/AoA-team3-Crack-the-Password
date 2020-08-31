#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import MultiArrayDimension
import numpy as np
from math import *
from sympy import *
from geometry_msgs.msg import Twist

dist=0.3
Co_or=[]
with open('PlaneCoord.txt',"r") as f:
     for coord in f:
         m=coord.split()
         for i in range(len(m)):
                Co_or.append(float(m[i]))
r=len(Co_or)//3
x=[]
y=[]
z=[]
for i in range(r):
    x.append(Co_or[3*i])
    y.append(Co_or[3*i+1]) 
    z.append(Co_or[3*i+2])
p1,p2,p3=Point3D(x[0],y[0],z[0]),Point3D(x[1],y[1],z[1]),Point3D(x[2],y[2],z[2])
a=Plane(p1,p2,p3)
n=a.normal_vector
m= p1.midpoint(p3)
k= dist/sqrt(m.x**2+m.y**2+m.z**2)
Robot_P=Point3D(m.x+n.x*k,m.y+k*n.y,m.z+k*n.z)
print(Robot_P)





