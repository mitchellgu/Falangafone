import sys
sys.path.append("../")
sys.path.append("../LeapSDK/lib")
sys.path.append("../profiles")
import LeapMusicServer
from flask import *
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/start')
def start():
	server.start("audio/call_me_maybe.aiff", DefaultProfile)

if __name__ == '__main__':
  server = LeapMusicServer()
  app.debug = True
  app.run()