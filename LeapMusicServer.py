import time, sys, threading
sys.path.insert(0, "LeapSDK/lib")
sys.path.append("profiles")
from pyo import *
import Leap
from default import *

class SongThread(threading.Thread):
  """Thread class with a stop() method. The thread itself has to check
  regularly for the stopped() condition."""

  def __init__(self, controller, source, profile):
      super(SongThread, self).__init__()
      self.source = source
      self.controller = controller
      self.profile = profile
      self._stop = threading.Event()

  def stop(self):
      self._stop.set()

  def stopped(self):
      return self._stop.isSet()

  def run(self):
    profile = self.profile(self.source)

    # Initialize offset Counter, Timestep
    i = 0
    TIMESTEP = 0.05

    while not self.stopped():
        now = time.time()  # get the time
        print i
        if profile.isPlaying():
          i += 1 * profile.source.speed

        if(self.controller.is_connected): #controller is a Leap.Controller object
          # Get frame
          frame = self.controller.frame()
          # Print frame info
          print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

          # Pause or play
          if len(frame.hands) == 2:
            height = frame.hands[0].palm_position.y + frame.hands[1].palm_position.y
            if profile.isPlaying() and height < 200.0: # If playing and hands are down
              profile.source.stop()
            elif height>200.0 and not profile.isPlaying(): # If not playing and hands are up
              profile.source.setOffset(i*TIMESTEP)
              profile.source.out()

          # Step the profile one timestep
          profile.step(frame)

        elapsed = time.time() - now  # how long was it running?
        time.sleep(TIMESTEP-elapsed)

    profile.source.stop()

class LeapMusicServer:

  songThread = None

  def __init__(self):
    # Setup Pyo Stream
    self.s = Server().boot()
    self.s.start()
    # Initialize Leap Controller
    self.controller = Leap.Controller()

  def start(self, snd="audio/call_me_maybe.aiff", profile=DefaultProfile):
    source = SfPlayer("audio/call_me_maybe.aiff", mul=0.5)
    self.songThread = SongThread(self.controller, source, profile)
    self.songThread.start()

  def stop(self):
    self.songThread.stop()

if __name__ == '__main__':
  server = LeapMusicServer()
  server.start("audio/call_me_maybe.aiff", DefaultProfile)
  time.sleep(10)
  server.stop()
