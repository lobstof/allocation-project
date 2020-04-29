import kubernetes_tools as tools
import time
import update_list as up
import json
from kubernetes import client, config, watch
from pick import pick
import os
import threading

PORT_RESERVED = 8000
PORT_RESERVED_STRING = "8000"
# default value
YOUTUBE_SERVER_IP = "172.17.0.6"
YOUTUBE_SERVER_PORT = "3000"

NETFLIX_SERVER_IP = "172.17.0.7"
NETFLIX_SERVER_PORT = "2000"

FILEPATH = "record.json"


#load k8s config
config.load_kube_config()
#get api instance
api_minikube = client.AppsV1Api()
core_v1_api = client.CoreV1Api()

def youtube_list_add_pod(core_v1_api,deployment_name):

    # youtube server
    hostip = YOUTUBE_SERVER_IP
    host_port = YOUTUBE_SERVER_PORT

    # get this.pod ip address
    pod_ip_address =  tools.get_deployment_info(core_v1_api,deployment_name)
    pod_name = deployment_name
    pod_status = "true"
    pod_port = PORT_RESERVED_STRING

    up.update_list(hostip,host_port,pod_name,pod_port,pod_ip_address,pod_status)

def youtube_list_delete_pod(deployment_name):
    # youtube server
    hostip = YOUTUBE_SERVER_IP
    host_port = YOUTUBE_SERVER_PORT

    # get this.pod ip address
    pod_ip_address = "1.1.1.1"
    pod_name = deployment_name
    pod_status = "false"
    pod_port = PORT_RESERVED_STRING

    up.update_list(hostip,host_port,pod_name,pod_port,pod_ip_address,pod_status)

def youtube_list_initial(core_v1_api,deployment_name):
    # config youtube server ip
    global YOUTUBE_SERVER_IP
    print("YOUTUBE_SERVER_IP" + "start")
    pod_ip_address =  tools.get_deployment_info(core_v1_api,deployment_name)
    YOUTUBE_SERVER_IP = pod_ip_address
    print("YOUTUBE_SERVER_IP" + " pod_ip_address:" + pod_ip_address)
    up.initial_list(YOUTUBE_SERVER_IP,YOUTUBE_SERVER_PORT)

def netflix_list_initial(core_v1_api,deployment_name):
    # config netflix server ip
    global NETFLIX_SERVER_IP
    print("NETFLIX_SERVER_IP" + "start")
    pod_ip_address =  tools.get_deployment_info(core_v1_api,deployment_name)
    NETFLIX_SERVER_IP = pod_ip_address
    print("NETFLIX_SERVER_IP" + " pod_ip_address:" + pod_ip_address)
    up.initial_list(NETFLIX_SERVER_IP,NETFLIX_SERVER_PORT)

def netflix_list_delete_pod(deployment_name):
    # netflix server
    hostip = NETFLIX_SERVER_IP
    host_port = NETFLIX_SERVER_PORT

    # get this.pod ip address
    pod_ip_address = "1.1.1.1"
    pod_name = deployment_name
    pod_status = "false"
    pod_port = PORT_RESERVED_STRING

    up.update_list(hostip,host_port,pod_name,pod_port,pod_ip_address,pod_status)

def netflix_list_add_pod(core_v1_api,deployment_name):
    # netflix server
    hostip = NETFLIX_SERVER_IP
    host_port = NETFLIX_SERVER_PORT

    # get this.pod ip address
    pod_ip_address =  tools.get_deployment_info(core_v1_api,deployment_name)
    pod_name = deployment_name
    pod_status = "true"
    pod_port = PORT_RESERVED_STRING

    up.update_list(hostip,host_port,pod_name,pod_port,pod_ip_address,pod_status)

def service_config():
    config.load_kube_config()
    core_v1_api = client.CoreV1Api()
    tools.service_youTube_create(core_v1_api, PORT_RESERVED)

