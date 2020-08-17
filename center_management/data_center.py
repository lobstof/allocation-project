import json
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import center_management.update_list as up
import asyncio
import time
import random


class data_center:

    def __init__(self,json_record_file,name_state_youtube,name_state_netflix,youtube_hostip,youtube_service_port,netflix_hostip,netflix_service_port):
        self.json_record_file = json_record_file
        self.name_state_youtube = name_state_youtube
        self.name_state_netflix = name_state_netflix

        self.ratio_list = [[0,0,0]]
        self.n_data_set = 0

        self.best_ratio_total = 100

        # server params
        self.youtube_hostip = youtube_hostip
        self.youtube_service_port = youtube_service_port
        self.netflix_hostip = netflix_hostip
        self.netflix_service_port = netflix_service_port

    # ratio_to_cloud_list[0] = ratio_youtube, ratio_to_cloud_list[1] = ratio_netflix, ratio_to_cloud_list[2] = ratio_total
    
    def get_local_request_ratio(self):
        matplotlib.use('Agg')
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
            if  ratio_to_cloud_total < self.best_ratio_total :
                self.best_ratio_total = ratio_to_cloud_total
            
            # return the total ratio to local
            return (100 - ratio_to_cloud_total)
        
    def result_graph(self):
        ratio_list = self.ratio_list
        # ratio_list[0] is intial value
        # ratio_list[i][youtube,netflix,total]    
        
        # print out Total request ratio to Cloud
        # select out the total flow ratio to Cloud
        total_ratio = []
        for i in range(len(ratio_list)):
            if i == 0:
                continue
            total_ratio.append(ratio_list[i][2])

        x_total = range(1,len(total_ratio)+1)
        y_total = total_ratio
        plt.plot(x_total,y_total)
        plt.title('Total Request Ratio To Cloud')
        plt.savefig('./log/request_ratio_total.png')
        plt.close()

        # print out Youtube request ratio to Cloud
        # select out the youtube flow ratio to Cloud
        youtube_ratio = []
        for i in range(len(ratio_list)):
            if i == 0:
                continue
            youtube_ratio.append(ratio_list[i][0])

        x_youtube = range(1,len(youtube_ratio)+1)
        y_youtube = youtube_ratio
        plt.plot(x_youtube,y_youtube)
        plt.title('YouTube Request Ratio To Cloud')
        plt.savefig('./log/request_ratio_youtube.png')
        plt.close()

        # print out Netflix request ratio to Cloud

        # select out the netflix flow ratio to Cloud
        netflix_ratio = []
        for i in range(len(ratio_list)):
            if i == 0:
                continue
            netflix_ratio.append(ratio_list[i][1])

        x_netflix = range(1,len(netflix_ratio)+1)
        y_netflix = netflix_ratio
        plt.plot(x_netflix,y_netflix)
        plt.title('Netflix Request Ratio To Cloud')
        plt.savefig('./log/request_ratio_netflix.png')
        plt.close()

        # request ratio all
        plt.plot(x_total,y_total)
        plt.plot(x_youtube,y_youtube)
        plt.plot(x_netflix,y_netflix)
        plt.title('Request Ratio To Cloud')
        plt.savefig('./log/request_ratio_all.png')
        plt.close()

        # convert the result data and operation records into JSON formal
        # and then transfer them to the file
        # data_list = self.ratio_list
        data_list = ratio_list

        file = open('./log/ratio_list_record.json', 'w')
        # for i in data_list:
        #     json_i = json.dumps(i)
        #     file.write(json_i+'\n')
        json_list = json.dumps(data_list)
        file.write(json_list)
        file.close()
       
    def stream_monitor(self):
        matplotlib.use('Agg')
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
            record_file.close()
            time.sleep(2)
        # print(data_with_title)

        # record ratio value to list
        ratio_to_local = self.get_local_request_ratio()
        return ratio_to_local




# data_center_instance = data_center("123","123","123","123","123","123","123")
# data_center_instance.result_graph()
