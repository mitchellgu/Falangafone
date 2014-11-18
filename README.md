# Falangafone  
###### Your music, brought to you by your beloved phalanges
---------------------------------------
Best Use of Leap Motion at HackPrinceton Fall 2014

Instructable [here](http://www.instructables.com/id/Falangafone-Use-Gestures-to-Control-Your-Music/)
ChallengePost [here](http://challengepost.com/software/falangafone)

Falangafone is an interactive python application for live music manipulation through the Leap Motion platform. Falangafone is inspired by fond memories of tweaking car volume knobs along to the radio and takes that idea of music manipulation far further. Through the Leap Motion API, Falangafone calculates several parameters of the user's hand position at once and uses them as inputs to a cascade of audio effects. This leads to great flexibility and creative potential in the sounds users can create.  

Firstly, volume is controlled by the average vertical position of both hands and the panning of stereo audio is determined by the difference in vertical position. The cumulative roll of both hands determines the speed of audio playback. Because playback speed also affects audio frequency, this adjusts both tempo and pitch and is often one of the most entertaining effects.  

The most flexible audio feature of Falangafone is the equalizer, which features five frequency bands whose gains are independently controlled by the position of each finger. Bending a finger increases the gain, while straightening it decreases the gain. Going from thumb to pinky manipulates the audio spectrum in the bass to treble direction. This allows users to literally shape their own filters for the audio in real time with their fingers to yield different sounds. Bending the thumb and index more yields a bass boost, while bending the pinky and ring more yields a brighter sound.  

Falangafone uses a Flask webapp to render a visualization of these audio effects in real time. Upon startup, Flask creates instances of our python audio server class and effect profile class, then communicates with them to display volume, pan, speed, and equalizer levels. The webapp is served across the internet so even third parties can watch the user's creativity flow.  

Controlling Falangafone's music playback is simple and convenient: Pushing the button on an Electric Imp remote starts and stops the current track playback, wirelessly. Resting one's hands below the Leap Motion's range pauses playback. Audio files can be switched through one-hand swipe gestures on the Leap motion. A handy LED array on the Imp remote displays the current track being played back.  
