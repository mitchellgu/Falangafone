from pyo import *
sys.path.insert(0, "../../../LeapSDK/lib")
import Leap, math
from Leap import *

# Clips number if less than a or greater than b
def clip(num, a, b):
  return min(max(num,a),b)

class DefaultProfile():

  DISTANCE_GAIN = 1/200.0
  HEIGHT_GAIN = 1/800.0
  source = None
  out = None

  def __init__(self, source):
    self.source = source
    self.out = EQ(source, freq=100, q=1, boost=0, mul=0.1)
    self.out.out()

  def step(self, frame):
    if self.out.isPlaying() and len(frame.hands) == 2:
      print "Two hands present!"
      hand0 = frame.hands[0]
      hand1 = frame.hands[1]

      # Compute distance between palm positions
      distance = hand0.palm_position.distance_to(hand1.palm_position)
      print "Distance: " + str(distance)

      # Compute average height of palm positions
      height = hand0.palm_position.y + hand1.palm_position.y
      print "Height: " + str(height)

      # Compute angle between thumb and palm normal
      thumb0 = hand0.fingers.finger_type(Finger.TYPE_THUMB)[0]
      thumb1 = hand1.fingers.finger_type(Finger.TYPE_THUMB)[0]
      angle0 = hand0.palm_normal.angle_to(thumb0.bone(1).direction.cross(hand0.direction))
      angle1 = hand1.palm_normal.angle_to(thumb1.bone(1).direction.cross(hand1.direction))
      bentness0 = 1-abs(math.pi/2 - angle0) * 2 / math.pi
      bentness1 = 1-abs(math.pi/2 - angle1) * 2 / math.pi
      print "Bentness 0: " + str(bentness0)
      print "Bentness 1: " + str(bentness1)

      # Set playback speed proportional to distance
      self.source.setSpeed(distance * self.DISTANCE_GAIN)

      # Set playback volume proportional to height
      self.out.mul = clip((height-200) * self.HEIGHT_GAIN, 0.0, 0.5)

  def isPlaying(self):
    return self.out.isPlaying()