#-*- encoding:utf-8 -*-
import requests
import time
import sys
import json
# from multiprocessing import Pool
# import config_file
# import multiprocessing as mp
from config import *


headers = HEADERS
query_words = '复仇者联盟'
a = requests.get(pre_url+query_words+next_url, headers = headers)
context = a.content.decode('utf8').split()
for line in context:
    if line[:extract_tag_len] == extract_tag:
        print(line)




with open('test.txt', 'w', encoding='utf8') as f:
    f.write(a.content.decode('utf8'))



# if __name__ == "__main__":
#     pass