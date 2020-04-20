# This project is prepared for the demonstrate that 
# it's possible for a python server to control 
# kubernetes cluster

# api doc:
# https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md
# https://pypi.org/project/kubernetes-py/1.5.6.6/

import time
from kubernetes import client, config, watch
from pick import pick

# PersistentVolume
def pv_create(core_v1_api,pv_name):
    core_v1_api = core_v1_api
    body = client.V1PersistentVolume(
        api_version="v1",
        kind="PersistentVolume",
        metadata=client.V1ObjectMeta(
            name=pv_name,
            labels={"key" : "localpvs"}
        ),
        spec=client.V1PersistentVolumeSpec(
            capacity={"storage" : "0.5Gi"},
            volume_mode="Filesystem",
            access_modes=["ReadWriteOnce"],
            persistent_volume_reclaim_policy= "Recycle",
            local={"path" : "/home/damu/Documents/kubernet/project/CDN_project/volumes/{_name}".format(_name=pv_name)},
            node_affinity=client.V1VolumeNodeAffinity(
                          required=client.V1NodeSelector(
                          [client.V1NodeSelectorTerm(
                          match_expressions=[
                          client.V1NodeSelectorRequirement(
                          key="kubernetes.io/hostname",
                          operator="In",
                          values=["minikube"])])])
                        )
        )
    )
    core_v1_api.create_persistent_volume(body=body)
    # local={"path" : "/home/damu/Documents/kubernet/project/CDN_project/volumes/{_name}".format(_name=pv_name)},
    # print(local[0])

# PersistentVolumeClaims
def pvc_create(core_v1_api,pvc_name):
    core_v1_api = core_v1_api
    body = client.V1PersistentVolumeClaim(
        api_version="v1",
        kind="PersistentVolumeClaim",
        metadata=client.V1ObjectMeta(
            name=pvc_name
        ),
        spec=client.V1PersistentVolumeClaimSpec(
            access_modes=["ReadWriteOnce"],
            volume_mode="Filesystem",
            resources=client.V1ResourceRequirements
                      (requests={"storage" : "0.5Gi"}),
            # volume_name=pv_name
            selector=client.V1LabelSelector(match_labels={"key" : "localpvs"})
        )
    )
    core_v1_api.create_namespaced_persistent_volume_claim(namespace="default", body=body)
    print(pvc_name + "created ---")

def service_youTube_create(core_v1_api,PORT_RESERVED):
    core_v1_api = core_v1_api
    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name="service-youtube-control",
            labels={"app": "youtube-control"}
        ),
        spec=client.V1ServiceSpec(
            type="NodePort",
            selector={"app": "youtube-control"},
            ports=[client.V1ServicePort(
                port=8080,
                target_port=PORT_RESERVED,
                protocol="TCP"
            )]
        )
    )
    # Creation of the Deployment in specified namespace
    # (Can replace "default" with a namespace you may have created)
    core_v1_api.create_namespaced_service(namespace="default", body=body)

def youTube_control_deployment_object_create(port_allocated):
    
    # define container
    container = client.V1Container(
        name="youtube-control",
        image="youtube-server",
        image_pull_policy="Never",
        ports=[client.V1ContainerPort(container_port=port_allocated)])

    # define template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"youtube-control": "youtube-control"}),
        spec=client.V1PodSpec(containers=[container]))

    # define spec 
    spec = client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={'matchLabels': {'youtube-control': 'youtube-control'}})
    
    # Instantiate the deployment object
    deployment_object = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="youtube-control"),
        spec=spec)
    
    return deployment_object

def youTube_deployment_object_create(port_allocated,pvc_name,deployment_name):

    # define container
    container = client.V1Container(
        name="youtube",
        image="cdnyoutube",
        # we use the local image on docker
        image_pull_policy="Never",
        ports=[client.V1ContainerPort(container_port=port_allocated)],
        volume_mounts=[client.V1VolumeMount(
                      mount_path="/var/empty",
                      name="mypd")])

    # define template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={deployment_name: deployment_name}),
        spec=client.V1PodSpec(containers=[container],
                              volumes=[client.V1Volume(
                              name="mypd",
                              persistent_volume_claim=
                              client.V1PersistentVolumeClaimVolumeSource(
                                  claim_name=pvc_name))],
                              hostname=deployment_name))

    # define spec 
    spec = client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={'matchLabels': {deployment_name: deployment_name}})
    
    # Instantiate the deployment object
    deployment_object = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=deployment_name),
        spec=spec)
    
    return deployment_object

