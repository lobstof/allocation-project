import json
import matplotlib.pyplot as plt
import update_list as up
import asyncio
import time
import random

import kubernetes
import kubernetes_tools




class control_center:

    def __init__(self,json_record_file,name_state_youtube,name_state_netflix,youtube_hostip,youtube_service_port,netflix_hostip,netflix_service_port):
        self.json_record_file = json_record_file
        self.name_state_youtube = name_state_youtube
        self.name_state_netflix = name_state_netflix

        self.ratio_list = []
        self.n_data_set = 0

        self.best_ratio_total = 100

        # server params
        self.youtube_hostip = youtube_hostip
        self.youtube_service_port = youtube_service_port
        self.netflix_hostip = netflix_hostip
        self.netflix_service_port = netflix_service_port

    # ratio_to_cloud_list[0] = ratio_youtube, ratio_to_cloud_list[1] = ratio_netflix, ratio_to_cloud_list[2] = ratio_total
    def get_ratio_to_local(self):

        ratio_to_cloud_list = []
        with open(self.json_record_file) as json_file:
            
            data = json.load(json_file)

            # youtube 
            data_youtube = data[self.name_state_youtube]
            
            data_youtube_cloud = data_youtube[4]
            data_youtube_total = data_youtube[5]

            # calculate the ratio of the request which have been sent to the cloud
            request_to_cloud_youtube = int(data_youtube_cloud["request_number"])
            request_total_youtube = int(data_youtube_total["total_request_number"])
            
            ratio_to_cloud_youtube = (request_to_cloud_youtube / request_total_youtube) * 100
            ratio_to_cloud_list.append(ratio_to_cloud_youtube)

            # netflix 
            data_netflix = data[self.name_state_netflix]

            data_netflix_cloud = data_netflix[4]
            data_netflix_total = data_netflix[5]

            # calculate the ratio of the request which have been sent to the cloud
            request_to_cloud_netflix = int(data_netflix_cloud["request_number"])
            request_total_netflix = int(data_netflix_total["total_request_number"])

            ratio_to_cloud_netflix = (request_to_cloud_netflix/request_total_netflix) * 100
            ratio_to_cloud_list.append(ratio_to_cloud_netflix)

            ratio_to_cloud_total = (request_to_cloud_youtube + request_to_cloud_netflix) / (request_total_youtube + request_total_netflix) * 100
            ratio_to_cloud_list.append(ratio_to_cloud_total)
            
            self.ratio_list.append(ratio_to_cloud_list)
            self.n_data_set = self.n_data_set + 1

            # update the best_ratio_total
            # if  ratio_to_cloud_total < self.best_ratio_total :
            #     self.best_ratio_total = ratio_to_cloud_total
            #     return True
            # else:
            #     return False


            # update the best_ratio_total
            if  ratio_to_cloud_total < self.best_ratio_total :
                self.best_ratio_total = ratio_to_cloud_total
            
            # return the total ratio to local
            return (1 - ratio_to_cloud_total)
        
    def result_graph(self):

        # number of data set
        n_data_set = self.n_data_set
        ratio_list = self.ratio_list

        # abscissa
        left = []
        tick_label = []

        # number of data set equals to n
        for j in range(n_data_set):
            temp1 = 1 + 4*j
            temp1_tick_label = "r_y" 
            
            temp2 = 2 + 4*j
            temp2_tick_label = "r_n"
            
            temp3 = 3 + 4*j
            temp3_tick_label = "r_total"

            left.append(temp1)
            left.append(temp2)
            left.append(temp3)

            tick_label.append(temp1_tick_label)
            tick_label.append(temp2_tick_label)
            tick_label.append(temp3_tick_label)
        
        # ordinate
        height = []
        for i in range(n_data_set):
            height = height + ratio_list[i]
    
        plt.bar(left, height, tick_label = tick_label,
                width=0.4)
        plt.title('ratio_request' + '   the lowest ratio = ' + str(self.best_ratio_total))
        # plt.show()
        # attach a random number to result's name (as a tag)
        ran_tag = str(random.randint(1,999))
        plt.savefig('./log/ratio_request{}.png'.format(ran_tag))

        # todo convert the result data and operation records into JSON formal
        # and then transfer them to the file
        
        # data_log_file = open('./log/ratio_request_raw_data{}.txt'.format(ran_tag),'w')
        # data_log_file.write(ratio_list)
        # data_log_file.close()
        # also we need to record the raw data
        
        

    
    def stream_monitor(self):

        # youtube
        print("stream_monitor_youtube")
        context_youtube = up.check_list(self.youtube_hostip, self.youtube_service_port)
        context_youtube = context_youtube.decode("utf-8")
        record_json_youtube = json.loads(context_youtube)

        # netflix
        print("stream_monitor_netflix")
        context_netflix = up.check_list(self.netflix_hostip, self.netflix_service_port)
        context_netflix = context_netflix.decode("utf-8")
        record_json_netflix = json.loads(context_netflix)

        data_with_title = {self.name_state_youtube : record_json_youtube, self.name_state_netflix : record_json_netflix}
        
        with open(self.json_record_file, "w") as record_file:
            record_file.write(json.dumps(data_with_title))
        # print(data_with_title)

        # record ratio value to list
        ratio_to_local = self.get_ratio_to_local()
        return ratio_to_local


# todo refresh the lists of netflix server and youtube server 





# control_center_instance = control_center("record_json_data_test.json","state_youtube","state_netflix","localhost","3000","localhost","2000")

# we will get a result value which indicates if this allocation is better or not 
# print(control_center_instance.stream_monitor())

# 
# control_center_instance.get_ratio_to_local()
# control_center_instance.get_ratio_to_local()



# control_center_instance.result_graph()


