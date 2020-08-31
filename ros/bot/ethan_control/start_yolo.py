#! /usr/bin/env python

import roslaunch
import rospy
from std_msgs.msg import Bool
rospy.init_node('en_Mapping', anonymous=True)
uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)
launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/vishwajeet/catkin_ws/src/darknet_ros/darknet_ros/launch/yolo_v3.launch"])
print("waiting")
# start = rospy.wait_for_message("/start_yolo", Bool)
print("started!!")
launch.start()
rospy.loginfo("started")
end = rospy.wait_for_message("/normal", Bool)
launch.shutdown()
