import kubernetes_tools as tools
from kubernetes import client, config, watch
import time
import update_list as up

PORT_RESERVED = 8000
PORT_RESERVED_STRING = "8000"


class k8s_automation_tool:
    def __init__(self,core_v1_api,api_minikube,list_volume_name,youtube_hostip,youtube_service_port,netflix_hostip,netflix_service_port):
        self.core_v1_api = core_v1_api
        self.api_minikube = api_minikube
        self.list_volume_name = list_volume_name
        self.volume_availabel_pool = []
        # dict to record allocated volume with its host pod_name
        self.volume_pod_paire = {}

        self.youtube_deployed_name_list = []
        self.netflix_deployed_name_list = []

        # youtube, netflix server info
        self.youtube_hostip = youtube_hostip
        self.youtube_service_port = youtube_service_port
        self.netflix_hostip = netflix_hostip
        self.netflix_service_port = netflix_service_port
        
        # ceration of pvc according to the list_volume_name
        for volume in self.list_volume_name:
            # create the pvc of the volume
            tools.pvc_create(self.core_v1_api,volume)
            # import this new volume into volume_availabel_pool
            self.volume_availabel_pool.append(volume)
    
    def youtube_list_add_pod(self,deployment_name):
        # youtube server
        hostip = self.youtube_hostip
        host_port = self.youtube_service_port

        # get this.pod ip address
        pod_ip_address =  tools.get_deployment_info(self.core_v1_api,deployment_name)
        pod_name = deployment_name
        pod_status = "true"
        pod_port = PORT_RESERVED_STRING

        up.update_list(hostip,host_port,pod_name,pod_port,pod_ip_address,pod_status)

    def youtube_list_delete_pod(self,deployment_name):
        # youtube server
        hostip = self.youtube_hostip
        host_port = self.youtube_service_port

        # get this.pod ip address
        pod_ip_address = "1.1.1.1"
        pod_name = deployment_name
        pod_status = "false"
        pod_port = PORT_RESERVED_STRING

        up.update_list(hostip,host_port,pod_name,pod_port,pod_ip_address,pod_status)


    def netflix_list_add_pod(self,deployment_name):
        # netflix server
        hostip = self.netflix_hostip
        host_port = self.netflix_service_port

        # get this.pod ip address
        pod_ip_address =  tools.get_deployment_info(self.core_v1_api,deployment_name)
        pod_name = deployment_name
        pod_status = "true"
        pod_port = PORT_RESERVED_STRING

        up.update_list(hostip,host_port,pod_name,pod_port,pod_ip_address,pod_status)

    def netflix_list_delete_pod(self,deployment_name):
        # netflix server
        hostip = self.netflix_hostip
        host_port = self.netflix_service_port

        # get this.pod ip address
        pod_ip_address = "1.1.1.1"
        pod_name = deployment_name
        pod_status = "false"
        pod_port = PORT_RESERVED_STRING

        up.update_list(hostip,host_port,pod_name,pod_port,pod_ip_address,pod_status)


    def volume_request(self,pod_name):
        if len(self.volume_availabel_pool) < 1:
            # there is no more volume available
            print("there is no more volume available")
            return False
        else:
            # pop a available pvc from volume 
            volume_picked = self.volume_availabel_pool.pop()
            print(volume_picked)
            # record allocation info into volume_pod_paire list
            self.volume_pod_paire.update({pod_name : volume_picked})
            return volume_picked
    
    def volume_return(self, pod_name):
        # pop this paire from the dict volume_pod_paire
        volume_to_return = self.volume_pod_paire.pop(pod_name)
        # add this colume_returned to volume_available_pool 
        self.volume_availabel_pool.append(volume_to_return)
    


    # cdn_name = youtube or netflix
    def deploy_one_pod(self,cdn_name):
        # we are going to deploy youtube cdn pod
        if cdn_name == "youtube":
            # we name each pod by its order
            pod_tag = len(self.youtube_deployed_name_list)

            # we can only allocate up to 5 pods (including cloud pod)
            if pod_tag >= 5:
                return False
            
            pod_name = "youtube-" + str(pod_tag+1)
            
            volume_name = self.volume_request(pod_name)
            if volume_name == False:
                # there is no more volume, pod creation failed
                return False
            temp_deployment_object = tools.youTube_deployment_object_create(
                                        PORT_RESERVED,
                                        volume_name,
                                        pod_name)
            # deploy the deployment object
            tools.create_deployment(self.api_minikube,temp_deployment_object)
            # wating deployement finished
            time.sleep(5)
            print("deplotment : " + pod_name + " deployed")

            # youtube-* created successfully 
            # add this new deployment to the pods list
            self.youtube_deployed_name_list.append(pod_name)

            # update the pod list of the youtube_server
            self.youtube_list_add_pod(pod_name)
            time.sleep(1)
            return True

        else:
            # we are going to deploy netflix cdn pod
            # we name this pod by its order
            pod_tag = len(self.netflix_deployed_name_list)

            # we can only allocate up to 5 pods (including cloud pod)
            if pod_tag >= 5:
                return False

            pod_name = "netflix-" + str(pod_tag+1)
            
            volume_name = self.volume_request(pod_name)
            if volume_name == False:
                # there is no more volume, pod creation failed
                return False
            temp_deployment_object = tools.netflix_deployment_object_create(
                                        PORT_RESERVED,
                                        volume_name,
                                        pod_name)

            # deploy the deployment object
            tools.create_deployment(self.api_minikube,temp_deployment_object)
            # wating deployement finished
            time.sleep(5)
            print("deplotment : " + pod_name + " deployed")

            # netflix-* created successfully 
            # add this new deployment to the pods list
            self.netflix_deployed_name_list.append(pod_name)

            # update the pod list of the netflix_server
            self.netflix_list_add_pod(pod_name)
            time.sleep(1)
            return True
    
    def delete_one_pod(self,cdn_name):
        if cdn_name == "youtube":
            # we are going to delete the latest added pod

            if len(self.youtube_deployed_name_list) < 1:
                # there is no more pod existed
                # we can't delete cloud pod
                return False

            pod_name = self.youtube_deployed_name_list.pop()

            # delete the pod
            tools.delete_deployment(self.api_minikube, pod_name)
            time.sleep(5)

            # give the volume back
            self.volume_return(pod_name)

            # update youtube server list
            self.youtube_list_delete_pod(pod_name)
            time.sleep(1)
            print("deplotment : " + pod_name + " deleted")

            return True

        else:
            # cdn_name = netflix
            # we are going to delete the latest added pod

            if len(self.netflix_deployed_name_list) < 1:
                # there is no more pod existed
                # we can't delete cloud pod
                return False

            pod_name = self.netflix_deployed_name_list.pop()

            # delete the pod
            tools.delete_deployment(self.api_minikube, pod_name)
            time.sleep(5)

            # give the volume back
            self.volume_return(pod_name)

            # update youtube server list
            self.netflix_list_delete_pod(pod_name)
            time.sleep(1)
            print("deplotment : " + pod_name + " deleted")

            return True
            

    
