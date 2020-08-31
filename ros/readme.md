


# For launching the bot with world


Copy  three folders given in bot folder to your ros workspace

Follow the readme in Lane's Apartment folder to Include world model files in your gazebo

Then,

`roslaunch ethan_control controller.launch`

`rosrun ethan_control rest.py`
 **(this command is neccessary for to make gripper in rest position)**

# For navigation of the bot and performing the whole task

**Execute following commands Sequentially in different terminals**

`rosrun ethan_description odom_pub.py`

`rosrun ethan_control go_to_point.py`

`rosrun ethan_control digit_reco_keras.py`

`rosrun ethan_control start_yolo.py`

`rosrun ethan_control genuine_safe_keys.py`

`rosrun ethan_control get_safe_cords.py`

`rosrun ethan_control confirm_safe.py`

`rosrun ethan_control up.py`

`rosrun ethan_control touch.py`

`rosrun ethan_control end.py`

`rosrun ethan_control wall_follow.py`


Above all Scripts wait until they are called to do their function


\
walls: test environment world
\
videos: videos used for testing ml models
\
bot: 'ethan_hunt' custom bot