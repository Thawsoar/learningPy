# encoding: utf-8
# -*- coding: utf-8 -*-
# python script for alfred workflow
# author: taoxiang

import re
import sys
import json
# from alfred.feedback import Feedback
from workflow import Workflow3
from workflow import web


def search_my_bug():
    url = "http://chandao.hgj.net/zentao/my-bug.json"
    headers = {
        'Content-Type': 'text/html; Language=UTF-8;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Cookie': 'lang=zh-cn; device=desktop; theme=default; keepLogin=on; za=taoxiang.tao; lastProject=220; preBranch=0; lastProduct=42; ajax_lastNext=on; preProjectID=220; projectTaskOrder=status%2Cid_desc; selfClose=0; zp=512c8cef2aa1d1429a3b14b59017288ddf155857; downloading=1; selfClose=1; windowWidth=1680; windowHeight=850; zentaosid=qmrgd782sip40fdmmmc53k5a16'
    }
    query_data = web.get(url=url, headers=headers).json()
    json_query_data = json.loads(query_data['data'])
    bug_list = []
    for item in json_query_data['bugs']:
        map_obj = {
            'uid': item['id'],
            'title': item['id'],
            'subtitle': item['title'],
            'arg': 'http://chandao.hgj.net/zentao/bug-view-{}.html'.format(item['id']),
            'valid': True,
        }
        bug_list.append(map_obj)
    first_item = {
        'uid': '-1',
        'title': '淦，还有{}个bug'.format(len(bug_list)),
        'subtitle': '加油改吧💪🏻',
        'arg': 'http://chandao.hgj.net/zentao/my-bug.html',
        'valid': True,
    }
    if len(bug_list) == 0:
        first_item['title'] = '🐂 木有bug啦'
        first_item['subtitle'] = '划水去 👻'
    bug_list.insert(0, first_item)
    return bug_list


def generate_feedback_results(result):
    wf = Workflow3()
    for item in result:
        wf.add_item(**item)
    wf.send_feedback()


def main():
    result = search_my_bug()
    generate_feedback_results(result)


if __name__ == "__main__":
    main()
