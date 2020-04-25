from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randint
TOTAL_NUMBER = 50
ID = randint(0,10000)

import numpy as np

def get_zipf_random():
    a = 1.7
    s = np.random.zipf(a, size=None)
    return s


# simulation youtube
def simulation_test_youtube(hostip, service_port, number1, number2, number3, number4):
    for i in range(2):
        # disable the UI
        opts = Options()
        opts.set_headless()
        assert opts.headless is True, "headless has not been set yet"# Operating in headless mode
        browser1 = Chrome(options=opts)
        browser2 = Chrome(options=opts)
        browser3 = Chrome(options=opts)
        browser4 = Chrome(options=opts)

        hostip = hostip
        service_port = service_port
        # query1
        query1 = "/?number=" + number1
        url1 = "http://" + hostip + ":" + service_port + query1
        browser1.get(url1)
        browser1.close()

        # query2
        query2 = "/?number=" + number2
        url2 = "http://" + hostip + ":" + service_port + query2
        browser2.get(url2)
        browser2.close()

        # query3
        query3 = "/?number=" + number3
        url3 = "http://" + hostip + ":" + service_port + query3
        browser3.get(url3)
        browser3.close()


        # query4
        query4 = "/?number=" + number4
        url4 = "http://" + hostip + ":" + service_port + query4
        browser4.get(url4)
        browser4.close()

        
        print("youtube: " + "%d" % (i+1))
        

# simulation youtube
def simulation_test_netflix(hostip, service_port, number1, number2):

    for i in range(2):
        # disable the UI
        opts = Options()
        opts.set_headless()
        assert opts.headless is True, "headless has not been set yet"# Operating in headless mode
        browser1 = Chrome(options=opts)
        browser2 = Chrome(options=opts)


        hostip = hostip
        service_port = service_port
        # query1
        query1 = "/?number=" + number1
        url1 = "http://" + hostip + ":" + service_port + query1
        browser1.get(url1)
        browser1.close()

        # query2
        query2 = "/?number=" + number2
        url2 = "http://" + hostip + ":" + service_port + query2
        browser2.get(url2)
        browser2.close()

        print("netflix: " + "%d" % (i+1))



def simulation_youtube(hostip, service_port):
   
    opts = Options()
    opts.set_headless()
    assert opts.headless is True, "headless has not been set yet"# Operating in headless mode
    browser = Chrome(options=opts)
    
    hostip = hostip
    service_port = service_port
    # query1

    number = randint(0,TOTAL_NUMBER)
    query = "/?number=" + str(number)
    print("ID = " + str(ID) + "  number = %d" % number + "--youtube")
    url = "http://" + hostip + ":" + service_port + query
    browser.get(url)
    sleep(20)
    print("ID = " + str(ID) + "end: " + str(number) "--youtube")
    browser.close()


# simulation youtube
def simulation_netflix(hostip, service_port):
    
    opts = Options()
    opts.set_headless()
    assert opts.headless is True, "headless has not been set yet"# Operating in headless mode
    browser = Chrome(options=opts)
    
    hostip = hostip
    service_port = service_port
    # query1

    number = randint(0,TOTAL_NUMBER)
    query = "/?number=" + str(number)
    print("ID = " + str(ID) + "  number = %d" % number + "netflix")
    url = "http://" + hostip + ":" + service_port + query
    browser.get(url)
    sleep(20)
    print("ID = " + str(ID) + "end: " + str(number) + "netflix")
    browser.close()


# simulation_test_youtube("172.17.0.10","9999","5","13","23","33")
# simulation_test_netflix("172.17.0.11","8888","5","13")

def request_simulation():
    
    for i in range(15):
        simulation_youtube("172.17.0.6","9999")
        simulation_netflix("172.17.0.7","8888")
        sleep(3)