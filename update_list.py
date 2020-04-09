import requests

def update_list(hostip,port,_name,_port,_ip_address,_status):
    # params prepare
    hostip = "http://localhost"
    port = "3002"
    _name = "youtube_1"
    _port = "10086"
    _ip_address = "1.1.1.1"
    _status = "true"
    query = "/?name=" + _name + "&port=" + _port + "&ip_address=" + _ip_address + "&status=" + _status

    # prepare url
    url = hostip + ":" + port + query

    payload = {}
    headers= {}
    # send the request
    response = requests.request("GET", url, headers=headers, data = payload)
    
    # return the result of the request
    if (response.status_code == 200):
        return True
    else:
        return False
    

# update_list("http://localhost","3002","youtube_1","10086","1.1.1.1","true")
