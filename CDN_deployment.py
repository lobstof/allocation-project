import kubernetes_tools as tools
import time
import update_list as up
import json
from kubernetes import client, config, watch
from pick import pick
import os
import threading
from control_center import control_center
from volume_pool import volume_pool

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
    list_volume_name = ["volume-claim-1","volume-claim-2","volume-claim-3",
                        "volume-claim-4","volume-claim-5","volume-claim-6",
                        "volume-claim-7","volume-claim-8","volume-claim-9",
                        "volume-claim-10",]

    # instance of volume_pool, pvc creation
    volume_pool_instance = volume_pool(core_v1_api,list_volume_name)
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
    deployment_youtube_1 = tools.youTube_deployment_object_create(PORT_RESERVED,
                                                                volume_pool_instance.volume_request(deployment_name_youtube_1),
                                                                deployment_name_youtube_1)
    deployment_youtube_2 = tools.youTube_deployment_object_create(PORT_RESERVED,
                                                                volume_pool_instance.volume_request(deployment_name_youtube_2),
                                                                deployment_name_youtube_2)
    deployment_youtube_cloud = tools.youTube_deployment_object_create(PORT_RESERVED,
                                                                volume_pool_instance.volume_request(deployment_name_youtube_cloud),
                                                                deployment_name_youtube_cloud)

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
    deployment_netflix_1 = tools.netflix_deployment_object_create(PORT_RESERVED,
                                                                volume_pool_instance.volume_request(deployment_name_netflix_1),
                                                                deployment_name_netflix_1)
    deployment_netflix_2 = tools.netflix_deployment_object_create(PORT_RESERVED,
                                                                volume_pool_instance.volume_request(deployment_name_netflix_2),
                                                                deployment_name_netflix_2)
    deployment_netflix_cloud = tools.netflix_deployment_object_create(PORT_RESERVED,
                                                                volume_pool_instance.volume_request(deployment_name_netflix_cloud),
                                                                deployment_name_netflix_cloud)

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

def stop_service():
    config.load_kube_config()
    api_minikube = client.AppsV1Api()

    print("Deleting all the deployments ...")
    #delete all the deployments 
    tools.delete_all_deployments(api_minikube)
    print("Deleted")

def simultaion():

    # We start with an initial allocation
    # 2 pods for YouYube, 3 pods for Netflix
    initial()
    print("initialization finish")

    # demande an instance of controle_center
    control_center_instance = control_center("record.json","state_youtube",
                                            "state_netflix",YOUTUBE_SERVER_IP,
                                            YOUTUBE_SERVER_PORT,NETFLIX_SERVER_IP,
                                            NETFLIX_SERVER_PORT)
    print("serving ...")

    # start 15 cleint request simulation instances 
    # pass the youtube, netflix server IP address and ID of client  
    threading._start_new_thread(os.system, ("python3 ./client/request_client.py {} {} {}".format(YOUTUBE_SERVER_IP, NETFLIX_SERVER_IP,"001"),))

    time.sleep(10)
    # monitoring 
    control_center_instance.stream_monitor()
    time.sleep(3)
    control_center_instance.get_ratio_to_cloud()
    
    # We then perturb it: we remove one container to CP1 and give a container to CP2.
    de_allocation_to_netflix_2()
    time.sleep(5)
    allocation_to_youtube_3()

    print("serving ...")
    time.sleep(10)
    # monitoring 
    control_center_instance.stream_monitor()
    time.sleep(3)
    control_center_instance.get_ratio_to_cloud()

    control_center_instance.result_graph()

if __name__ == '__main__':
    initial()
    # simultaion()
    # stop_service()
    # test2() 


# preapre volume pool 

# random request 
# preapre generator of allocation strategy 

# update control center, result_graph, 
# add graph of zipf distribution 
# 
# # start simulation 
# 
# 
# 
# make request waiting time to randome (distribution exponentiel) 