import random


# this class is responsible for generating the random re_allocation decision
# todo renforcement learning 

class decision_center:
    def __init__(self,deployed_youtube_available,deployed_netflix_available):
        
        self.deployed_youtube_available = deployed_youtube_available
        self.deployed_netflix_available = deployed_netflix_available
    
    def youtube_add(self):
        self.deployed_youtube_available = self.deployed_youtube_available + 1
    
    def netflix_add(self):
        self.deployed_netflix_available = self.deployed_netflix_available + 1
    
    def youtube_delete(self):
        self.deployed_youtube_available = self.deployed_youtube_available - 1
    
    def netflix_delete(self):
        self.deployed_netflix_available = self.deployed_netflix_available - 1


    def decision_generate(self):
        dict_decision = {}
        # youtube 
        if self.deployed_youtube_available == 0:
            # we have to give one to youtube
            dict_decision.update({"youtube":"add"})
            self.youtube_add()

        elif self.deployed_youtube_available == 4:
            # we cant allocate more
            dict_decision.update({"youtube":"delete"})
            self.youtube_delete()
        
        else:
            # normal case
            tag = random.random()
            if tag < 0.5:
                dict_decision.update({"youtube":"delete"})
                self.youtube_delete()
            else:
                dict_decision.update({"youtube":"add"})
                self.youtube_add()

        # netflix 
        if self.deployed_netflix_available == 0:
            # we have to give one to netflix
            dict_decision.update({"netflix":"add"})
            self.netflix_add()

        elif self.deployed_netflix_available == 4:
            # we cant allocate more
            dict_decision.update({"netflix":"delete"})
            self.netflix_delete()
        
        else:
            # normal case
            tag = random.random()
            if tag < 0.5:
                dict_decision.update({"netflix":"delete"})
                self.netflix_delete()
            else:
                dict_decision.update({"netflix":"add"})
                self.netflix_add()
        
        return dict_decision