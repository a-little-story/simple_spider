#-*- encoding:utf-8 -*-
import requests
import time
import sys
import json
# from multiprocessing import Pool
# import config_file
# import multiprocessing as mp



headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"}
a = requests.get("https://www.baidu.com/s?wd=复仇者联盟&si=movie.douban.com&ct=2097152", headers = headers)
context = a.content.decode('utf8').split()
for line in context:
    if "bds.comm.iaurl" == line[:14]:
        print(line)




with open('test.txt', 'w', encoding='utf8') as f:
    f.write(a.content.decode('utf8'))



# if __name__ == "__main__":
#     pass