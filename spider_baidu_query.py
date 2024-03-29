#-*- encoding:utf-8 -*-
import requests
import time
import os
import json
import logging

from pprint import pprint
from multiprocessing import Pool
# import config_file
import multiprocessing as mp
from config import *

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("spider")


def extract_tag_content(query_words, pre_url=pre_url, next_url=next_url, headers=HEADERS,
                extract_tag=extract_tag, extract_tag_len=extract_tag_len, max_try=10, sleep_time=0.2):
    url = pre_url + query_words + next_url
    i = 0
    while i < max_try:  # 一直循环，知道访问站点成功
        i += 1
        try:
            a = requests.get(url, headers=headers)
            if a.status_code == 200:

                break
        except requests.exceptions.ConnectionError:
            time.sleep(sleep_time)
        except requests.exceptions.ChunkedEncodingError:
            time.sleep(sleep_time)
        except:
            time.sleep(sleep_time)
    if i == max_try:
        return '[]'
    try:
        context = a.content.decode('utf8')
    except UnicodeDecodeError:
        a.encoding = 'utf8'
        context = a.content

    context = context.split()
    for line in context:
        if line[:extract_tag_len] == extract_tag:
            return line[extract_tag_len:-1]
    return '[]'


def spider_single(file_path, output_path):
    with open(file_path, 'r', encoding='utf8') as f, \
            open(output_path, 'w', encoding='utf8') as f_out:
        try:
            for line in f:
                query = extract_query(line)
                result = extract_tag_content(query)
                for i in range(5):
                    if result != '[]':
                        break
                    query = extract_query(line, i)
                    if not query:
                        break
                    result = extract_tag_content(query)
                t = {}
                if not query:
                    t[extract_query(line)] = '[]'
                else:
                    t[query] = result if result else '[]'
                t = json.dumps(t, ensure_ascii=False) + '\n'
                f_out.write(t)
        except UnicodeDecodeError:
            logger.warning(f"UnicodeDecodeError: {line}{i}")
        # ii = 0
        # for line in f:
        #     ii += 1
        #     if ii < 760:
        #         continue
        #     print(ii)
        #     query = extract_query(line)
        #     result = extract_tag_content(query)
        #     for i in range(5):
        #         if result != '[]':
        #             break
        #         query = extract_query(line, i)
        #         if not query:
        #             break
        #         result = extract_tag_content(query)
        #     t = {}
        #     if not query:
        #         t[extract_query(line)] = '[]'
        #     else:
        #         t[query] = result if result else '[]'
        #     t = json.dumps(t, ensure_ascii=False) + '\n'
        #     f_out.write(t)


def extract_query(line, func_nums = -1):

    line = json.loads(line)
    query = line['query']
    if func_nums<0:
        return query
    else:
        # if func_nums > len(query_file.split())-1:
        #     return None
        # if func_nums == 0:
        #     return query[:MAX_LENGTH]
        query = query.split()
        r = []
        r.append(query[0])
        cur_len = len(query.pop(0))
        if func_nums < len(query):
            query.pop(func_nums)
        for q in query:
            if cur_len+1+len(q)>MAX_LENGTH:
                break
            cur_len += 1
            cur_len += len(q)
            r.append(q)
        return ' '.join(r)
    # else:
    #     query = query.split()
    #     r = []
    #     r.append(query[0])
    #     cur_len = len(query.pop(0))
    #     query.pop(func_nums)
    #     for q in query:
    #         if cur_len+1+len(q)>MAX_LENGTH:
    #             break
    #         cur_len += 1
    #         cur_len += len(q)
    #         r.append(q)
    #     return ' '.join(r)


def split_file(file_path=query_file, nums=pool_size):
    result  = os.popen(f'wc -l {file_path}').readlines()
    print(result)
    line_nums = int(result[0].split()[0])
    nums_per_file = int(line_nums/nums) + 1
    command = f"split -l {nums_per_file} {file_path} -d -a 2 {file_path}"
    print(command)
    os.popen(command).readlines()


def multi_p_spider(func=spider_single, pool_size=pool_size, file_pre=query_file):
    my_pool = Pool(processes=pool_size)
    for i in range(pool_size):
        in_file_name = file_pre+'0'+str(i)
        out_file_name = file_pre+str(i)+'output2'
        my_pool.apply_async(func, (in_file_name, out_file_name))
    my_pool.close()
    my_pool.join()


def merge_result(file_pre=query_file, nums=pool_size, output_file=rssult_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for i in range(nums):
            file_name = file_pre + str(i) + 'output2'
            assert os.path.exists(file_name), f"the file {file_name} does not exist"
            line_nums = 0
            with open(file_name, 'r', encoding='utf-8') as f_:
                for line in f_:
                    line_nums += 1
                    f.write(line)
            logger.info(f'{file_name} has {line_nums} lines')





if __name__ == "__main__":
    # split_file()
    # spider_single(query_file+'1', query_file+'1out')
    logger.info("start working")
    # spider_single('./data/json_format00', './data/json_format0output2')
    # multi_p_spider()
    merge_result()