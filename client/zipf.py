import numpy as np

def get_zipf_random():
    a = 1.2
    s = np.random.zipf(a, size=100)
    return s

print(get_zipf_random())