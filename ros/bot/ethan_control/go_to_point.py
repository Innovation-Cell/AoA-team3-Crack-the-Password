#! /usr/bin/env python

# import ros stuff
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from tf import transformations
from gazebo_msgs.msg import ModelStates
import math
import numpy as np 
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Pose
from std_msgs.msg import MultiArrayDimension
from std_msgs.msg import Bool
index =0
# robot state variables
position_ = Point()
yaw_ = 0
# machine state
state_ = 0
status = False
# goal
desired_position_ = Point()
desired_position_.x = -5
desired_position_.y = 5
desired_position_.z = 0
# parameters
yaw_precision_ = math.pi / 180 # +/- 1 degree allowed
dist_precision_ = 0.1
kp_angle = 15
kd_angle = 10
ki_angle = 0.0
prev_err_yaw = 0
Sum = 0

kp_dist = 10
kd_dist = 18
ki_dist = 0.1
yaw_required = math.pi/2

# publishers
pub = None
message_arrived = False

# callbacks

def clbk_goal(msg):
    global desired_position_,yaw_required,message_arrived,status
    status = False
    message_arrived = True
    desired_position_.x = msg.position.x
    desired_position_.y = msg.position.y
    quaternion = (
        msg.orientation.x,
        msg.orientation.y,
        msg.orientation.z,
        msg.orientation.w)
    euler = transformations.euler_from_quaternion(quaternion)
    yaw_required = euler[2]
    print("yaw_required", yaw_required)
    change_state(0)

    print(msg)

def clbk_odom(msg):
    global position_
    global yaw_
    
    # position
    position_ = msg.pose.pose.position
    
    # yaw
    quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    euler = transformations.euler_from_quaternion(quaternion)
    yaw_ = euler[2]
    # print(position_)
def change_state(state):
    global state_
    state_ = state
    # print 'State changed to [%s]' % state_

def fix_yaw(des_pos):
    global yaw_, pub, yaw_precision_, state_,prev_err_yaw,Sum
    desired_yaw = math.atan2(des_pos.y - position_.y, des_pos.x - position_.x)

    err_yaw = desired_yaw - yaw_
    Sum +=err_yaw
    twist_msg = Twist()
    # twist_msg.linear.x = 0.05 
    if math.fabs(err_yaw) > yaw_precision_:
        a = -(kp_angle*err_yaw + kd_angle*(err_yaw- prev_err_yaw) )
        twist_msg.angular.z = (a/abs(a))*min(abs(a),0.8)

    pub.publish(twist_msg)
    prev_err_yaw = err_yaw

    # state change conditions
    if math.fabs(err_yaw) <= yaw_precision_:
        # print 'Yaw error: [%s]' % err_yaw
        # print(err_yaw)
        change_state(1)

def orient_yaw(des_yaw):
    global yaw_, pub, yaw_precision_, state_,prev_err_yaw,Sum
    err_yaw = des_yaw - yaw_
    Sum +=err_yaw
    twist_msg = Twist()
    # twist_msg.linear.x = 0.05 
    if math.fabs(err_yaw) > yaw_precision_:
        a = -(kp_angle*err_yaw + kd_angle*(err_yaw- prev_err_yaw) )
        twist_msg.angular.z = (a/abs(a))*min(abs(a),0.5)

    pub.publish(twist_msg)
    # print("yaw")
    prev_err_yaw = err_yaw
    # print(yaw_)
    
    # state change conditions
    if math.fabs(err_yaw) <= yaw_precision_:
        print("dkfjd")
        change_state(3)

def go_straight_ahead(des_pos):
    global yaw_, pub, yaw_precision_, state_
    desired_yaw = math.atan2(des_pos.y - position_.y, des_pos.x - position_.x)
    err_yaw = desired_yaw - yaw_
    err_pos = math.sqrt(pow(des_pos.y - position_.y, 2) + pow(des_pos.x - position_.x, 2))
    # print(position_)
    # print(" pos")    
    if err_pos > dist_precision_:
        twist_msg = Twist()
        twist_msg.linear.x = 0.2
        pub.publish(twist_msg)
    else:
        # print 'Position error: [%s]' % err_pos
        change_state(2)

    if math.fabs(err_yaw) > yaw_precision_:
        # print 'Yaw error: [%s]' % err_yaw
        change_state(0)
    
    # state change conditions


def done():
    twist_msg = Twist()
    twist_msg.linear.x = 0
    twist_msg.angular.z = 0
    pub.publish(twist_msg)

def main():
    global pub
    
    rospy.init_node('go_to_point')
    
    pub = rospy.Publisher('/diff_drive_controller/cmd_vel', Twist, queue_size=1)
    status_pub = rospy.Publisher('/move_bot/status', Bool, queue_size=1)
    sub_odom = rospy.Subscriber('/odom',Odometry, clbk_odom)
    target_sub = rospy.Subscriber('/move_bot/goal',Pose, clbk_goal)
    mat = Float64MultiArray()
    mat.layout.dim.append(MultiArrayDimension())
    mat.layout.dim.append(MultiArrayDimension())
    gripper_pub = rospy.Publisher('/gripper_controller/command', Float64MultiArray, queue_size=1)
    rate =rospy.Rate(200)
    extend = 0
    gripper_extend = 0
    global message_arrived
    while not rospy.is_shutdown():
        if message_arrived:
            if state_ == 0:
                fix_yaw(desired_position_)
            elif state_ == 1:
                go_straight_ahead(desired_position_)
            elif state_ == 2:
                orient_yaw(yaw_required)
            elif state_ ==3:
                done()
                change_state(0)
                message_arrived = False
                status = True
                status_msg = Bool()
                status_msg.data = status
                status_pub.publish(status_msg)
                print("done")
        # rate.sleep()
                   


if __name__ == '__main__':
    main()