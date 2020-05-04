import json

def get_ration_to_cloud():

    ratio_to_cloud = 0
    with open('record.json') as json_file:
        data = json.load(json_file)
        data_youtube = data["state1_youtube"]
        
        data_youtube_cloud = data_youtube[4]
        data_youtube_total = data_youtube[5]

        # calculate the ratio of the request which have been sent to the cloud
        request_to_cloud = data_youtube_cloud["request_number"]
        request_to_cloud = int(request_to_cloud)

        request_total = data_youtube_total["total_request_number"]
        request_total = int(request_total)
        
        ratio_to_cloud = (request_to_cloud / request_total) * 100

        # print("ration_to_cloud = %.2f" % ratio_to_cloud + "%")
    return ratio_to_cloud



