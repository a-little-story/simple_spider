HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"}
pre_url = "https://www.baidu.com/s?wd="
next_url = "&si=movie.douban.com&ct=2097152"
extract_tag = "bds.comm.iaurl="
extract_tag_len = len(extract_tag)
pool_size = 10
query_file = 'data/json_format'
MAX_LENGTH = 38
