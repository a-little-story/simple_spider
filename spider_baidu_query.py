#-*- encoding:utf-8 -*-
import requests
import time
import os
import json

from pprint import pprint
from multiprocessing import Pool
# import config_file
import multiprocessing as mp
from config import *




def extract_tag_content(query_words, pre_url=pre_url, next_url=next_url, headers=HEADERS,
                extract_tag=extract_tag, extract_tag_len=extract_tag_len):
    url = pre_url + query_words + next_url
    a = requests.get(url, headers=headers)
    context = a.content.decode('utf8')
    with open(query_words, 'w', encoding='utf-8') as f:
        f.write(context)
    context = context.split()
    print(len(context))
    for line in context:
        if line[:extract_tag_len] == extract_tag:
            return line[extract_tag_len:]

def spider_single(file_path, output_path):
    with open(file_path, 'r', encoding='utf8') as f, \
            open(output_path, 'w', encoding='utf8') as f_out:
        for line in f:
            query = extract_query(line)
            result = extract_tag_content(query)
            t = {}
            t[query] = result
            t = json.dumps(t, ensure_ascii=False) + '\n'
            f_out.write(t)



def extract_query(line):
    line = json.loads(line)
    return line['query'][:MAX_LENGTH]


def split_file(file_path=query_file, nums=pool_size):
    result  = os.popen(f'wc -l {file_path}').readlines()
    print(result)
    line_nums = int(result[0].split()[0])
    nums_per_file = int(line_nums/nums) + 1
    command = f"split -l {nums_per_file} {file_path} -d -a 2 {file_path}"
    print(command)
    os.popen(command).readlines()


def multi_p_spider(func=extract_tag_content, pool_size=pool_size):
    my_pool = Pool(processes=pool_size)
    for i in range(pool_size):
        my_pool.apply_async()

if __name__ == "__main__":
    spider_single('./data/json_format1', './data/json_format1out')