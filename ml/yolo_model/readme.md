
1.follow the steps to generate ssh key in your github account:-
\
https://support.atlassian.com/bitbucket-cloud/docs/set-up-an-ssh-key/
\
2.clone the repo yolo_darknet via SSH after setting up ssh in your github account:
\
cd catkin_workspace/src
git clone --recursive git@github.com:leggedrobotics/darknet_ros.git
catkin_make -DCMAKE_BUILD_TYPE=Release
\
3.download weights from this folder and add it to the repo at location:
\
catkin_workspace/src/darknet_ros/darknet_ros/yolo_network_config/weights/
\
4.download the file 'yolov3-tiny-obj.cfg' from this folder and add it to the location:
\
catkin_workspace/src/darknet_ros/darknet_ros/yolo_network_config/cfg/
\
5.replace the files yolo_v3.launch and darknet_ros.launch from this folder to :
\
catkin_workspace/src/darknet_ros/darknet_ros/launch/

