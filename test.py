from decision_center import decision_center
import time

N_time = 3
SERVERING_DURATION = 6

decision_center_instance = decision_center(1,1)

for i in range (N_time):
    print("--------------------")
    print("initial number : youtube = " + str(decision_center_instance.deployed_youtube_available) + "  netflix = " + str(decision_center_instance.deployed_netflix_available))

    decision_dict = decision_center_instance.decision_generate()
    decision_object1 = list(decision_dict.keys())[0]
    decision_operation1 = list(decision_dict.values())[0]

    decision_object2 = list(decision_dict.keys())[1]
    decision_operation2 = list(decision_dict.values())[1]

    if decision_operation1 == "add":
        # k8s_automation_tool_instance.deploy_one_pod(decision_object)
        print("add 1 " + decision_object1)
    elif decision_operation1 == "delete":
        # k8s_automation_tool_instance.delete_one_pod(decision_object)
        print("delete 1 " + decision_object1)
    else:
        # something wrong
        continue
    
    if decision_operation2 == "add":
        # k8s_automation_tool_instance.deploy_one_pod(decision_object)
        print("add 1 " + decision_object2)
    elif decision_operation2 == "delete":
        # k8s_automation_tool_instance.delete_one_pod(decision_object)
        print("delete 1 " + decision_object2)
    else:
        # something wrong
        continue


    print("after number : youtube = " + str(decision_center_instance.deployed_youtube_available) + "  netflix = " + str(decision_center_instance.deployed_netflix_available))
    print("--------------------")
    # serving time
    time.sleep(SERVERING_DURATION)
    # monitoring
    # control_center_instance.stream_monitor()
    # time.sleep(3)