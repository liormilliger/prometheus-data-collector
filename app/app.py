from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Environment Variables
prometheus_url = "http://prometheus:9090/api/v1/"

mem_usage = "query?query=node_memory_Active_bytes/node_memory_MemTotal_bytes*100"
cpu_usage = "query?query=(sum by (cpu)(rate(node_cpu_seconds_total{mode!='idle'}[5m]))*100)"
disk_status = "query?query=(node_filesystem_avail_bytes/node_filesystem_size_bytes)*100"

@app.route('/', methods=['GET'])
def prometheus_service():
    # Logic for CPU Data
    cpu_response = requests.get(prometheus_url + cpu_usage)
    cpu_data = cpu_response.json()
    if cpu_data["status"] == "success":
        cpu_value = cpu_data["data"]["result"][0]["value"][1]
    else:
        cpu_value = "ERROR: Failed to retrieve system data from Prometheus"
    # Logic for Memory Data
    mem_response = requests.get(prometheus_url + mem_usage)
    mem_data = mem_response.json()
    if mem_data["status"] == "success":
        mem_value = mem_data["data"]["result"][0]["value"][1]
    else:
        mem_value = "ERROR: Failed to retrieve system data from Prometheus"

    # Logic for Diskspace Data
    disk_response = requests.get(prometheus_url + disk_status)
    disk_data = disk_response.json()
    if disk_data["status"] == "success":
        disk_value = disk_data["data"]["result"][0]["value"][1]
    else:
        disk_value = "ERROR: Failed to retrieve system data from Prometheus"

    # Creating JSON response
    response_data = {
        'memory_usage': f'{float(mem_value):.2f}%',
        'used_disk_space': f'{float(disk_value):.2f}%',
        'cpu_usage': f'{float(cpu_value)*100:.2f}% of CPU is in use'
        }

    return jsonify(response_data)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
