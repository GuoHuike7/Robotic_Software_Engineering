#!/usr/bin/env python

"""
    talkback.py - Version 1.1 2013-12-20
    
    Use the sound_play client to say back what is heard by the pocketsphinx recognizer.
    
"""

import rospy, os, sys
import aiml
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient

class TalkBack:
    def __init__(self, script_path):
        rospy.init_node('mywork')

        rospy.on_shutdown(self.cleanup)
        
        # Create the sound client object
        self.soundhandle = SoundClient()
        
        # Wait a moment to let the client connect to the
        # sound_play server
        rospy.sleep(1)
        
        # Make sure any lingering sound_play processes are stopped.
        self.soundhandle.stopAll()
        
        # Announce that we are ready for input
        #self.soundhandle.playWave('say-beep.wav')
        #rospy.sleep(2)
        #self.soundhandle.say('Ready')
        
        #rospy.loginfo("Say one of the navigation commands...")

        # Subscribe to the recognizer output and set the callback function
        rospy.Subscriber('lm_data', String, self.talkback)
        
    def talkback(self, msg):
        # Print the recognized words on the screen
        rospy.loginfo(msg.data)
        
        # Speak the recognized words in the selected voice
        # self.soundhandle.say("I heard " + msg.data, volume=0.01)
        # rospy.sleep(5)
	
	if msg.data.find('HELLO') > -1:
	   self.soundhandl.say("Well,hello",volume=0.6)
	   rospy.sleep(6)
	elif msg.data.find('WHAT IS YOUR NAME') > -1:
	   self.soundhandl.say("My name is casie",volume=0.6)
	   rospy.sleep(6)
	elif msg.data.find('HOW OLD ARE YOU') > -1:
	   self.soundhandl.say("I'm ten",volume=0.6)
	   rospy.sleep(6)
	elif msg.data.find('WHAT DO YOU LIKE') > -1:
	   self.soundhandl.say("I like play computer",volume=0.6)
	   rospy.sleep(6)
	elif msg.data.find('I WANT TO MAKE FRIENDS WITH YOU') > -1:
	   self.soundhandl.say("Me too",volume=0.3)
	   rospy.sleep(6)
	elif msg.data.find('I LIKE YOU VERY MUCH') > -1:
	   self.soundhandl.say("Thank you",volume=0.6)
	   rospy.sleep(6)

    def cleanup(self):
        self.soundhandle.stopAll()
        rospy.loginfo("Shutting down talkback node...")

if __name__=="__main__":
    try:
        TalkBack(sys.path[0])
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Talkback node terminated.")
