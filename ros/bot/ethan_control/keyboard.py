#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from pynput.keyboard import Key, Listener
rospy.init_node("keyboard_control")
pub = rospy.Publisher("/diff_drive_controller/cmd_vel",Twist)
control = Twist()
def on_press(key):
    # print(key)
    if(key == Key.left):
        control.angular.z = -1
        pub.publish(control)
    if(key == Key.right):
        control.angular.z =1
        pub.publish(control)
    if(key == Key.down):
        control.linear.x = -1
        pub.publish(control)
    if(key == Key.up):
        control.linear.x = 1
        pub.publish(control)

def on_release(key):
    if(key == Key.left):
        control.angular.z = 0
        pub.publish(control)
    if(key == Key.right):
        control.angular.z = 0
        pub.publish(control)
    if(key == Key.down):
        control.linear.x = 0
        pub.publish(control)
    if(key == Key.up):
        control.linear.x = 0
        pub.publish(control)
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()