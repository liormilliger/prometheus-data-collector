from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Environment Variables
prometheus_url = "http://prometheus:9090/api/v1/"

mem_usage = "query?query=node_memory_MemTotal_bytes - node_memory_MemFree_bytes"
cpu_usage = "query?query=100 - (avg(irate(node_cpu_seconds_total{mode='idle'}[5m])) by (instance) * 100)"
disk_status = "query?query=node_filesystem_size_bytes{fstype!~'tmpfs|squashfs'} - node_filesystem_free_bytes{fstype!~'tmpfs|squashfs'}"

 
# mem_usage_query = "query?query=node_memory_MemTotal_bytes+-+node_memory_MemFree_bytes"
# disk_usage_query = "query?query=node_filesystem_size_bytes%7Bfstype%21%7E%27tmpfs%7Csquashfs%27%7D+-+node_filesystem_free_bytes%7Bfstype%21%7E%27tmpfs%7Csquashfs%27%7D"
# cpu_usage_query = "query?query=100+-+%28avg%28irate%28node_cpu_seconds_total%7Bmode%3D%27idle%27%7D%5B5m%5D%29%29+by+%28instance%29+*+100%29"
@app.route('/', methods=['GET'])
def welcome():
    return render_template('index.html')

@app.route('/system-data', methods=['GET'])
def prometheus_service():
    response = requests.get(prometheus_url + cpu_usage)
    data = response.json()
    if data["status"] == "success":
        cpu_value = round(float(data["data"]["result"][0]["value"][1]), 2)

        # Creating JSON response
        response_data = {
            # 'memory_usage': mem_usage,
            # 'disk_status': disk_status,
            'cpu_usage': cpu_value

        }

        return jsonify(response_data)
    else:
        return jsonify({"error": "Failed to retrieve system data from Prometheus"}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
