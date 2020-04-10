#!/usr/bin/env python

"""
    talkback.py - Version 1.1 2013-12-20
    
    Use the sound_play client to say back what is heard by the pocketsphinx recognizer.
    
"""

import rospy, os, sys
import aiml,cv2
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
import message_filters
from sensor_msgs.msg import Image
from opencv_apps.msg import FaceArrayStamped
from opencv_apps.srv import FaceRecognitionTrain, FaceRecognitionTrainRequest


kernel = aiml.Kernel()
kernel.learn("/home/casie/catkin_ws/src/rc-home-edu-learn-ros/The_fifth_homework/rchomeedu_speech/aiml/std-startup.xml")
kernel.respond("load aiml b")
 

class TalkBack:
    
    def __init__(self, script_path):
        rospy.init_node('mywork2')

        rospy.on_shutdown(self.cleanup)
        
        # Create the sound client object
        self.soundhandle = SoundClient()
        
        # Wait a moment to let the client connect to the
        # sound_play server
        rospy.sleep(1) 
	self.okstr = ''
	
        # Make sure any lingering sound_play processes are stopped.
        self.soundhandle.stopAll()
        
        # Announce that we are ready for input
        #self.soundhandle.playWave('say-beep.wav')
        #rospy.sleep(2)
        #self.soundhandle.say('Ready')
        
        #rospy.loginfo("Say one of the navigation commands...")

        # Subscribe to the recognizer output and set the callback function
        rospy.Subscriber('/lm_data', String, self.talkback1)
	rospy.Subscriber('/face_recognition/output', FaceArrayStamped, self.talkback)

    
    def talkback1(self,lm): 
	self.okstr = lm.data
	print(lm.data)
	if kernel.respond(lm.data)!='':
		print(kernel.respond(lm.data))
		self.soundhandle.say(kernel.respond(lm.data),volume=0.6) 

    def talkback(self, msg):
        # Print the recognized words on the screen
        #rospy.loginfo(msg.faces)
        #print(msg.faces[0].face.x)
        # Speak the recognized words in the selected voice
        # self.soundhandle.say("I heard " + msg.data, volume=0.01)
	name=msg.faces[0].label
	print(self.okstr)
	if self.okstr == 'HELLO':
		self.soundhandle.say("hello,%s" % name)
        if self.okstr == 'OK':
		self.soundhandle.say("Please sit on the center!")
		rospy.sleep(5)
		# if kernel.respond(msg.data)!='':
			# print(kernel.respond(msg.data))
			# self.soundhandle.say(kernel.respond(msg.data),volume=0.6)
		if msg.faces[0].face.x<200 :
			print("To the left a little!")
			self.soundhandle.say("To the left a little!")
			rospy.sleep(3)
		if msg.faces[0].face.x>400 :
			print("To the right a little!")
			self.soundhandle.say("To the right a little!")
			rospy.sleep(3)
		if msg.faces[0].face.x>200 and msg.faces[0].face.x<400:
			print("Keep it!")
			self.soundhandle.say("Keep it!")
			rospy.sleep(3)
			self.soundhandle.say("three")
			rospy.sleep(1)
			self.soundhandle.say("two")
			rospy.sleep(1)
			self.soundhandle.say("one")
			rospy.sleep(1)
			pub = rospy.Publisher('take_photo', String, queue_size=10)
			pub.publish("take a photo")
    def cleanup(self):
        self.soundhandle.stopAll()
        rospy.loginfo("Shutting down mywork2 node...")

if __name__=="__main__":
    #global okstr =''
    try:
        TalkBack(sys.path[0])
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Mywork2 node terminated.")
