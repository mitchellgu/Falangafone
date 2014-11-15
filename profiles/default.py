# Clips number if less than a or greater than b
def clip(num, a, b):
  return min(max(num,a),b)

class DefaultProfile():

  DISTANCE_GAIN = 1/200.0
  HEIGHT_GAIN = 1/400.0

  def step(self, frame, sf):
    if len(frame.hands) == 2:
      print "Two hands present!"

      # Compute distance between palm positions
      distance = frame.hands[0].palm_position.distance_to(frame.hands[1].palm_position)
      print "Distance: " + str(distance)

      # Compute average height of palm positions
      height = frame.hands[0].palm_position.y + frame.hands[1].palm_position.y
      print "Height: " + str(height)

      # Set playback speed proportional to distance
      sf.setSpeed(distance * self.DISTANCE_GAIN)

      # Set playback volume proportional to height
      sf.mul = clip((height-200) * self.HEIGHT_GAIN, 0.0, 1.0)