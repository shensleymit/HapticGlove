import Leap, sys, serial, time, math
from time import sleep
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

connected = False

ser = serial.Serial("COM5", 9600)


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

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        a = 0
        # Check if the hand has any fingers
        fingers = frame.pointables
        if fingers.is_empty:
            a = 0
        if not fingers.is_empty:
            finger = fingers.frontmost
            position = finger.tip_position
            x = position.x / 50
            y = (position.y - 50) / 50
            f = pow(2, x)
            if y >= -1.2 + f and y <= 1.2 + f:
               a = 1
            print (x, y)
        ser.write(str(a))
        
        

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
