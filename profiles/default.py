from pyo import *
sys.path.insert(0, "../../../LeapSDK/lib")
import Leap, math
from Leap import Finger

# Clips number if less than a or greater than b
def clip(num, a, b):
  return min(max(num,a),b)

class DefaultProfile:

  FINGER_IDS = [Finger.TYPE_THUMB, Finger.TYPE_INDEX, Finger.TYPE_MIDDLE, Finger.TYPE_RING, Finger.TYPE_PINKY]
  ROLL_GAIN = 1/4.0
  HEIGHT_GAIN = 1/400.0
  EQ_FREQS = [53, 237, 1020, 3677, 10200]
  EQ_GAINS = [15, 15, 15, 15, 15]
  source = None
  eqs = [None, None, None, None, None]
  out = None

  def __init__(self, source):
    self.source = source
    self.eqs[0] = EQ(source, freq=self.EQ_FREQS[0], boost=0)
    self.eqs[1] = EQ(self.eqs[0], freq=self.EQ_FREQS[1], boost=0)
    self.eqs[2] = EQ(self.eqs[1], freq=self.EQ_FREQS[2], boost=0)
    self.eqs[3] = EQ(self.eqs[2], freq=self.EQ_FREQS[3], boost=0)
    self.eqs[4] = EQ(self.eqs[3], freq=self.EQ_FREQS[4], boost=0)
    self.pan = Pan(self.eqs[4])
    self.out = self.pan

  def getBentness(self, hand0, hand1, fingerID):
    # Compute bentness based on finger coplanarity with palm in direction of articulation
    finger0 = hand0.fingers.finger_type(self.FINGER_IDS[fingerID])[0]
    finger1 = hand1.fingers.finger_type(self.FINGER_IDS[fingerID])[0]
    # For thumbs, calculate angle between palm normal and thumb crossed with hand direction
    if fingerID == 0:
      angle0 = hand0.palm_normal.angle_to(finger0.bone(1).direction.cross(hand0.direction))
      angle1 = hand1.palm_normal.angle_to(finger1.bone(1).direction.cross(hand1.direction))
    # For non-thumbs, calculate angle between palm normal and finger crossed with x basis of hand
    else: 
      angle0 = hand0.palm_normal.angle_to(finger0.bone(2).direction.cross(hand0.basis.x_basis))
      angle1 = hand1.palm_normal.angle_to(finger1.bone(2).direction.cross(hand1.basis.x_basis))
    bentness = 2 - abs(math.pi/2 - angle0) * 2 / math.pi - abs(math.pi/2 - angle1) * 2 / math.pi
    #print "Bentness for FingerID = " + str(fingerID) + ": " + str(bentness)
    return bentness

  def start(self):
    self.out.out()

  def step(self, frame):
    if self.out.isPlaying() and len(frame.hands) == 2:
      print "Two hands present!"
      hand0 = frame.hands.leftmost
      hand1 = frame.hands.rightmost

      # Compute distance between palm positions
      #distance = hand0.palm_position.distance_to(hand1.palm_position)
      #print "Distance: " + str(distance)

      # Compute roll of palm normals
      roll = hand0.palm_normal.roll - hand1.palm_normal.roll
      #print "Roll: " + str(roll)

      # Compute average height of palm positions
      height = hand0.palm_position.y + hand1.palm_position.y
      print "Height: " + str(height)

      # Compute difference in height of palm positions
      ydiff = (-hand0.palm_position.y + hand1.palm_position.y)/500.0

      # Set playback pan proportional to ydiff
      self.pan.setPan(clip(ydiff + 0.5, 0, 1))

      for fingerID in range(len(self.FINGER_IDS)):
        bentness = self.getBentness(hand0, hand1, fingerID)
        self.eqs[fingerID].setBoost(self.EQ_GAINS[fingerID] * (bentness - 1))
        print "Boost for EQ" + str(fingerID) + ": " + str(self.EQ_GAINS[fingerID] * (bentness - 1))

      # Set playback speed proportional to roll
      if roll > 0.7:
        self.source.setSpeed(clip(1 + (roll-0.7) * self.ROLL_GAIN, 1.0, 2.0))
      elif roll < -0.5:
        self.source.setSpeed(clip(1 + (roll+0.5) * self.ROLL_GAIN, 0.5, 1.0))
      else:
        self.source.setSpeed(1)
      print "Playback Speed: " + str(self.source.speed)

      # Set playback volume proportional to height
      self.source.mul = clip((height-200) * self.HEIGHT_GAIN, 0.0, 1.0)

    return {"volume": str(int(round(self.source.mul*100))),
            "speed": str(int(round(self.source.speed * 100))),
            "pan": str(int(round(self.pan.pan*100))),
            "eq0": (self.eqs[0].boost + 15.0)/30.0 * 100,
            "eq1": (self.eqs[1].boost + 15.0)/30.0 * 100,
            "eq2": (self.eqs[2].boost + 15.0)/30.0 * 100,
            "eq3": (self.eqs[3].boost + 15.0)/30.0 * 100,
            "eq4": (self.eqs[4].boost + 15.0)/30.0 * 100}

  def isPlaying(self):
    return self.source.isPlaying()