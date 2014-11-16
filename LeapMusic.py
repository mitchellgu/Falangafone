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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/toggle')
def toggle():
	if server.isplaying:
	  server.stop()
	  return "OK", 200
	else:
		server.start(DefaultProfile)
		return "OK", 200

@app.route('/params')
def params():
	if server.isplaying:
		return jsonify(server.getParameters()), 200
	else:
		return jsonify({"volume": 50, "speed": 100, "pan": 50, "eq0": 50, "eq1": 50, "eq2": 50, "eq3": 50, "eq4": 50}), 200

if __name__ == '__main__':
  server = LeapMusicServer()
  app.debug = True
  app.run()
