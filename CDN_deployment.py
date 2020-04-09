import kubernetes_tools as tools
import time
import update_list as up
from kubernetes import client, config, watch
from pick import pick

PORT_RESERVED = 8000

#load k8s config
config.load_kube_config()
#get api instance
api_minikube = client.AppsV1Api()
core_v1_api = client.CoreV1Api()

def setUpVolume():
    tools.pv_create(core_v1_api,"volume_1")

def service_config():
    config.load_kube_config()
    core_v1_api = client.CoreV1Api()
    tools.service_youTube_create(core_v1_api, PORT_RESERVED)

# set up the CP controller
# set up the service, export the contoller Pod to customers
# set up initial CP containers(one Pod per CP)
def initial():
    
    volume_name = "volume-claim-1"
    deployment_name = "youtube-1"
    # pvc create
    tools.pvc_create(core_v1_api,volume_name)

    # deploy CP service controller and CP container
    deployment_control_youtube = tools.youTube_control_deployment_object_create(PORT_RESERVED)
    deployment_pod1_youtube = tools.youTube_deployment_object_create(PORT_RESERVED,volume_name,deployment_name) 
    tools.create_deployment(api_minikube,deployment_control_youtube)
    tools.create_deployment(api_minikube,deployment_pod1_youtube)

    # get the deployments info 
    # ip_address, name, port


    # update the Pods list 
    # up.update_list()

    # create service
    tools.service_youTube_create(core_v1_api, PORT_RESERVED)

def delete_CDN():
    config.load_kube_config()
    api_minikube = client.AppsV1Api()

    print("Deleting all the deployments ...")
    #delete all the deployments 
    tools.delete_all_deployments(api_minikube)
    print("Deleted")

def list_add():
    # send the request
    # hostip,port,_name,_port,_ip_address,_status
    result = up.update_list("http://localhost",
                            "3002","youtube_1",
                            "10086","1.1.1.1","true")
    return result

def list_delete():
    # send the request
    # hostip,port,_name,_port,_ip_address,_status
    result = up.update_list("http://localhost",
                            "3002","youtube_1",
                            "10086","1.1.1.1","true")
                
    return result

def addPod():

    volume_name = "volume-claim-2"
    deployment_name = "youtube-2"
    # pvc create
    tools.pvc_create(core_v1_api,volume_name)
    # deploy the Pod with the volume
    deployment_pod2_youtube = tools.youTube_deployment_object_create(PORT_RESERVED,volume_name,deployment_name) 
    tools.create_deployment(api_minikube,deployment_pod2_youtube)
    
    # get the deployments info 
    # ip_address, name, port
    

    # update the Pods list 
    # up.update_list()
    return True

def deletePod():
    # update the list

    # retrive the Pod

    return True

def simultaion():
    # initial the project
    initial()
    time.sleep(20)
    # add one more Pod of Youtube CP
    addPod()
    time.sleep(20)

    # delete one Pod of Youtube CP
    deletePod()
    time.sleep(20)

    # end of the simulation
    # delete the entire project
    delete_CDN()
    time.sleep(20)

def test():
    # tools.pvc_create(core_v1_api,"volume-claim-1")

    # deployment_control_youtube = tools.youTube_control_deployment_object_create(PORT_RESERVED)
    # tools.create_deployment(api_minikube,deployment_control_youtube)
    addPod()
    # monut location
    # /var/empty

if __name__ == "__main__":
    # start_CDN()  
    # delete_CDN()
    # service_config()
    test()