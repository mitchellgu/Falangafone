import time, sys
sys.path.insert(0, "../../LeapSDK/lib")
sys.path.append("profiles")
from pyo import *
import Leap
from default import *

# Setup Pyo Stream
s = Server().boot()
s.start()
snd = "audio/call_me_maybe.aiff"
sf = SfPlayer(snd, mul=0.5).out()

# Initialize Leap Controller
controller = Leap.Controller()

profile = DefaultProfile()

# Initialize offset Counter, Timestep
i = 0
TIMESTEP = 0.05

while True:
    now = time.time()  # get the time
    print i
    if sf.isPlaying():
      i += 1 * sf.speed

    if(controller.is_connected): #controller is a Leap.Controller object
      # Get frame
      frame = controller.frame()
      # Print frame info
      print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

      # Pause or play
      if len(frame.hands) == 2:
        height = frame.hands[0].palm_position.y + frame.hands[1].palm_position.y
        if sf.isPlaying() and height < 200.0: # If playing and hands are down
          sf.stop()
        elif height>200.0 and not sf.isPlaying(): # If not playing and hands are up
          sf.setOffset(i*TIMESTEP)
          sf.out()

      if sf.isPlaying():
        profile.step(frame, sf)

    elapsed = time.time() - now  # how long was it running?
    time.sleep(TIMESTEP-elapsed)    