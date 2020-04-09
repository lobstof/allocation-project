import requests


hostip = "localhost"
port = "3002"
_name = "cloud"
_port = "8000"
_ip_address = "172.17.0.11"
_status = "true"
query = "/?name=" + _name + "&port=" + _port + "&ip_address=" + _ip_address + "&status=" + _status

url = "http://" + hostip + ":" + port + query

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))