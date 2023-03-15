# @Time    : 2023/3/14 0:13
# @Author  : tamya2020
# @File    : ohRequest.py
# @Description :
import random


def LoadUserAgent(filename="./parse_content/user_agents.txt"):
    """
    filename:string,path to user-agent file
    """
    ualist = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line:
                ualist.append(line.strip()[1:-1])
    random.shuffle(ualist)
    return ualist


if __name__ == '__main__':
    print(random.choice(LoadUserAgent()))
