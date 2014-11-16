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
	return "OK", 200

@app.route('/stop')
def stop():
  server.stop()
  return "OK", 200

@app.route('/params')
def params():
	if server.isplaying:
		return jsonify(server.getParameters()), 200
	else:
		return jsonify({"height": "N/A"}), 200

if __name__ == '__main__':
  server = LeapMusicServer()
  app.debug = True
  app.run()
