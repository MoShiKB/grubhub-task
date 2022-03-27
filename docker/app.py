from flask import Flask, render_template
import json
import os
from prometheus_client import Counter, generate_latest
from templates.pods import get_pods
from templates.ip import get_ip

app = Flask(__name__)

view_metric = Counter('view', 'Pods', ['env'])

try:
    env = os.environ['env']
except:
    env = ""
    print("No environment variable named env")


@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/pods',methods=['GET'])
def pods():
    view_metric.labels(env=env).inc()
    return str(get_pods())

@app.route('/metrics',methods=['GET'])
def metrics():
    return generate_latest()

@app.route('/me',methods=['GET'])
def characters():
    return get_ip(), 200

@app.route('/health')
def health():
    if env != "":
        return json.dumps({"OK": env}), 200
    else:
        return ("ERROR"), 503

def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    main()
