import kubernetes_tools as tools
import time
import update_list as up
import json
from kubernetes import client, config, watch
from pick import pick

PORT_RESERVED = 8000
PORT_RESERVED_STRING = "8000"
# default value
YOUTUBE_SERVER_IP = "1.1.1.1"
YOUTUBE_SERVER_PORT = "3000"


IP_YOUTUBE_SERVER=""

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
    print("start")
    pod_ip_address =  tools.get_deployment_info(core_v1_api,deployment_name)
    YOUTUBE_SERVER_IP = pod_ip_address
    print(pod_ip_address)
    up.initial_list(YOUTUBE_SERVER_IP,YOUTUBE_SERVER_PORT)
                
def setUpVolume():
    tools.pv_create(core_v1_api,"volume_1")

def service_config():
    config.load_kube_config()
    core_v1_api = client.CoreV1Api()
    tools.service_youTube_create(core_v1_api, PORT_RESERVED)

def initial():
    
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
    youtube_list_initial(core_v1_api,"youtube-control")
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


def allocation_to_youtube_1():
    volume_name = "volume-claim-5"
    deployment_name = "youtube-3"
    # deployment object create
    deployment_youtube = tools.youTube_deployment_object_create(PORT_RESERVED,volume_name,deployment_name)
    # deploy
    tools.create_deployment(api_minikube,deployment_youtube)
    # update the pods list
    youtube_list_add_pod(core_v1_api,deployment_name)

    print("allocation_to_youtube_1")

def allocation_to_netflix_2():
    print("allocation_to_netflix")

def allocation_to_monitor():
    print()

def stop_service():
    config.load_kube_config()
    api_minikube = client.AppsV1Api()

    print("Deleting all the deployments ...")
    #delete all the deployments 
    tools.delete_all_deployments(api_minikube)
    print("Deleted")

def stream_monitor():
    # todo
    # download pods list from youtube server
    print("stream_monitor")

def simultaion():

    # We start with an initial allocation
    # 2 pods for YouYube, 3 pods for Netflix
    initial()
    
    # observation time
    time.sleep(10)
    stream_monitor()

    # We then perturb it: we remove one container to CP1 and give a container to CP2. 
    allocation_to_youtube_1()

    # For an observation window, we keep the system perturbed and we measure the miss stream
    # If the miss stream of the perturbed allocation has decreased, we accept the perturbation
    # i.e., we do not come back to the previous allocation.
    stream_monitor()

    # We redo the allocation
    allocation_to_netflix_2()
    stream_monitor()

    # stop
    stop_service()

if __name__ == '__main__':
    initial()