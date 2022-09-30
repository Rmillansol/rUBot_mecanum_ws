#!/usr/bin/env python3
import rospy
import sys
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2

class camera_sub:

    def __init__(self):
        self.camera_sub = rospy.Subscriber('/rubot/camera1/image_raw',Image, self.camera_cb)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.vel_msg=Twist()
        self.bridge=CvBridge()



    def camera_cb(self, data):
        frame = self.bridge.imgmsg_to_cv2(data,'bgr8')
        frame = frame[290:479,130:400] # First is Y and sencond is X
        edged = cv2.Canny(frame ,60,100 )

        white_index=[]
        mid_point_line = 0
        for index,values in enumerate(edged[:][172]):
            if(values == 255):
                white_index.append(index)
        print(white_index)

        if(len(white_index) == 2 ):
            cv2.circle(img=edged, center = (white_index[0],172), radius = 2 , color = (255,0,0), thickness=1)
            cv2.circle(img=edged, center = (white_index[1],172), radius = 2 , color = (255,0,0), thickness=1)
            mid_point_line = int ( (white_index[0] + white_index[1]) /2 )
            cv2.circle(img=edged, center = (mid_point_line,172), radius = 3 , color = (255,0,0), thickness=2)

        mid_point_robot = [135,172]
        cv2.circle(img=edged, center = (mid_point_robot[0],mid_point_robot[1]), radius = 5 , color = (255,0,0), thickness=2)
        error = mid_point_robot[0] - mid_point_line
        print("Error -> " , error)

        if ( error < 0):
            self.vel_msg.angular.z = -0.5
        else:
            self.vel_msg.angular.z = 0.5

        self.vel_msg.linear.x = 0.4

        self.cmd_vel_pub.publish(self.vel_msg)


        cv2.imshow('Frame',frame)
        cv2.imshow('Canny Output',edged)
        cv2.waitKey(1)


def main(args=None):
    rospy.init_node('line_following_sim', anonymous=True)

    sensor_sub = camera_sub()

    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print ("Ending MoveForward")