from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
import time
import sys 
import fun_zipf
import matplotlib.pyplot as plt
import subprocess
import shlex
import random 

from random import randint
# content number must be multiple of 10
TOTAL_CONTENT_NUMBER = 60
# the duration of the video
SERVICE_DURATION = 40

# each 1 second, the script will generate a new request to servers
WAIT_DURATION = 1

YOUTUBE_SERVICE_PORT = "9999"
NETFLIX_SERVICE_PORT = "8888"

ZIPF_S = 0.4

import numpy as np

def get_zipf_random():
    a = 1.7
    s = np.random.zipf(a, size=None)
    return s

def simulation_youtube(hostip, service_port, ID,generator_zipf):
    generator_zipf = generator_zipf
    opts = Options()
    opts.set_headless()
    assert opts.headless is True, "headless has not been set yet"# Operating in headless mode
    browser = Chrome(options=opts)
    
    hostip = hostip
    service_port = service_port
    # query1

    number = generator_zipf.random_zipf_normalized_generator()
    query = "/?number=" + str(number)
    print("ID = " + ID + "  number = %d" % number + "--youtube")
    url = "http://" + hostip + ":" + service_port + query
    browser.get(url)
    # ..
    sleep(SERVICE_DURATION)
    print("ID = " + ID + "end: " + str(number) + "--youtube")
    browser.close()

# simulation youtube
def simulation_netflix(hostip, service_port, ID,generator_zipf):
    generator_zipf = generator_zipf
    opts = Options()
    opts.set_headless()
    assert opts.headless is True, "headless has not been set yet"# Operating in headless mode
    browser = Chrome(options=opts)
    
    hostip = hostip
    service_port = service_port
    # query1

    number = generator_zipf.random_zipf_normalized_generator()
    query = "/?number=" + str(number)
    print("ID = " + ID + "  number = %d" % number + "--netflix")
    url = "http://" + hostip + ":" + service_port + query
    browser.get(url)
    sleep(SERVICE_DURATION)
    print("ID = " + ID + "end: " + str(number) + "--netflix")
    browser.close()

def request_simulation(youtube_ip,netflix_ip,ID,generator_zipf):
    # 70 percent to request youtube, 30 percent to request netflix
    i = random.randint(1,10)
    if i <= 7 :
        simulation_youtube(youtube_ip,YOUTUBE_SERVICE_PORT,ID,generator_zipf)
    else:
        simulation_netflix(netflix_ip,NETFLIX_SERVICE_PORT,ID,generator_zipf)

def request_graph(zipf_list, N):
    left = list(range((int(N/10))))
    zipf_list = zipf_list

    height = []
    tick_label = []
    # prepare bar
    for j in range((int(N/10))):
        temp = 0
        for i in range(j*10,(j+1)*10):
            temp = temp + zipf_list[i]
        height.append(temp)
        tick_label.append("container-{}".format(str(j+1)))
    plt.bar(left, height, tick_label = tick_label,
            width=0.4)
    # plt.show()
    plt.title('request_distribution')
    plt.savefig('../log/request_distribution.png')
    
if __name__ == "__main__":

    # read the input info
    youtube_ip = sys.argv[1]
    netflix_ip = sys.argv[2]
    ID = sys.argv[3]


    # demand fun_zipf generator 
    generator_zipf = fun_zipf.ZipfGenerator(ZIPF_S,TOTAL_CONTENT_NUMBER)
    
    # print request distribution
    zipf_list = generator_zipf.get_probability_list()
    request_graph(zipf_list, TOTAL_CONTENT_NUMBER)

    # set the log config and start time
    log_file = open('../log/request_running.log', 'a')
    sys.stdout = log_file
    start_time = time.time()

    # start requesting 
    print("ID = "+ str(sys.argv[1]) + "start time = %s seconds ---" % (start_time))
    while(True):
        # threading._start_new_thread(os.system, ("python3 ./client/request_client.py {} {} {}".format(YOUTUBE_SERVER_IP, NETFLIX_SERVER_IP,"001"),))
        request_simulation(youtube_ip,netflix_ip,ID,generator_zipf)
        
        # https://www.themathcitadel.com/poisson-processes-and-data-loss/
        # todo, make WAIT_DURATION a random value 
        time.sleep(WAIT_DURATION)

        # check the existence of main simulation processe
        output = subprocess.check_output("ps ax | grep CDN_de...py", shell=True)
        output = output.decode("utf-8")
        output_args = shlex.split(output)
        count = output_args.count("graph_test.py")
        if(count == 2):
            # the main process has finished, so this process will be ended too
            break

    # output the finish info
    print("ID = "+ str(sys.argv[1]) + "--- %s seconds ---" % (time.time() - start_time))
    # close the log file
    log_file.close()

# duration estimation : (SERVICE_TIME + SERVICE_TIME + WAIT_DURATION + 15s) *  REQUEST_TIME