import json
import time
import yaml
import os
from flask import Flask, request, send_file,render_template


with open(os.path.join(os.path.split(__file__)[0], 'config.yaml')) as f:
    config = yaml.load(f)

app = Flask(__name__)

act_map = {}

@app.route('/')
def index():
    return send_file('templates/index.html',act_map)
    # return render_template('index.html',gpu_data=act_map)


@app.route('/api/gpu', methods=['GET'])
def gpu():
    return json.dumps(act_map)

@app.route('/api/ping', methods=['GET', 'POST'])
def ping():
    body = 0
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data.decode())
        if not data.get('ip'):
            body = 1
        else:
            act_map[data['host']] = data
    return str(body)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999)
