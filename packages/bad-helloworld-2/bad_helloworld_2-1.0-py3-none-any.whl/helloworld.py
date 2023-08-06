import numpy as np
import sys

def say(cnt=5):
    helloworld = "Hello, World!"
    for i in np.arange(cnt):
        print(helloworld[:int(np.random.uniform()*len(helloworld))])


if __name__ == '__main__':
    say(5 if len(sys.argv) == 1 else int(sys.argv[1]))