def initial():
    
    # todo clean all the existing pods, service, pv and pvc

    # set up the volumes
    # pvc config
    volume_name_1 = "volume-claim-1"
    volume_name_2 = "volume-claim-2"
    volume_name_3 = "volume-claim-3"
    volume_name_4 = "volume-claim-4"
    volume_name_5 = "volume-claim-5"
    volume_name_cloud_youtube = "volume-claim-cloud-youtube"
    volume_name_cloud_netflix = "volume-claim-cloud-netflix"

    # # pvc create
    # tools.pvc_create(core_v1_api,volume_name_1)
    # tools.pvc_create(core_v1_api,volume_name_2)
    # tools.pvc_create(core_v1_api,volume_name_3)
    # tools.pvc_create(core_v1_api,volume_name_4)
    # tools.pvc_create(core_v1_api,volume_name_5)
    # tools.pvc_create(core_v1_api,volume_name_cloud_youtube)
    # tools.pvc_create(core_v1_api,volume_name_cloud_netflix)
    time.sleep(8)

    # youtube control server, netflix control serveR
    deployment_youtube_server = tools.youTube_control_deployment_object_create(PORT_RESERVED)    
    deployment_netflix_server = tools.netflix_control_deployment_object_create(PORT_RESERVED)

    # deploy two servers
    tools.create_deployment(api_minikube,deployment_youtube_server)
    tools.create_deployment(api_minikube,deployment_netflix_server)    
    time.sleep(8)

    # youtube server list initial
    youtube_list_initial(core_v1_api,"youtube-control")
    print("YOUTUBE_SERVER_IP = " + YOUTUBE_SERVER_IP)
    time.sleep(4)

    # netflix server list initial
    netflix_list_initial(core_v1_api,"netflix-control")
    print("NETFLIX_SERVER_IP = " + NETFLIX_SERVER_IP)
    time.sleep(4)

    # 2 local youtube containers with one cloud youtube server container
    deployment_name_youtube_1 = "youtube-1"
    deployment_name_youtube_2 = "youtube-2"
    deployment_name_youtube_cloud = "youtube-cloud"

    # youtube deployments
    deployment_youtube_1 = tools.youTube_deployment_object_create(PORT_RESERVED,volume_name_1,deployment_name_youtube_1)
    deployment_youtube_2 = tools.youTube_deployment_object_create(PORT_RESERVED,volume_name_2,deployment_name_youtube_2)
    deployment_youtube_cloud = tools.youTube_deployment_object_create(PORT_RESERVED,volume_name_cloud_youtube,deployment_name_youtube_cloud)

    # deploy the youtube deployments and update the pod's list after the creation
    tools.create_deployment(api_minikube,deployment_youtube_1)
    time.sleep(5)
    youtube_list_add_pod(core_v1_api,deployment_name_youtube_1)

    tools.create_deployment(api_minikube,deployment_youtube_2)
    time.sleep(5)
    youtube_list_add_pod(core_v1_api,deployment_name_youtube_2)

    tools.create_deployment(api_minikube,deployment_youtube_cloud)
    time.sleep(5)
    youtube_list_add_pod(core_v1_api,deployment_name_youtube_cloud)

    # 2 local netflix containers with one cloud netflix server container
    deployment_name_netflix_1 = "netflix-1"
    deployment_name_netflix_2 = "netflix-2"
    deployment_name_netflix_cloud = "netflix-cloud"

    # netflix deployments
    deployment_netflix_1 = tools.netflix_deployment_object_create(PORT_RESERVED,volume_name_3,deployment_name_netflix_1)
    deployment_netflix_2 = tools.netflix_deployment_object_create(PORT_RESERVED,volume_name_4,deployment_name_netflix_2)
    deployment_netflix_cloud = tools.netflix_deployment_object_create(PORT_RESERVED,volume_name_cloud_netflix,deployment_name_netflix_cloud)

    # deploy the netflix deployments and update the pod's list after the creation
    tools.create_deployment(api_minikube,deployment_netflix_1)
    time.sleep(5)
    netflix_list_add_pod(core_v1_api,deployment_name_netflix_1)

    tools.create_deployment(api_minikube,deployment_netflix_2)
    time.sleep(5)
    netflix_list_add_pod(core_v1_api,deployment_name_netflix_2)

    tools.create_deployment(api_minikube,deployment_netflix_cloud)
    time.sleep(5)
    netflix_list_add_pod(core_v1_api,deployment_name_netflix_cloud)

def initial_try_server():
    # todo clean all the existing pods, service, pv and pvc

    # pvc config
    volume_name_1 = "volume-claim-1"
    volume_name_2 = "volume-claim-2"
    volume_name_3 = "volume-claim-3"
    volume_name_4 = "volume-claim-4"
    volume_name_5 = "volume-claim-5"
    volume_name_cloud = "volume-claim-cloud"

    # pvc create
    tools.pvc_create(core_v1_api,volume_name_1)
    tools.pvc_create(core_v1_api,volume_name_2)
    tools.pvc_create(core_v1_api,volume_name_3)
    tools.pvc_create(core_v1_api,volume_name_4)
    tools.pvc_create(core_v1_api,volume_name_5)
    tools.pvc_create(core_v1_api,volume_name_cloud)
    
    time.sleep(5)

    # youtube control server, netflix control serveR
    deployment_youtube_server = tools.youTube_control_deployment_object_create(PORT_RESERVED)    
    # deployment_netflix_server = tools.netflix_control_deployment_object_create(PORT_RESERVED)

    # deploy two servers
    tools.create_deployment(api_minikube,deployment_youtube_server)
    # tools.create_deployment(api_minikube,deployment_netflix_server)    
    time.sleep(5)

    # youtube server list initial
    # youtube_list_initial(core_v1_api,"youtube-control")
    global YOUTUBE_SERVER_IP
    YOUTUBE_SERVER_IP = "192.168.5.140"
    print("YOUTUBE_SERVER_IP = " + YOUTUBE_SERVER_IP)
    time.sleep(5)

    # 2 local youtube containers with one cloud youtube server container
    deployment_name_youtube_1 = "youtube-1"
    deployment_name_youtube_2 = "youtube-2"
    deployment_name_youtube_cloud = "youtube-cloud"

    # youtube deployments
    deployment_youtube_1 = tools.youTube_deployment_object_create(PORT_RESERVED,volume_name_1,deployment_name_youtube_1)
    deployment_youtube_2 = tools.youTube_deployment_object_create(PORT_RESERVED,volume_name_2,deployment_name_youtube_2)
    deployment_youtube_cloud = tools.youTube_deployment_object_create(PORT_RESERVED,volume_name_cloud,deployment_name_youtube_cloud)

    # deploy the youtube deployments and update the pod's list after the creation
    tools.create_deployment(api_minikube,deployment_youtube_1)
    time.sleep(5)
    youtube_list_add_pod(core_v1_api,deployment_name_youtube_1)

    tools.create_deployment(api_minikube,deployment_youtube_2)
    time.sleep(5)
    youtube_list_add_pod(core_v1_api,deployment_name_youtube_2)

    tools.create_deployment(api_minikube,deployment_youtube_cloud)
    time.sleep(5)
    youtube_list_add_pod(core_v1_api,deployment_name_youtube_cloud)

