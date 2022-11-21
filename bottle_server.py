import json
import os
from datetime import datetime

import yaml
from bottle import TEMPLATE_PATH, Bottle, request, response, template


with open(os.path.join(os.path.split(__file__)[0], 'config.yaml')) as f:
    config = yaml.load(f)


app = Bottle()
abs_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_path, 'views')
TEMPLATE_PATH.insert(0, abs_views_path)

EXCLUDE_SELF = False  # Do not report to `/gpustat` calls.


gpustats = {}

@app.route('/')
def index():
    now = datetime.now().strftime('Updated at %Y-%m-%d %H-%M-%S')
    return template('index', gpustats=gpustats, update_time=now)


@app.route('/gpustat', methods=['GET'])
def report_gpustat():
    return json.dumps(gpustats, sort_keys=True)

@app.route('/api/ping', methods=[ 'POST'])
def ping():
    body = 0
    if request.method == 'POST':
        data=request.json
        data = request.get_data()
        data = json.loads(data.decode())
        if not data.get('ip'):
            body = 1
        else:
            gpustats[data['host']] = data
    return str(body)

def main():
    
    app.run(host='0.0.0.0', port=int(config['lab']['center']['port']))


if __name__ == '__main__':
    main()
