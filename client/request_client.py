import numpy as np
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
from threading import Thread
from random import randint
from scipy.stats import poisson

# content number must be multiple of 10
TOTAL_CONTENT_NUMBER = 60
# the duration of the video
SERVICE_DURATION = 60

# average number of events per interval for youtube
P_POISSON_YOUTUBE = 2

# average number of events per interval for netflix
P_POISSON_NETFLIX = 1

# each 1 second, the script will generate a new request to servers
REQUEST_INTERVALE = 5

YOUTUBE_SERVICE_PORT = "9999"
NETFLIX_SERVICE_PORT = "8888"

ZIPF_S = 0.8


def get_zipf_random():
    a = 1.7
    s = np.random.zipf(a, size=None)
    return s


def simulation_youtube(hostip, service_port, ID, generator_zipf):
    generator_zipf = generator_zipf
    opts = Options()
    opts.set_headless()
    # Operating in headless mode
    assert opts.headless is True, "headless has not been set yet"
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


def simulation_netflix(hostip, service_port, ID, generator_zipf):
    generator_zipf = generator_zipf
    opts = Options()
    opts.set_headless()
    # Operating in headless mode
    assert opts.headless is True, "headless has not been set yet"
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

def request_simulation_youtube(youtube_ip, ID, generator_zipf):
    simulation_youtube(youtube_ip, YOUTUBE_SERVICE_PORT, ID, generator_zipf)
    # number = generator_zipf.random_zipf_normalized_generator()
    # print("youtube test " + youtube_ip + "with number " + str(number))

def request_simulation_netflix(netflix_ip, ID, generator_zipf):
    simulation_netflix(netflix_ip, NETFLIX_SERVICE_PORT, ID, generator_zipf)
    # number = generator_zipf.random_zipf_normalized_generator()
    # print("netflix test " + netflix_ip + "with number " + str(number))

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

if __name__ == "__main__":

    # read the input info
    youtube_ip = sys.argv[1]
    netflix_ip = sys.argv[2]
    ID = sys.argv[3]

    # demand fun_zipf generator
    generator_zipf = fun_zipf.ZipfGenerator(ZIPF_S, TOTAL_CONTENT_NUMBER)

    # print request distribution
    zipf_list = generator_zipf.get_probability_list()
    request_graph(zipf_list, TOTAL_CONTENT_NUMBER)

    # set the log config and start time
    log_file = open('./log/request_running.log', 'a')
    sys.stdout = log_file
    start_time = time.time()

    # start requesting
    print("ID = " + str(sys.argv[1]) +
          "start time = %s seconds ---" % (start_time))
    simulation_id = 0
    while(True):
        print("simulation ID = " + str(simulation_id))
        simulation_id = simulation_id + 1
        # To Youtube
        # threading._start_new_thread(os.system, ("python3 ./client/request_client.py {} {} {}".format(YOUTUBE_SERVER_IP, NETFLIX_SERVER_IP,"001"),))
        YOUTUBE_POISSON_NUMBER = poisson.rvs(P_POISSON_YOUTUBE, size=1)[0]
        for i in range(YOUTUBE_POISSON_NUMBER):
            print("generate " + str(YOUTUBE_POISSON_NUMBER) + "-------")
            Thread(target=request_simulation_youtube, args=(
                youtube_ip, ID, generator_zipf)).start()

        # To Netflix
        # threading._start_new_thread(os.system, ("python3 ./client/request_client.py {} {} {}".format(YOUTUBE_SERVER_IP, NETFLIX_SERVER_IP,"001"),))
        NETFLIX_POISSON_NUMBER = poisson.rvs(P_POISSON_NETFLIX, size=1)[0]
        for i in range(NETFLIX_POISSON_NUMBER):
            print("generate " + str(NETFLIX_POISSON_NUMBER) + "-------")
            Thread(target=request_simulation_netflix, args=(
                netflix_ip, ID, generator_zipf)).start()

        time.sleep(REQUEST_INTERVALE)

        # check the existence of main simulation processe
        output = subprocess.check_output(
            "ps ax | grep CDN_deployment.py", shell=True)
        output = output.decode("utf-8")
        output_args = shlex.split(output)
        count = output_args.count("CDN_deployment.py")
        if(count > 2):
            continue
        else:
            # the main process has finished, so this process will be ended
            break
            # continue

    # output the finish info
    print("ID = " + str(sys.argv[1]) +
          "--- %s seconds ---" % (time.time() - start_time))
    # close the log file
    log_file.close()

# duration estimation : (SERVICE_TIME + SERVICE_TIME + REQUEST_INTERVALE + 15s) *  REQUEST_TIME
