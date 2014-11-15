from pyo import *
sys.path.insert(0, "../../../LeapSDK/lib")
import Leap, math
from Leap import Finger

# Clips number if less than a or greater than b
def clip(num, a, b):
  return min(max(num,a),b)

class DefaultProfile():

  FINGER_IDS = [Finger.TYPE_THUMB, Finger.TYPE_INDEX, Finger.TYPE_MIDDLE, Finger.TYPE_RING, Finger.TYPE_PINKY]
  DISTANCE_GAIN = 1/200.0
  HEIGHT_GAIN = 1/800.0
  EQ_GAINS = [10, 10, 10, 10, 10]
  source = None
  out = None

  def __init__(self, source):
    self.source = source
    self.out = EQ(source, freq=70, q=1, boost=0, mul=0.1)
    self.out.out()

  def getBentness(self, hand0, hand1, fingerID):
    # Compute angle between thumb and palm normal
    finger0 = hand0.fingers.finger_type(self.FINGER_IDS[fingerID])[0]
    finger1 = hand1.fingers.finger_type(self.FINGER_IDS[fingerID])[0]
    if fingerID == 0:
      angle0 = hand0.palm_normal.angle_to(finger0.bone(1).direction.cross(hand0.direction))
      angle1 = hand1.palm_normal.angle_to(finger1.bone(1).direction.cross(hand1.direction))
    else: 
      angle0 = hand0.palm_normal.angle_to(finger0.bone(1).direction.cross(hand0.basis.x_basis))
      angle1 = hand1.palm_normal.angle_to(finger1.bone(1).direction.cross(hand1.basis.x_basis))
    bentness = 2 - abs(math.pi/2 - angle0) * 2 / math.pi - abs(math.pi/2 - angle1) * 2 / math.pi
    print "Bentness for FingerID = " + str(fingerID) + ": " + str(bentness)
    return bentness


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

      for fingerID in range(len(self.FINGER_IDS)):
        bentness = self.getBentness(hand0, hand1, fingerID)
        if fingerID == 0:
          self.out.setBoost(self.EQ_GAINS[fingerID] * (bentness - 1))
          print "Bass Boost: " + str(self.EQ_GAINS[fingerID] * (bentness - 1))

      # Set playback speed proportional to distance
      self.source.setSpeed(distance * self.DISTANCE_GAIN)

      # Set playback volume proportional to height
      self.out.mul = clip((height-200) * self.HEIGHT_GAIN, 0.0, 0.5)

  def isPlaying(self):
    return self.out.isPlaying()