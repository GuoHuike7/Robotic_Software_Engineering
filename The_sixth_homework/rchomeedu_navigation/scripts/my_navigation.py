#!/usr/bin/env python

"""

    RoboCup@Home Education | oc@robocupathomeedu.org
    navi.py - enable turtlebot to navigate to predefined waypoint location

"""

import rospy

import actionlib
from actionlib_msgs.msg import *
from std_msgs.msg import String
from opencv_apps.msg import Point2D
from sound_play.libsoundplay import SoundClient
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler

original = 0
start = 1

class NavToPoint:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        self.soundhandle = SoundClient()
        
        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        rospy.loginfo("Waiting for move_base action server...")

        # Wait for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(120))
        rospy.loginfo("Connected to move base server")

        # A variable to hold the initial pose of the robot to be set by the user in RViz
        initial_pose = PoseWithCovarianceStamped()
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)
	rospy.Subscriber('/location',Point2D,self.locate)


        # Get the initial pose from the user
        rospy.loginfo("*** Click the 2D Pose Estimate button in RViz to set the robot's initial pose...")
        rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)
        
        

        # Make sure we have the initial pose
        while initial_pose.header.stamp == "":
                rospy.sleep(1)
            
        rospy.loginfo("Ready to go")
        rospy.sleep(1)

        

    def locate(self,msg):
        locations = dict()

        # Location A
        A_x = msg.x
        A_y = msg.y
        A_theta = 0

        quaternion = quaternion_from_euler(0.0, 0.0, A_theta)
        locations['A'] = Pose(Point(A_x, A_y, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

        self.goal = MoveBaseGoal()
        rospy.loginfo("Starting navigation test")


        while not rospy.is_shutdown():
          self.goal.target_pose.header.frame_id = 'map'
          self.goal.target_pose.header.stamp = rospy.Time.now()

          # Robot will go to point A

          rospy.loginfo("Going to point A")
          rospy.sleep(2)
          self.goal.target_pose.pose = locations['A']
          self.move_base.send_goal(self.goal)
          waiting = self.move_base.wait_for_result(rospy.Duration(300))
          if waiting == 1:
                    rospy.loginfo("Reached point A")
                    self.soundhandle.say("Here am I!")
                    rospy.sleep(2)
                    rospy.loginfo("I'm ready to go to another place.")
                    self.soundhandle.say("I'm ready to go to another place.")
                    rospy.sleep(2)
                    global start
		    break
                    #start = 0

          rospy.Rate(5).sleep()
        

    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose
        #if original == 0:
        self.origin = self.initial_pose.pose.pose
                

    def cleanup(self):
        rospy.loginfo("Shutting down navigation ....")
        self.move_base.cancel_goal()

if __name__=="__main__":
    rospy.init_node('navi_point')
    try:
        NavToPoint()
        rospy.spin()
    except:
        pass


