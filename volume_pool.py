import kubernetes_tools as tools
from kubernetes import client, config, watch

class volume_pool:
    def __init__(self,core_v1_api,list_volume_name):
        self.core_v1_api = core_v1_api
        self.list_volume_name = list_volume_name
        self.volume_availabel_pool = []
        # dict to record allocated volume with its host pod_name
        self.volume_pod_paire = {}

        # ceration of pvc according to the list_volume_name
        for volume in self.list_volume_name:
            # create the pvc of the volume
            tools.pvc_create(self.core_v1_api,volume)
            # import this new volume into volume_availabel_pool
            self.volume_availabel_pool.append(volume)
    
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
        
# list_volume_name = ["volume-claim-1","volume-claim-2","volume-claim-3",
#                         "volume-claim-4","volume-claim-5","volume-claim-6",
#                         "volume-claim-7","volume-claim-8","volume-claim-9",
#                         "volume-claim-10",]