def allocation_to_youtube_3():
    volume_name = "volume-claim-5"
    deployment_name = "youtube-3"
    # deployment object create
    deployment_youtube = tools.youTube_deployment_object_create(PORT_RESERVED,volume_name,deployment_name)
    # deploy
    tools.create_deployment(api_minikube,deployment_youtube)
    time.sleep(5)
    # update the pods list
    youtube_list_add_pod(core_v1_api,deployment_name)
    print("allocation_to_youtube_1")

def de_allocation_to_netflix_2():
    name_deployment = "netflix-2"
    # delete
    tools.delete_deployment(api_minikube,name_deployment)
    time.sleep(5)
    # update the pods list
    netflix_list_delete_pod(name_deployment)
    print("delete netflix allocation:" + name_deployment)

def allocation_to_monitor():
    print()

def stop_service():
    config.load_kube_config()
    api_minikube = client.AppsV1Api()

    print("Deleting all the deployments ...")
    #delete all the deployments 
    tools.delete_all_deployments(api_minikube)
    print("Deleted")

def stream_monitor(hostip, service_port):
    # todo
    # download pods list from youtube server
    print("stream_monitor")
    context = up.check_list(hostip, service_port)
    record_json = json.loads(context)

    print(json.dumps(record_json))
    print("................")

    return record_json

def simultaion():

    # load record file 
    file_record = open(FILEPATH, "a")

    # We start with an initial allocation
    # 2 pods for YouYube, 3 pods for Netflix
    initial()
    print("initialization finish")
    print("waiting ...")
    time.sleep(5)
    # start cleint request simulation
    # pass the youtube and netflix server IP address 
    threading._start_new_thread(os.system, ("sh ./client/simulation.sh {} {}".format(YOUTUBE_SERVER_IP, NETFLIX_SERVER_IP),))

    time.sleep(2000)
    # observe the two pods list
    log1 = stream_monitor(YOUTUBE_SERVER_IP, YOUTUBE_SERVER_PORT)
    file_record.write("state1_youtube")
    file_record.write(json.dumps(log1))
    
    log2 = stream_monitor(NETFLIX_SERVER_IP, NETFLIX_SERVER_PORT)
    file_record.write("state1_netflix")
    file_record.write(json.dumps(log2))

    time.sleep(5) 
    

    # We then perturb it: we remove one container to CP1 and give a container to CP2.
    de_allocation_to_netflix_2()
    time.sleep(5)
    allocation_to_youtube_3()
    print("waiting ...")
    time.sleep(2000) 

    # observe the two pods list
    log3 = stream_monitor(YOUTUBE_SERVER_IP, YOUTUBE_SERVER_PORT)
    file_record.write("state2_youtube")
    file_record.write(json.dumps(log3))

    log4 = stream_monitor(NETFLIX_SERVER_IP, NETFLIX_SERVER_PORT)
    file_record.write("state2_netflix")
    file_record.write(json.dumps(log4))
    
    file_record.close()

    # time.sleep(5)

    # time.sleep(100)
    # # stop
    # stop_service()

def test():
    volume_name_1 = "volume-claim-1"

    # 2 local youtube containers with one cloud youtube server container
    deployment_name_netflix_1 = "netflix-1"
 
    # youtube deployments
    deployment_netflix_1 = tools.netflix_deployment_object_create(PORT_RESERVED,volume_name_1,deployment_name_netflix_1)

    # deploy the youtube deployments and update the pod's list after the creation
    tools.create_deployment(api_minikube,deployment_netflix_1)

def test2():
    # file = open(FILEPATH,"a")

    x =  '{ "organization":"GeeksForGeeks", "city":"Noida", "country":"India"}'
    y =  {"organization2":"GeeksForGeeks2"}
    x = json.loads(x)
    print(json.dumps(x))    
    x.update(y)

    # file.write(json.dumps(z)+json.dumps(y))
    print(json.dumps(x))    
    # file.close()

if __name__ == '__main__':
    # initial()
    simultaion()
    # stop_service()
    # test2() 
