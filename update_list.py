import requests
import json


def update_list(hostip,service_port,_name,_port,_ip_address,_status):
    # params prepare
    hostip = hostip
    service_port = service_port

    # preapre the Pod's infomation 
    _name = _name
    _port = _port
    _ip_address = _ip_address
    _status = _status
    query = "/?name=" + _name + "&port=" + _port + "&ip_address=" + _ip_address + "&status=" + _status

    # prepare url
    url = "http://" + hostip + ":" + service_port + query

    payload = {}
    headers= {}
    # send the request
    response = requests.request("GET", url, headers=headers, data = payload)
    
    # return the result of the request
    if (response.status_code == 200):
        return True
    else:
        return False
    
def initial_list(hostip, service_port):
    # location of the server
    hostip = hostip
    service_port = service_port

    # build the initialization request
    query = "/?initial=true"

    # build the request url 
    url = "http://" + hostip + ":" + service_port + query

    payload = {}
    headers= {}
    # send the request
    response = requests.request("GET", url, headers=headers, data = payload)

    # catch the return status code
    if (response.status_code == 200):
        return True
    else:
        return False

def check_list(hostip, service_port):
    # location of the server
    hostip = hostip
    service_port = service_port

    # build the list check request
    query = "/?check=true"

    # build the request url 
    url = "http://" + hostip + ":" + service_port + query
    
    payload = {}
    headers= {}
    # send the request
    response = requests.request("GET", url, headers=headers, data = payload)

    # catch the return status code
    if (response.status_code == 200):
        return response.content
    else:
        return False
