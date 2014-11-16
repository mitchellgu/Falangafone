import time, sys, threading
sys.path.insert(0, "LeapSDK/lib")
sys.path.append("profiles")
from pyo import *
import Leap
from Leap import SwipeGesture
from default import *
from os import walk, path

class SongThread(threading.Thread):
  """Thread class with a stop() method. The thread itself has to check
  regularly for the stopped() condition."""

  parameters = {"volume": "stopped", "speed": "stopped", "pan": "stopped", "eq0": 50, "eq1": 50, "eq2": 50, "eq3": 50, "eq4": 50}

  def __init__(self, server, controller, source, profile):
      super(SongThread, self).__init__()
      self.server = server
      self.source = source
      self.controller = controller
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

          if len(frame.gestures())>0 and i > 15:
            maxSwipe = SwipeGesture(frame.gestures()[0])
            for gesture in frame.gestures():
              if maxSwipe.speed < SwipeGesture(gesture).speed:
                maxSwipe = SwipeGesture(gesture)
            if abs(maxSwipe.direction[0]) > abs(maxSwipe.direction[1]):
              if maxSwipe.direction[0] > 0: # swipe right
                self.server.prevTrack()
              else:
                self.server.nextTrack()

          # Step the profile one timestep
          self.parameters = self.profile.step(frame)

        elapsed = time.time() - now  # how long was it running?
        time.sleep(TIMESTEP-elapsed)

    self.profile.source.stop()

  def getParameters(self):
    return self.parameters

class LeapMusicServer:

  songThread = None
  isplaying = False

  def __init__(self, startSong = 0):
    # Setup Pyo Stream
    self.s = Server().boot()
    self.s.start()
    self.currentSong = startSong
    # Initialize Leap Controller
    self.controller = Leap.Controller()
    self.controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES);
    self.controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
    self.TRACKS = []
    for (dirpath, dirnames, filenames) in walk('audio'):
      self.TRACKS.extend(filenames)
      break
    if os.path.exists(".DS_STORE"):
      self.TRACKS.remove(".DS_Store")

  def start(self, profile):
    if self.isplaying ==False:
        self.isplaying = True
        source = SfPlayer("audio/" + self.TRACKS[self.currentSong], mul=0.5)
        self.songThread = SongThread(self, self.controller, source, profile)
        self.songThread.start()

  def stop(self):
    if self.isplaying ==True:
        self.songThread.stop()
        self.isplaying = False

  def nextTrack(self):
    self.stop()
    print "CURRENT SONG: " + str(self.currentSong)
    self.currentSong += 1
    self.currentSong %= len(self.TRACKS)
    print "NEXT SONG: " + str(self.currentSong)
    self.start(DefaultProfile)

  def prevTrack(self):
    self.stop()
    print "CURRENT SONG: " + str(self.currentSong)
    self.currentSong -= 1
    self.currentSong %= len(self.TRACKS)
    print "PREV SONG: " + str(self.currentSong)
    self.start(DefaultProfile)

  def getParameters(self):
    parameters = self.songThread.getParameters()
    parameters["track"] = os.path.splitext(self.TRACKS[self.currentSong])[0]
    return parameters

if __name__ == '__main__':
  server = LeapMusicServer()
  server.start("audio/i_love_it.flac", DefaultProfile)
  time.sleep(10)
  server.stop()
