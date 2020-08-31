#!/usr/bin/env python


import time
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
import os

# from sklearn.externals import joblib

# import tensorflow.keras as keras

#function for asserting color configuratoin
from sensor_msgs.msg import Image
import rospy
from cv_bridge import CvBridge, CvBridgeError
from tensorflow.keras.models import load_model
import numpy as np
import tensorflow as tf
import cv2
#from PIL import Image, ImageOps

from skimage import transform
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
image_height = 28
image_width = 28
num_channels = 1
num_classes = 10

r={'0':[0,0,0,0],'1':[0,0,0,0],'2':[0,0,0,0],'3':[0,0,0,0],'4':[0,0,0,0],'5':[0,0,0,0],'6':[0,0,0,0],'7':[0,0,0,0],'8':[0,0,0,0],'9':[0,0,0,0]}
yxz={0:[0,0,0],1:[0,0,0],2:[0,0,0],3:[0,0,0],4:[0,0,0],5:[0,0,0],6:[0,0,0],7:[0,0,0],8:[0,0,0],9:[0,0,0]}

def get_centres(rect):
	a=[]
	a.append(rect[0]+rect[2]/2)
	a.append(rect[1]+rect[3]/2)
	return a


def callback_pointcloud(data):
    global r
    global xyz
    assert isinstance(data, PointCloud2)
    gen = list(point_cloud2.read_points(data, field_names=("x", "y", "z"), skip_nans=False))
    for i in range(10):
    	I=str(i)
    	uv=get_centres(r[I])
    	po=(uv[0]*640+uv[1])-1
    	xyz[i]=[gen[po][0],gen[po][1],gen[po][2]]
    	#xyz coordinates being stored corresponding to the numbers
    time.sleep(1)


def build_model():
    model = Sequential()
    # add Convolutional layers
    model.add(Conv2D(filters=32, kernel_size=(3,3), activation='relu', padding='same',
                     input_shape=(image_height, image_width, num_channels)))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2,2)))    
    model.add(Flatten())
    # Densely connected layers
    model.add(Dense(128, activation='relu'))
    # output layer
    model.add(Dense(num_classes, activation='softmax'))
    # compile with adam optimizer & categorical_crossentropy loss function
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

model = build_model()
model.load_weights('test.h5')
#model = load_model('my_model.h5')

def load(im):

   nk=np.zeros((1,28,28,1),dtype='float')
   np_image = np.array(im).astype('float32')/255
   nk[0,:,:,0]=np_image
#np_image = transform.resize(np_image, (28, 28, 1))
   #np_image = np.expand_dims(np_image, axis=0)
   return nk
def predictor(model_name,img):
  global model
  image = load(img)
  res=model.predict(image)
  i=np.argmax(res, axis=1)
  prob=res[0,i]
  return i,prob
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
		if area>3000 and area<10000:
		    rect=cv2.boundingRect(ctr)
		    if rect[2]/rect[3]<2 and rect[3]/rect[2]<2:
		        rects.append(rect)
		        #print(rect[0], ' ' ,rect[1])

			if len(x_list)<12 and len(y_list)<12:

		        	x_list.append(rect[0])
		        	y_list.append(rect[1])
		# Draw the rectangles
	   

	x_list.sort()
	y_list.sort()
	def get_key(rect):
		leng = int(rect[3] * 0.7)
		pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
		pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
		imCrop = im_th[pt1:pt1+leng, pt2:pt2+leng]


		ret, imCrop = cv2.threshold(imCrop, 30, 255, cv2.THRESH_BINARY_INV)
		imCrop = cv2.resize(imCrop, (28, 28), interpolation=cv2.INTER_AREA)
		imCrop = cv2.dilate(imCrop, (3, 3))
		if rect[0] in range(x_list[0]-15,x_list[0]+15):
			if rect[1] in range(y_list[0]-15,y_list[0]+15):
				cls,prob=predictor('my_model.h5',imCrop)
			
				return cls,imCrop
			elif rect[1] in range(y_list[4]-15,y_list[4]+15):
				cls,prob=predictor('my_model.h5',imCrop)
			
				return cls,imCrop
			elif rect[1] in range(y_list[8]-15,y_list[8]+15):
			
				return '',imCrop
		if rect[0] in range(x_list[3]-15,x_list[3]+15):
			if rect[1] in range(y_list[0]-15,y_list[0]+15):
				cls,prob=predictor('my_model.h5',imCrop)
			
				return cls,imCrop
			elif rect[1] in range(y_list[4]-15,y_list[4]+15):
				cls,prob=predictor('my_model.h5',imCrop)
			
				return cls,imCrop
			elif rect[1] in range(y_list[8]-15,y_list[8]+15):
				cls,prob=predictor('my_model.h5',imCrop)
				return cls,imCrop
		if rect[0] in range(x_list[6]-15,x_list[6]+15):
			if rect[1] in range(y_list[0]-15,y_list[0]+15):
				cls,prob=predictor('my_model.h5',imCrop)
			
				return cls,imCrop
			elif rect[1] in range(y_list[4]-15,y_list[4]+15):
				cls,prob=predictor('my_model.h5',imCrop)
			
				return cls,imCrop
			elif rect[1] in range(y_list[8]-15,y_list[8]+15):
				cls,prob=predictor('my_model.h5',imCrop)
			
				return cls,imCrop
		if rect[0] in range(x_list[9]-15,x_list[9]+15):
			if rect[1] in range(y_list[0]-15,y_list[0]+15):
				cls,prob=predictor('my_model.h5',imCrop)
			
				return cls,imCrop
			elif rect[1] in range(y_list[4]-15,y_list[4]+15):
				cls,prob=predictor('my_model.h5',imCrop)
			
				return cls,imCrop
			elif rect[1] in range(y_list[8]-15,y_list[8]+15):
			
				return '',imCrop

	for rect in rects:
		# Draw the rectangles
		if len(rects)==12:

			cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3) 
		
		
		if(len(rects)==12):
			cls , pic = get_key(rect)    
			cv2.putText(im,str(cls), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)
			global r
			r[str(cls)]=[rect[0],rect[1],rect[2],rect[3]]
	cv2.imshow('img',im)
    #show  the frame with detection
	cv2.waitKey(3)		
if __name__ == '__main__':
	try:
		# Load the classifier
		# clf=joblib.load("cls.pkl")
		#initialise the ros node
		rospy.init_node('realtime_test', anonymous=True)
		# Initalize a subscriber to the "/camera/rgb/image_raw" topic with the function "image_callback" as a callback
		sub_image = rospy.Subscriber("/camera/rgb/image_raw", Image, image_callback)
		# Initialize the CvBridge class
		bridge=CvBridge()
		#for xyz coordinates
		rospy.init_node('pcl_listener', anonymous=True)
		rospy.Subscriber('/camera/depth/points', PointCloud2, callback_pointcloud)
		rospy.spin()

	except rospy.ROSInterruptException:
		rospy.loginfo("node terminated")
