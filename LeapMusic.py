import sys
sys.path.append("LeapSDK/lib")
sys.path.append("profiles")
from LeapMusicServer import LeapMusicServer
from flask import *
from default import *
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/start')
def start():
	server.start()

@app.route('/stop')
def stop():
    server.stop()

if __name__ == '__main__':
  server = LeapMusicServer()
  app.debug = True
  app.run()
