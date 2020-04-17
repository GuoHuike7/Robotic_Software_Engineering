#!/usr/bin/env python

"""
    partybot.py - Version 0.2 2019-03-30
    
    A party robot to serve guests and entertainment.
    
"""

import rospy
from std_msgs.msg import String
from opencv_apps.msg import Point2D
from sound_play.libsoundplay import SoundClient
import sys
from subprocess import call
from geometry_msgs.msg import Twist
from math import radians
import os
from turtlebot_msgs.srv import SetFollowState

class PartyBot:
    def __init__(self, script_path):
        rospy.init_node('mywork')
        rospy.on_shutdown(self.cleanup)
        self.soundhandle = SoundClient()
        
        # Wait a moment to let the client connect to the sound_play server
        rospy.sleep(1)
        
        # Make sure any lingering sound_play processes are stopped.
        self.soundhandle.stopAll()
       
        rospy.loginfo("Ready, waiting for commands...")
        # Subscribe to the recognizer output and set the callback function
        rospy.Subscriber('/lm_data', String, self.talkback)
	self.location = rospy.Publisher("/location",Point2D,queue_size = 1)
	self.Point=Point2D()
	self.Point.x=0
	self.Point.y=0
    def talkback(self, msg):
        # Print the recognized words on the screen
        #msg.data=msg.data.lower()
        rospy.loginfo(msg.data)
        
        # Speak the recognized words in the selected voice
        # self.soundhandle.say(msg.data, self.voice)
        # call('rosrun sound_play say.py "montreal"', shell=True)
        # rospy.sleep(1)
	if msg.data.find('CAN YOU NAVIGATE FOR ME')>-1:
		self.soundhandle.say("Yes,of course!")
		rospy.sleep(1) 
	elif msg.data.find('GO TO THE BOOKSHELF')>-1:
		self.soundhandle.say("Ok,wait for a minute!")
		self.Point.x=-1.8
		self.Point.y=-6.77
		self.location.publish(self.Point)
		rospy.sleep(1) 
	elif msg.data.find('GO TO THE BALL')>-1:
        	self.soundhandle.say("OK, wait for a minute!")
		self.Point.x=1.91
		self.Point.y=1.07
		self.location.publish(self.Point)
		rospy.sleep(1)
	elif msg.data.find('GO TO THE WHEEL')>-1:
        	self.soundhandle.say("OK, wait for a minute!")
		self.Point.x=4.27
		self.Point.y=-2.39
		self.location.publish(self.Point)
		rospy.sleep(1)
	elif msg.data.find('GO BOXES')>-1:
        	self.soundhandle.say("OK, wait for a minute!")
		self.Point.x=-5
		self.Point.y=2.06
		self.location.publish(self.Point)
		rospy.sleep(1)
	elif msg.data.find('OVER THANK YOU')>-1:
		self.soundhandle.say("Ok,see you")   
		rospy.sleep(1)      
	else: rospy.sleep(3)
        
        
    def cleanup(self):
        self.soundhandle.stopAll()
        rospy.loginfo("Shutting down mywork node...")

if __name__=="__main__":
    try:
        PartyBot(sys.path[0])
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("mywork node terminated.")
