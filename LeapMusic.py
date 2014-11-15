import time, sys
sys.path.insert(0, "../../LeapSDK/lib")
from pyo import *
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

# Setup Pyo Stream
s = Server().boot()
s.start()
snd = "call_me_maybe.aiff"
sf = SfPlayer(snd).out()
controller = Leap.Controller()

# Initialize Frame Counter
i = 0
isPlaying = True

# Clips number if less than a or greater than b
def clip(num, a, b):
  return min(max(num,a),b)

while True:
    now = time.time()            # get the time
    print i
    i += 1

    if(controller.is_connected): #controller is a Leap.Controller object
      frame = controller.frame()
      print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

      # Get hands
      for hand in frame.hands:

        handType = "Left hand" if hand.is_left else "Right hand"

        print "  %s, id %d, position: %s" % (
          handType, hand.id, hand.palm_position)

      if len(frame.hands) == 2:
        print "Two hands present!"
        distance = frame.hands[0].palm_position.distance_to(frame.hands[1].palm_position)
        print distance
        height = frame.hands[0].palm_position.y + frame.hands[1].palm_position.y
        print "height: " + str(height)
        sf.setSpeed(distance/200.0)
        sf.mul = clip((height-200)/400.0, 0.0, 1.0)
        if isPlaying and height < 200.0:
          isPlaying = False
          sf.stop()
        elif height>200.0 and not isPlaying:
          isPlaying = True
          sf.out()

    elapsed = time.time() - now  # how long was it running?
    time.sleep(0.02-elapsed)    