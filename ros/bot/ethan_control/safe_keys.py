#!/usr/bin/env python

import numpy as np
import time
import cv2
import os

# from sklearn.externals import joblib

# import tensorflow.keras as keras

#function for asserting color configuratoin
from sensor_msgs.msg import Image
import rospy
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Bool
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
rospy.init_node('realtime_test', anonymous=True)
print("waiting")
start = rospy.wait_for_message("/move_bot/status", Bool)
print("started!!")
finish = False
boxes = None
sequence = []
result = None

"""
def assert_color(img):
    ar=np.array(img,dtype='int')
    cnt=0
    for i in range(ar.shape[0]):
        for j in range(ar.shape[1]):
            if ar[i,j]==255:
                cnt=cnt+1
                if cnt>(ar.shape[0]*ar.shape[1]/100):
                    return 1
                else:
                    continue
    return 0
"""


def image_callback(img_msg):
	

	
	#read the converted input image
	try:
		im=bridge.imgmsg_to_cv2(img_msg,"bgr8")
	except CvBridgeError,e:
		
		rospy.logerr("CvBridgeError: {0}".format(e))
	x_list=[]
	y_list=[]



	# Convert to grayscale and apply Gaussian filtering
	im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)
	ret, im_th = cv2.threshold(im_gray, 30, 255, cv2.THRESH_BINARY_INV)
	# Threshold the image
	th3 = cv2.adaptiveThreshold(im_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
		    cv2.THRESH_BINARY_INV,11,2)

	    
	_,ctrs,_ = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	    
	rects=list()
	for ctr in ctrs:
		area = cv2.contourArea(ctr)
		if area>3000 and area<8000:
		    rect=cv2.boundingRect(ctr)
		    if rect[2]/rect[3]<2 and rect[3]/rect[2]<2:
		        rects.append(rect)
		        print(rect[0], ' ' ,rect[1])

			if len(x_list)<=12:

		        	x_list.append(rect[0])
		        	y_list.append(rect[1])
		# Draw the rectangles
	   

	x_list.sort()
	y_list.sort()
	def get_key(rect):
		if rect[0] in range(x_list[0]-15,x_list[0]+15):
		    if rect[1] in range(y_list[0]-15,y_list[0]+15):
		        return '1'
		    elif rect[1] in range(y_list[4]-15,y_list[4]+15):
		        return '5'
		    elif rect[1] in range(y_list[8]-15,y_list[8]+15):
		        return ''
		if rect[0] in range(x_list[3]-15,x_list[3]+15):
		    if rect[1] in range(y_list[0]-15,y_list[0]+15):
		        return '2'
		    elif rect[1] in range(y_list[4]-15,y_list[4]+15):
		        return '6'
		    elif rect[1] in range(y_list[8]-15,y_list[8]+15):
		        return '9'
		if rect[0] in range(x_list[6]-15,x_list[6]+15):
		    if rect[1] in range(y_list[0]-15,y_list[0]+15):
		        return '3'
		    elif rect[1] in range(y_list[4]-15,y_list[4]+15):
		        return '7'
		    elif rect[1] in range(y_list[8]-15,y_list[8]+15):
		        return '0'
		if rect[0] in range(x_list[9]-15,x_list[9]+15):
		    if rect[1] in range(y_list[0]-15,y_list[0]+15):
		        return '4'
		    elif rect[1] in range(y_list[4]-15,y_list[4]+15):
		        return '8'
		    elif rect[1] in range(y_list[8]-15,y_list[8]+15):
		        return ''

	global sequence
	sequence =[]     
	b = ["1","2","3","4","5","6","7","8","","9",""]  
	i= 0
	for rect in rects:
		# Draw the rectangles
		if len(rects)==12:
			i +=1
			cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3) 
			global boxes
			boxes = rects
		"""print(rect[0], ' ' ,rect[1])
		imCrop = im[int(rect[1]):int(rect[1]+rect[3]), int(rect[0]):int(rect[0]+rect[2])]
	 
	   
		# Make the rectangular region around the digit
		leng = int(rect[3] * 1.6)
		pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
		pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
		roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
		# Resize the image
		try:
		   
		    roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
		    roi = cv2.dilate(roi, (3, 3))
		    
		except:
		    continue
		# Calculate the HOG features
		roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualize=False)
		nbr = clf.predict(np.array([roi_hog_fd], 'float64'))"""
		if(len(rects)==12):
			a = get_key(rect)
			sequence.append(a)
		    
			cv2.putText(im,b[i], (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)

	# cv2.imshow('img',im)
	# cv2.waitKey(3)	
	if len(rects)==12:
		global finish,result
		print("finish")
		result = im

		finish = True
    #show  the frame with detection
		
if __name__ == '__main__':
	try:
		# Load the classifier
		# clf=joblib.load("cls.pkl")
		#initialise the ros node
		
		# Initalize a subscriber to the "/camera/rgb/image_raw" topic with the function "image_callback" as a callback
		sub_image = rospy.Subscriber("/camera/rgb/image_raw", Image, image_callback)
		# Initialize the CvBridge class
		bridge=CvBridge()
		while not rospy.is_shutdown():
			# print("yo")
			if finish:
				break

		depth_data = rospy.wait_for_message("/camera/depth/points",PointCloud2)
		gen = list(point_cloud2.read_points(depth_data, field_names=("x", "y", "z"), skip_nans=False))
		# print(depth_data)
		sub_image.unregister()
		print(boxes)
		print(sequence)
		keys = []
		for box in boxes:
			print(box)
			a = gen[1920*(box[1]) + (box[0]) -1]
			keys.append(str(a[0])+" "+str(a[1])+" "+str(a[2]) +"\n")
		f = open("/home/vishwajeet/catkin_ws/src/ethan_control/demofile3.txt", "w")

		f.writelines(keys)
		f.close()
		print("text file written!")
		i = 0
		final = rospy.Publisher("/stick",Bool)

		while i <1000 :
			i +=1
			cv2.imshow('img',result)
			# cv2.waitKey(3)
			final.publish(True)
	except rospy.ROSInterruptException:
		rospy.loginfo("node terminated")
