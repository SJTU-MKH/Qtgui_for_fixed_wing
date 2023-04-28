#!/usr/bin/env python
import rospy
import sys
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def pubVideo():
    rospy.init_node('video_pub', anonymous=True)
    img_pub = rospy.Publisher('/airsim_node/drone_1/front_center_custom/Scene', Image, queue_size=10)
    rate = rospy.Rate(10)
    path = '/home/x/catkin_ws/src/demo/{}.mp4'.format(sys.argv[1])
    # rospy.loginfo(address)

    cap = cv2.VideoCapture(path)
    scaling_factor = 0.5
    bridge = CvBridge()
    if not cap.isOpened():
        sys.stdout.write("video is not available !")
        return

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        # resize the frame
        if ret:
            frame = cv2.resize(frame,None,fx=scaling_factor,fy=scaling_factor,interpolation=cv2.INTER_AREA)
            msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            img_pub.publish(msg)
        else:
            return
        rate.sleep()
        
if __name__ == '__main__':
    try:
        pubVideo()
    except rospy.ROSInterruptException:
        pass

# if(self.Box_video_src.currentText()=='real time'):