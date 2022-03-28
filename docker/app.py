from flask import Flask, render_template
import json
import os
from prometheus_client import Counter, generate_latest
from templates.pods import get_pods
from templates.ip import get_ip

app = Flask(__name__)

# Counter for prometheus
view_metric = Counter('view', 'Pods', ['env'])

# Try to get env, else enter empty string to var
try:
    env = os.environ['env']
except:
    env = ""
    print("No environment variable named env")


@app.route('/')
def hello():
    return 'Hello Grubhub!'

# Getting Pods
@app.route('/pods',methods=['GET'])
def pods():
    # Increasing metrics each connection
    view_metric.labels(env=env).inc()
    return str(get_pods())

@app.route('/metrics',methods=['GET'])
def metrics():
    # Generate prometheus metrics page
    return generate_latest()

# Getting IP of container
@app.route('/me',methods=['GET'])
def characters():
    return get_ip(), 200

# Health check for the application
@app.route('/health')
def health():
    if env != "":
        return json.dumps({"OK": env}), 200
    else:
        return ("ERROR"), 503

# Run Command
def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    main()
