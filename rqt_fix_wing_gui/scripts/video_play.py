#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import sys

rospy.init_node('video_pub', anonymous=True)
img_pub = rospy.Publisher('/airsim_node/drone_1/front_center_custom/Scene', Image, queue_size=2)
rate = rospy.Rate(5) # 5hz

# print(sys.argv[1])
address = '/home/x/catkin_ws/src/demo/{}.mp4'.format(sys.argv[1])
rospy.loginfo(address)


# make a video_object and init the video object
cap = cv2.VideoCapture(address)
# define picture to_down' coefficient of ratio
scaling_factor = 0.5
bridge = CvBridge()
if not cap.isOpened():
    sys.stdout.write("video is not available !")

count = 0
# loop until press 'esc' or 'q'
while not rospy.is_shutdown():
    ret, frame = cap.read()
    # resize the frame
    if ret:
        count = count + 1
    else:
        rospy.loginfo("Capturing image failed.")
    if count == 2:
        count = 0
        frame = cv2.resize(frame,None,fx=scaling_factor,fy=scaling_factor,interpolation=cv2.INTER_AREA)
        msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        img_pub.publish(msg)
    rate.sleep()
        
# if(self.Box_video_src.currentText()=='real time'):