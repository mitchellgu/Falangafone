import time, sys, threading
sys.path.insert(0, "LeapSDK/lib")
sys.path.append("profiles")
from pyo import *
import Leap
from default import *

class SongThread(threading.Thread):
  """Thread class with a stop() method. The thread itself has to check
  regularly for the stopped() condition."""

  parameters = None

  def __init__(self, controller, source, profile):
      super(SongThread, self).__init__()
      self.source = source
      self.controller = controller
      self.controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES);
      self.profile = profile(self.source)
      self._stop = threading.Event()

  def stop(self):
      self._stop.set()

  def stopped(self):
      return self._stop.isSet()

  def run(self):
    self.profile.start()

    # Initialize offset Counter, Timestep
    i = 0
    TIMESTEP = 0.05

    while not self.stopped():
        now = time.time()  # get the time
        print i
        if self.source.isPlaying():
          i += 1 * self.source.speed

        if(self.controller.is_connected): #controller is a Leap.Controller object
          # Get frame
          frame = self.controller.frame()
          # Print frame info
          print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

          # Pause or play
          if len(frame.hands) == 2:
            height = frame.hands[0].palm_position.y + frame.hands[1].palm_position.y
            if self.source.isPlaying() and height < 200.0: # If playing and hands are down
              self.source.stop()
            elif height>200.0 and not self.source.isPlaying(): # If not playing and hands are up
              self.source.setOffset(i*TIMESTEP)
              self.source.out()

          # Step the profile one timestep
          self.parameters = str(self.profile.step(frame))

        elapsed = time.time() - now  # how long was it running?
        time.sleep(TIMESTEP-elapsed)

    self.profile.source.stop()

  def getParameters(self):
    return str(self.parameters)

class LeapMusicServer:

  songThread = None
  isplaying = False

  def __init__(self):
    # Setup Pyo Stream
    self.s = Server().boot()
    self.s.start()
    # Initialize Leap Controller
    self.controller = Leap.Controller()

  def start(self, snd="audio/call_me_maybe.aiff", profile=DefaultProfile):
    if self.isplaying ==False:
        self.isplaying = True
        source = SfPlayer("audio/call_me_maybe.aiff", mul=0.5)
        self.songThread = SongThread(self.controller, source, profile)
        self.songThread.start()

  def stop(self):
    if self.isplaying ==True:
        self.songThread.stop()
        self.isplaying = False

  def getParameters(self):
    return self.songThread.getParameters()

if __name__ == '__main__':
  server = LeapMusicServer()
  server.start("audio/call_me_maybe.aiff", DefaultProfile)
  time.sleep(10)
  server.stop()
