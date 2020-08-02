import k8s_tools.kubernetes_tools as tools
import time
import center_management.update_list as up
import json
from kubernetes import client, config, watch
# from pick import pick
import os
import threading
from center_management.data_center import data_center
from k8s_tools.k8s_automation_tool import k8s_automation_tool
from center_management.q_learning_decision import q_learning_decision_center

PORT_RESERVED = 8000
PORT_RESERVED_STRING = "8000"
# default value
YOUTUBE_SERVER_IP = "172.17.0.6"
YOUTUBE_SERVER_PORT = "3000"

NETFLIX_SERVER_IP = "172.17.0.7"
NETFLIX_SERVER_PORT = "2000"

FILEPATH_STATE_TEMP = "log/state_record_temp.json"


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
    
    #prepare youtube and netflix redirection server
    print(1)
    # youtube redirection server, netflix redirection server. Objects creation 
    deployment_youtube_server = tools.youTube_control_deployment_object_create(PORT_RESERVED)    
    deployment_netflix_server = tools.netflix_control_deployment_object_create(PORT_RESERVED)

    # deploy the created objects
    tools.create_deployment(api_minikube,deployment_youtube_server)
    tools.create_deployment(api_minikube,deployment_netflix_server)    
    time.sleep(8)
    print(2)

    # youtube redirection server list initial
    youtube_list_initial(core_v1_api,"youtube-control")
    print("YOUTUBE_SERVER_IP = " + YOUTUBE_SERVER_IP)
    time.sleep(4)

    # netflix redirection server list initial
    netflix_list_initial(core_v1_api,"netflix-control")
    print("NETFLIX_SERVER_IP = " + NETFLIX_SERVER_IP)
    time.sleep(4)

    # set up the volumes
    # pvc config
    list_volume_name = ["volume-claim-1","volume-claim-2","volume-claim-3",
                        "volume-claim-4","volume-claim-5","volume-claim-6",
                        "volume-claim-7","volume-claim-8","volume-claim-9",
                        "volume-claim-10",]

    # volume pool preapre 
    k8s_automation_tool_instance = k8s_automation_tool(core_v1_api,api_minikube,
                                        list_volume_name,YOUTUBE_SERVER_IP,
                                        YOUTUBE_SERVER_PORT,NETFLIX_SERVER_IP,
                                        NETFLIX_SERVER_PORT)
    time.sleep(4)

    # preapre cdn pods of for youtube_cloud and netflix cloud

    # youtube-cloud
    deployment_name_youtube_cloud = "youtube-cloud"
    deployment_youtube_cloud = tools.youTube_deployment_object_create(PORT_RESERVED,
                                                                k8s_automation_tool_instance.volume_request(deployment_name_youtube_cloud),
                                                                deployment_name_youtube_cloud)
    tools.create_deployment(api_minikube,deployment_youtube_cloud)
    time.sleep(5)
    # update the youtube server's list
    youtube_list_add_pod(core_v1_api,deployment_name_youtube_cloud)


    # netflix-cloud
    deployment_name_netflix_cloud = "netflix-cloud"
    deployment_netflix_cloud = tools.netflix_deployment_object_create(PORT_RESERVED,
                                                                k8s_automation_tool_instance.volume_request(deployment_name_netflix_cloud),
                                                                deployment_name_netflix_cloud)
    tools.create_deployment(api_minikube,deployment_netflix_cloud)
    time.sleep(5)
    # update the netflix server's list
    netflix_list_add_pod(core_v1_api,deployment_name_netflix_cloud)

    # deploy inital cdn pods 
    # we are going to deploy one youtube-container(youtube-1) and one netflix-container(netflix-1)
    k8s_automation_tool_instance.deploy_one_pod("youtube",0,"initial","add 1 youtube")
    k8s_automation_tool_instance.deploy_one_pod("netflix",10,"initial","add one 1 netflix")

    return k8s_automation_tool_instance

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

    print("deleting all the deployments ...")
    #delete all the deployments 
    tools.delete_all_deployments(api_minikube)
    print("deployments Deleted")

    print("deleting all the pvcs")
    tools.delete_all_pvcs()
    print("pvcs deleted")

