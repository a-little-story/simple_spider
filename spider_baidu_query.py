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
    while True:  # 一直循环，知道访问站点成功
        try:
            a = requests.get(url, headers=headers)
            if a.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        except requests.exceptions.ChunkedEncodingError:
            time.sleep(1)
        except:
            time.sleep(1)
    context = a.content.decode('utf8')
    context = context.split()
    for line in context:
        if line[:extract_tag_len] == extract_tag:
            return line[extract_tag_len:-1]

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

        except:
            pass

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
        out_file_name = file_pre+str(i)+'output'
        my_pool.apply_async(func, (in_file_name, out_file_name))
    my_pool.close()
    my_pool.join()


if __name__ == "__main__":
    # split_file()
    # spider_single(query_file+'1', query_file+'1out')
    multi_p_spider()