# self,core_v1_api,api_minikube,list_volume_name,youtube_hostip,youtube_service_port,netflix_hostip,netflix_service_port

def test_code():
    #load k8s config
    config.load_kube_config()
    #get api instance
    api_minikube = client.AppsV1Api()
    core_v1_api = client.CoreV1Api()

    # list_volume_name = ["volume-claim-1","volume-claim-2"]

    list_volume_name = ["volume-claim-1","volume-claim-2","volume-claim-3",
                            "volume-claim-4","volume-claim-5"]

    # list_volume_name = ["volume-claim-1","volume-claim-2","volume-claim-3",
    #                         "volume-claim-4","volume-claim-5","volume-claim-6",
    #                         "volume-claim-7","volume-claim-8","volume-claim-9",
    #                         "volume-claim-10"]

    youtube_hostip = "192.168.5.140"
    youtube_service_port = "3000"
    netflix_hostip = "192.168.5.140"
    netflix_service_port = "2000"

    # initial the lists of two servers 
    up.initial_list(youtube_hostip,youtube_service_port)
    up.initial_list(netflix_hostip,netflix_service_port)


    # volume pool preapre 
    k8s_automation_tool_instance = k8s_automation_tool(core_v1_api,api_minikube,
                                        list_volume_name,youtube_hostip,
                                        youtube_service_port,netflix_hostip,
                                        netflix_service_port)


    # chanmps test
    print("volume_availabel_pool :")
    print(k8s_automation_tool_instance.volume_availabel_pool)

    # deploying 
    k8s_automation_tool_instance.deploy_one_pod("youtube")
    k8s_automation_tool_instance.deploy_one_pod("youtube")
    k8s_automation_tool_instance.deploy_one_pod("netflix")
    k8s_automation_tool_instance.deploy_one_pod("youtube")
    # k8s_automation_tool_instance.deploy_one_pod("youtube")



    print("youtube deployed")
    print(k8s_automation_tool_instance.youtube_deployed_name_list)

    print("netflix deployed")
    print(k8s_automation_tool_instance.netflix_deployed_name_list)

    print("volume_pod_paire")
    print(k8s_automation_tool_instance.volume_pod_paire)


    # modification
    result1 = k8s_automation_tool_instance.delete_one_pod("netflix")
    print("result1 = " + str(result1))

    result2= k8s_automation_tool_instance.delete_one_pod("youtube")
    print("result2 = " + str(result2))

    print("youtube deployed")
    print(k8s_automation_tool_instance.youtube_deployed_name_list)

    print("netflix deployed")
    print(k8s_automation_tool_instance.netflix_deployed_name_list)

    print("volume_pod_paire")
    print(k8s_automation_tool_instance.volume_pod_paire)



