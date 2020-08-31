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
from std_msgs.msg import Bool


pub_ = None
regions_ = {
    'right': 0,
    'fright': 0,
    'front': 0,
    'fleft': 0,
    'left': 0,
}
state_ = 0
state_dict_ = {
    0: 'find the wall',
    1: 'turn left',
    2: 'follow the wall',
}
def clbk_laser(msg):
    global regions_
    regions_ = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[10:240]), 10),
        'front':  min(min(msg.ranges[241:480]), 10),
        'fleft':  min(min(msg.ranges[481:710]), 10),
        'left':   min(min(msg.ranges[700:720]), 10),
    }
    # print(regions_)

    take_action()


def change_state(state):
    global state_, state_dict_
    if state is not state_:
        # print 'Wall follower - [%s] - %s' % (state, state_dict_[state])
        state_ = state


def take_action():
    global regions_
    regions = regions_
    msg = Twist()
    linear_x = 0
    angular_z = 0
    
    state_description = ''
    
    d = 0.6
    
    if regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:
        state_description = 'case 1 - nothing'
        change_state(0)
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] > d:
        state_description = 'case 2 - front'
        change_state(1)
    elif regions['front'] > d and regions['fleft'] > d and regions['fright'] < d:
        state_description = 'case 3 - fright'
        change_state(2)
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] > d:
        state_description = 'case 4 - fleft'
        change_state(0)
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] < d:
        state_description = 'case 5 - front and fright'
        change_state(1)
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] > d:
        state_description = 'case 6 - front and fleft'
        change_state(1)
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d:
        state_description = 'case 7 - front and fleft and fright'
        change_state(1)
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d:
        state_description = 'case 8 - fleft and fright'
        change_state(0)
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

def find_wall():
    msg = Twist()
    msg.linear.x = 0.04
    msg.angular.z = 0.4
    return msg

def turn_left():
    msg = Twist()
    msg.angular.z = -0.4
    return msg

def follow_the_wall():
    global regions_
    
    msg = Twist()
    msg.linear.x = 0.5
    return msg
a=" "
finish=False
def callback(data):
    # print(data)
    global finish
    finish = True

def main():
    global pub_,finish
    
    rospy.init_node('reading_laser')
    
    pub_ = rospy.Publisher('/diff_drive_controller/cmd_vel', Twist, queue_size=1)
    
    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    
    rate = rospy.Rate(10)
    print("yo")
    rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes , callback) 
    check_safe = rospy.Publisher("/check_safe",Bool)       
    while not rospy.is_shutdown():
        msg = Twist()
        if state_ == 0:
            msg = find_wall()
        elif state_ == 1:
            msg = turn_left()
        elif state_ == 2:
            msg = follow_the_wall()
            pass
        else:
            rospy.logerr('Unknown state!')
        #terminating when we detect safe
        # rospy.init_node('bbmsg', anonymous=True)
        pub_.publish(msg)
        if finish:
            check_safe.publish(True)
            is_safe = rospy.wait_for_message("/confirm_safe", Bool)
            is_safe =  str(is_safe)
            if "False" in is_safe:
                finish = False
            else:
                break

        rate.sleep()
    send_to_safe = rospy.Publisher("/go_to_safe", Bool,queue_size=1)
    i = 0
    while i <10000:
        i +=1
        send_to_safe.publish(True)

main()