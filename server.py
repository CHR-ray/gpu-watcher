import json
import time
import yaml
import os
from flask import Flask, request, render_template, send_file
from datetime import datetime


with open(os.path.join(os.path.split(__file__)[0], 'config.yaml')) as f:
    config = yaml.load(f)

app = Flask(__name__)

gpu_stats_dict = {}

@app.route('/')
def index():
    now = datetime.now().strftime('Updated at %Y-%m-%d %H-%M-%S')
    return render_template('index.html',gpustats=gpu_stats_dict,update_time=now)


@app.route('/api/gpu', methods=['GET', 'POST'])
def gpu():
    return json.dumps(gpu_stats_dict, sort_keys=True)

@app.route('/api/ping', methods=['GET', 'POST'])
def ping():
    body = 0
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data.decode())
        if not data.get('ip'):
            body = 1
        else:
            gpu_stats_dict[data['ip']] = data
    return str(body)

@app.route('/api/myip', methods=['GET'])
def myip():
    ip = request.remote_addr
    return ip

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(config['lab']['center']['port']))