###########################################################################
# This is one of several different files that create a specific function. #
# A lot of the framework for this function runs with the LeapMotion       #
# software. It isn't possible to adjust how many arguements get passed    #
# into those functions, or when they are called.                          #
#                                                                         #
# The file starts with main, which allows the LeapMotion device to be     #
# initialized. The sleep is necessary, and without it the program tries   #
# running when the LeapMotion isn't ready to send and receive data.       #
# The sys.stdin.readline() is a built in function that calls functions in #
# the SampleListener class when the corresponding event happens.          #
#                                                                         #
# on_init(), on_connect(), on_disconnect(), on_exit(), and state_string() #
# are all functions that go with sys.stdin.readline(). I didn't adjust    #
# those functions at all.                                                 #
###########################################################################

import Leap, sys, serial, time, math
from time import sleep
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

connected = False

ser = serial.Serial("COM5", 9600) #this is where the Arduino is connected


class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        ser.write("0")
        ser.close()
        print "Exited"

    def on_frame(self, controller): #this is called several times per second
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        a = 0 #this is what's passed from the LeapMotion to the Arduino
        # Check if the hand has any fingers
        fingers = frame.pointables 
        if fingers.is_empty: #if there are no fingers in the frame, it doesn't vibrate
            a = 0 #a = 0 corresponds to not vibrating
        if not fingers.is_empty:
            finger = fingers.frontmost #picks the finger that's the farthest forward if there's multiple fingers
            x = finger.tip_position.x / 50
            #the coordinates are in millimeters, so /50 makes the scale of the coordinates reasonable
            y = (finger.tip_position.y - 50) / 50
            # tip_position.y = 0 is at the center of the LeapMotion, so -50 moves the origin up by one unit
            f = x #this is different in each of the files
            if y >= -1.2 + f and y <= 1.2 + f: #the tolerance is 1.2 units
               a = 1 #this means vibrate
            print (x, y) #prints coordinates, good for debugging and figuring out where your finger is
        ser.write(str(a)) #writes a to the Arduino to cause the vibration/no vibration
        
        

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    time.sleep(2)

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)



    
if __name__ == "__main__":
    main()
