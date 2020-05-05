import json
import matplotlib.pyplot as plt
import update_list as up


class control_center:

    def __init__(self,json_record_file,name_state_youtube,name_state_netflix,youtube_hostip,youtube_service_port,netflix_hostip,netflix_service_port):
        self.json_record_file = json_record_file
        self.name_state_youtube = name_state_youtube
        self.name_state_netflix = name_state_netflix

        self.ratio_list = []
        self.n_data_set = 0

        self.best_ratio_total = 50

        # server params
        self.youtube_hostip = youtube_hostip
        self.youtube_service_port = youtube_service_port
        self.netflix_hostip = netflix_hostip
        self.netflix_service_port = netflix_service_port

    # ratio_to_cloud_list[0] = ratio_youtube, ratio_to_cloud_list[1] = ratio_netflix, ratio_to_cloud_list[2] = ratio_total
    def get_ratio_to_cloud(self):

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
        plt.title('ratio_request')
        plt.show()
        # plt.savefig('../log/ratio_request.png')


    
    def stream_monitor(self):

        # youtube
        print("stream_monitor_youtube")
        context_youtube = up.check_list(self.youtube_hostip, self.youtube_service_port)
        record_json_youtube = json.load(context_youtube)


        # netflix
        print("stream_monitor_netflix")
        context_netflix = up.check_list(self.netflix_hostip, self.netflix_service_port)
        record_json_netflix = json.load(context_netflix)

        data_with_title = {self.name_state_youtube : record_json_youtube, self.name_state_netflix : record_json_netflix}
        
        with open(self.json_record_file, "w") as record_file:
            record_file.write(json.dumps(data_with_title))
    
# control_center_instance = control_center("record_json_data_test.json","state_youtube","state_netflix","1","2","3","4")

# control_center_instance.get_ratio_to_cloud()
# control_center_instance.get_ratio_to_cloud()
# control_center_instance.get_ratio_to_cloud()

# control_center_instance.result_graph()