def simultaion():

    # We start with an initial allocation
    # 1 pod for YouYube, 1 pod for Netflix
    k8s_automation_tool_instance = initial()
    print("initialization finished")

    # demande an instance of controle_center
    data_center_instance = data_center(FILEPATH_STATE_TEMP,"state_youtube",
                                            "state_netflix",YOUTUBE_SERVER_IP,
                                            YOUTUBE_SERVER_PORT,NETFLIX_SERVER_IP,
                                            NETFLIX_SERVER_PORT)
    print("serving ...")

    # pass the youtube, netflix server IP address and ID of client  
    threading._start_new_thread(os.system, ("python ./client/request_client.py {} {} {}".format(YOUTUBE_SERVER_IP, NETFLIX_SERVER_IP,"001"),))
    time.sleep(150)

    # monitoring 
    data_center_instance.stream_monitor()
    # time.sleep(3)

    # re-allocation loop
    # re-allocation time
    # until now, we have one normal youtube cdn container and one normal netflix cdn container
    # decision_center_instance = decision_center(1,1)
    
    # model parms 
    # N_PODS_TOTAL -- the total pods that we can deploy (the max volume amount)
    # EPSILON -- greedy police
    # ALPHA -- learning rate
    # GAMMA --discount factor
    # initial deployment is 1 youtube pod, 1 netflix pod
    q_learning_decision_center_instance = q_learning_decision_center(real_time_state=11)

    N_time = 50
    MONITORING_DURATION = 150
    for loop_time in range (N_time):
        # decision_dict = decision_center_instance.decision_generate()
        print("state now (k8s automation): ")
        print(str(len(k8s_automation_tool_instance.youtube_deployed_name_list)) 
              + str(len(k8s_automation_tool_instance.netflix_deployed_name_list)))
        print(q_learning_decision_center_instance.real_time_state)
        decision_dict = q_learning_decision_center_instance.action_generate()

        # state check k8s_automation.state and q_learning_decision.state
        k8s_automation_tool_instance.state_check(q_learning_decision_center_instance.real_time_state)

        decision_object1 = list(decision_dict.keys())[0]
        decision_operation1 = list(decision_dict.values())[0]

        decision_object2 = list(decision_dict.keys())[1]
        decision_operation2 = list(decision_dict.values())[1]

        # interval numero i
        # print the actions taken 
        
        # wait the re-allcoation
        # update the server's list 
        # delete one pod

        if decision_operation1 == "add":
            k8s_automation_tool_instance.deploy_one_pod(decision_object1,q_learning_decision_center_instance.real_time_state,loop_time,decision_dict)
        elif decision_operation1 == "delete":
            k8s_automation_tool_instance.delete_one_pod(decision_object1,q_learning_decision_center_instance.real_time_state,loop_time,decision_dict)
        elif decision_operation1 == "still":
            print("Youtube deployment stay still")
        else :
            print("something wrong .... y")
            exit()

        if decision_operation2 == "add":
            k8s_automation_tool_instance.deploy_one_pod(decision_object2,q_learning_decision_center_instance.real_time_state,loop_time,decision_dict)
        elif decision_operation2 == "delete":
            k8s_automation_tool_instance.delete_one_pod(decision_object2,q_learning_decision_center_instance.real_time_state,loop_time,decision_dict)
        elif decision_operation2 == "still":
            print("Netflix deployment stay still")
        else:
            print("something wrong .... n")
            exit()
        
        # refresh the server's counter
        up.resetcounter_list(YOUTUBE_SERVER_IP, YOUTUBE_SERVER_PORT)
        up.resetcounter_list(NETFLIX_SERVER_IP, NETFLIX_SERVER_PORT)

        # serving time
        time.sleep(MONITORING_DURATION)
        # monitoring
        ratio_to_local = data_center_instance.stream_monitor()
        print("ratio_to_local = " + str(ratio_to_local))

        # update the q_learning table by ENV_return_value -> ratio to local
        q_learning_decision_center_instance.rl_by_step(ratio_to_local,loop_time)
        # time.sleep(3)

    data_center_instance.result_graph()
    print(q_learning_decision_center_instance.state_list)

    # recoding data
    q_learning_decision_center_instance.data_record()
    q_learning_decision_center_instance.q_table.to_csv("q_table.csv", sep='\t')


if __name__ == '__main__':
    # initial()
    simultaion()
    # stop_service()
  