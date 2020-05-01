import numpy as np
import math
import random
from collections import Counter

# This is a simple normilized zipf based random value gererator

# N be the number of elements
# k be their rank
# s be the value of the exponent characterizing the distribution

# This function predict that out of a population of N elements, the normalized frequency of elements of rank k
# To check the formule, pls go to https://en.wikipedia.org/wiki/Zipf%27s_law at "Theoretical review"


class ZipfGenerator:

    def __init__(self, s, N):
        self.s = s
        self.N = N
        self.zipf_list = []

        # generate distribution list according to the s and N
        def nomilized_zipf(self,k):
            numerator = 1 / math.pow(k, self.s)
            denominator = 0
            for i in range(self.N):
                power_value_i = 1 / math.pow((i+1), self.s)
                denominator = denominator + power_value_i
            return_value = numerator / denominator

            return return_value

        def zipf_distribution_list(self):
            zipf_list = []
            cumulative_variable = 0

            for i in range(self.N):
                value_temp = nomilized_zipf(self,(i+1))
                cumulative_variable = cumulative_variable + value_temp
                zipf_list.append(cumulative_variable)
            # print(zipf_list)
            # print(len(zipf_list))
            return zipf_list

        self.zipf_list = zipf_distribution_list(self)

    
    def random_zipf_normalized_generator(self):
        random_uniform = random.uniform(0,1)
        # print("random_uniform selected = " + str(random_uniform))
        # generate zipf distribution list
        zipf_list = self.zipf_list
        N = self.N

        # compare the generated random value with zipf_distribution list
        for i in range(N):
            if (random_uniform - zipf_list[i]) < 0:
                return i+1
        return N


def test():
    zipfGenerator_1 = ZipfGenerator(1.2,10)
    result = []
    for i in range(100):
        temp = zipfGenerator_1.random_zipf_normalized_generator()
        result.append(temp)

    counter_result = Counter(result)
    print(counter_result)    