def netflix_control_deployment_object_create(port_allocated):
    
    # define container
    container = client.V1Container(
        name="netflix-control",
        image="youtube-server",
        image_pull_policy="Never",
        ports=[client.V1ContainerPort(container_port=port_allocated)])

    # define template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"netflix-control": "netflix-control"}),
        spec=client.V1PodSpec(containers=[container]))

    # define spec 
    spec = client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={'matchLabels': {'netflix-control': 'netflix-control'}})
    
    # Instantiate the deployment object
    deployment_object = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="netflix-control"),
        spec=spec)
    
    return deployment_object

def netflix_deployment_object_create(port_allocated,pvc_name,deployment_name):

    # define container
    container = client.V1Container(
        name="netflix",
        # we impose the same image for netflix service
        image="cdnyoutube",
        # we use the local image on docker
        image_pull_policy="Never",
        ports=[client.V1ContainerPort(container_port=port_allocated)],
        volume_mounts=[client.V1VolumeMount(
                      mount_path="/var/empty",
                      name="mypd")])

    # define template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={deployment_name: deployment_name}),
        spec=client.V1PodSpec(containers=[container],
                              volumes=[client.V1Volume(
                              name="mypd",
                              persistent_volume_claim=
                              client.V1PersistentVolumeClaimVolumeSource(
                                  claim_name=pvc_name))],
                              hostname=deployment_name))

    # define spec 
    spec = client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={'matchLabels': {deployment_name: deployment_name}})
    
    # Instantiate the deployment object
    deployment_object = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=deployment_name),
        spec=spec)
    
    return deployment_object

def create_deployment(api_instance, deployment):
    # Create deployement
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace="default")
    print("Deployment created. status='%s'" % str(api_response.status))
    # TODO
    # need to verify if the deployment already exists

def delete_deployment(api_instance, name_deployment):
    # Delete deployment
    api_response = api_instance.delete_namespaced_deployment(
        name=name_deployment,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Deployment deleted. status='%s'" % str(api_response.status))

def update_replicas_deployment(api_instance, deployment, amount, deployment_name):
    # Update container image
    # deployment.spec.template.spec.containers[0].image = "nginx:1.16.0"
    
    # Update the deployment
    deployment.spec.replicas = amount

    # push the changes
    api_response = api_instance.patch_namespaced_deployment(
        name= deployment_name,
        namespace="default",
        body=deployment,
        )
    
    print("Deployment updated. status='%s'" % str(api_response.status))

def event_monitoring():
    config.load_kube_config()
    api_minikube_core = client.CoreV1Api()
    # count = 40
    w = watch.Watch()
    for event in w.stream(api_minikube_core.list_namespace, timeout_seconds=10):
        print("Event: %s %s" % (event['type'], event['object'].metadata.name))
        # count -= 1
        #if not count:
          #  w.stop()
    print("Finished namespace stream.")
    
    for event in w.stream(api_minikube_core.list_pod_for_all_namespaces, timeout_seconds=10):
        print("Event: %s %s %s" % (
            event['type'],
            event['object'].kind,
            event['object'].metadata.name)
        )
        #count -= 1
       #if not count:
           # w.stop()
    print("Finished pod stream.")

# get pods name with their there ip address 
def get_pods_list():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_namespaced_pod("default", watch=False)
    pods = {}
    for item in ret.items:
        print(
            "%s\t%s\t%s" %
            (item.status.pod_ip,
             item.metadata.namespace,
             item.metadata.name))
        pods.update({item.metadata.name: item.status.pod_ip})
    print(pods)

# return a dict of deployments under the namespace "default"
def get_deployment_list():
    config.load_kube_config()
    api_minikube = client.AppsV1Api()
    print("Listing deployments")
    thead = api_minikube.list_namespaced_deployment("default",async_req=True)
    deployments = []
    ret = thead.get()
    
    for item in ret.items:
        print(
            "%s\t%s" %
            (item.metadata.namespace,
             item.metadata.name))
        deployments.append(item.metadata.name)
    print("------------")
    # print(deployments)

    # return the deployments
    return deployments

def get_deployment_info(core_v1_api, deployment_name):
    # use "for" to wait the info
    for i in range(1,10):
        data = core_v1_api.list_namespaced_pod("default",label_selector = deployment_name)
        pod_ip_address = data.items[0].status.pod_ip
        if pod_ip_address is None:
            print(str(i) + "time, try later")
            time.sleep(2)
        else :
            print("read sucessfully")
            break
        if i == 10:
            print("Can't find the pod:" + deployment_name)
            return ""    
    return pod_ip_address


def delete_all_deployments(api_instance):
    deployments = get_deployment_list()
    for item in deployments:
        delete_deployment(api_instance,item)

def test():
    config.load_kube_config()
    api_minikube = client.AppsV1Api()
    delete_all_deployments(api_minikube)
