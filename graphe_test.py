import threading
import time
import os
from scipy.stats import poisson
import client.fun_zipf
import matplotlib.pyplot as plt

ZIPF_S = 0.8
TOTAL_CONTENT_NUMBER = 60

# YOUTUBE_SERVER_IP = "youtube"
# NETFLIX_SERVER_IP = "netflix"

# print("1")
# threading._start_new_thread(os.system, ("python ./client/request_client.py {} {} {}".format(YOUTUBE_SERVER_IP, NETFLIX_SERVER_IP,"001"),))
# print("2")
# time.sleep(30)

# logfile = open("./log/test_log.log",'a')
# loop_number = 4
# number = "input 1 "
# number2 = "input 2"

# logfile.write('\n' + "This is the " + str(loop_number) + "loop:" + '\n')
# logfile.write(number + "test 1")
# logfile.write(number2 + "test 2")

# logfile.write('\n' + "This is the " + str(loop_number) + "loop:" + '\n')
# logfile.write(number + "test 1")
# logfile.write(number2 + "test 2")

# logfile.write('\n' + "This is the " + str(loop_number) + "loop:" + '\n')
# logfile.write(number + "test 1")
# logfile.write(number2 + "test 2")

# logfile.close()

# count = 0
# P_POISSON_NETFLIX = 2
# for i in range(30):
#     if(poisson.rvs(P_POISSON_NETFLIX, size=1)[0] == 0):
#         count = count +1 
# print(count)

def request_graph(zipf_list, N):
    left = list(range((int(N/10))))
    zipf_list = zipf_list

    height = []
    tick_label = []
    # prepare bar
    for j in range((int(N/10))):
        temp = 0
        for i in range(j*10, (j+1)*10):
            temp = temp + zipf_list[i]
        height.append(temp)
        tick_label.append("container-{}".format(str(j+1)))
    plt.bar(left, height, tick_label=tick_label,
            width=0.4)
    # plt.show()
    plt.title('request_distribution')
    plt.savefig('./log/request_distribution.png')
    print("Distribution Graph generated")


# generator_zipf = client.fun_zipf.ZipfGenerator(ZIPF_S, TOTAL_CONTENT_NUMBER)
# # print request distribution
# zipf_list = generator_zipf.get_probability_list()
# request_graph(zipf_list, TOTAL_CONTENT_NUMBER)

time.sleep(30)