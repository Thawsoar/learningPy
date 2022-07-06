"""
Python爬取B站视频弹幕
"""
import re
import os
import jieba
import jieba.analyse
import requests
url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=337903262'

response = requests.get(url)
response.encoding = 'url-8'
content_list = re.findall('<d p=".*?">(.*?)</d>', response.text)
content_str = ''.join(content_list)
keywords_top10 = jieba.analyse.extract_tags(content_str, withWeight=True, topK=10)

for d in content_list:
    # for keywords in keywords_top10:
    if '佳能' in d:
        print(d)
print(keywords_top10)
# print('adf' in 'adf123')
