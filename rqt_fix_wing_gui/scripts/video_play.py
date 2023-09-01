#!/usr/bin/env python
import rospy
import sys
import cv2
import csv
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge, CvBridgeError

def pubVideo_1(path):
    rospy.init_node('video_pub_1', anonymous=True)
    img_pub1 = rospy.Publisher('/airsim_node/drone_1/front_center_custom/Scene1', Image, queue_size=10)
    rate = rospy.Rate(10)

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
            img_pub1.publish(msg)
        else:
            return
        rate.sleep()

def pubVideo_2(path1, path2):
    rospy.init_node('video_pub_2', anonymous=True)
    img_pub1 = rospy.Publisher('/airsim_node/drone_1/front_center_custom/Scene1', Image, queue_size=10)  # for image
    img_pub2 = rospy.Publisher('/airsim_node/drone_1/front_center_custom/Scene2', Image, queue_size=10)  # for lidar
    rypd_pub = rospy.Publisher('/rypd_data', Float32MultiArray, queue_size=10)
    rate = rospy.Rate(10)

    rypd_data = np.loadtxt('../../demo/rypd_data.txt')
    rypd_index = 0
    cap1 = cv2.VideoCapture(path1)
    cap2 = cv2.VideoCapture(path2)
    scaling_factor = 0.5
    bridge = CvBridge()
    if not cap1.isOpened():
        sys.stdout.write("video1 is not available !")
        return
    if not cap2.isOpened():
        sys.stdout.write("video2 is not available !")
        return

    while not rospy.is_shutdown():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        # resize the frame
        if ret1:
            frame1 = cv2.resize(frame1,None,fx=scaling_factor,fy=scaling_factor,interpolation=cv2.INTER_AREA)
            msg1 = bridge.cv2_to_imgmsg(frame1, encoding="bgr8")
            img_pub1.publish(msg1)
        else:
            return
        
        if ret2:
            frame2 = cv2.resize(frame2,None,fx=scaling_factor,fy=scaling_factor,interpolation=cv2.INTER_AREA)
            msg2 = bridge.cv2_to_imgmsg(frame2, encoding="bgr8")
            img_pub2.publish(msg2)
        else:
            return
        
        rypd = Float32MultiArray(data=rypd_data[rypd_index])
        rypd_pub.publish(rypd)
        rypd_index += 1

        rate.sleep()
        


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'demo1':
            path = '../../demo/demo1.mp4'
            pubVideo_1(path)
        elif sys.argv[1] == 'demo2':    # original
            path = '../../demo/original.mp4'
            pubVideo_1(path)
        elif sys.argv[1] == 'demo3':    # process and lidar
            path1 = '../../demo/process.mp4'
            path2 = '../../demo/lidar.mp4'
            pubVideo_2(path1, path2)
        elif sys.argv[1] == 'demo4':
            path = '../../demo/blur_deblur.mp4'
            pubVideo_1(path)
        else:
            pass
            # path = '../../demo/{}.mp4'.format(sys.argv[1])
        # rospy.loginfo(address)
    except rospy.ROSInterruptException:
        pass

# if(self.Box_video_src.currentText()=='real time'):