# -*- coding: utf-8 -*-

import json

def format_str(string, index=0, split_str="-"):

    split_list = string.split(split_str)
    insert_index = len(split_list) - 1 + index

    split_list.insert(insert_index, 'a1')
    return split_str.join(split_list)

with open("/Users/tx/Desktop/api.json", "r") as load_f:
    load_dict = json.load(load_f)
    for item in load_dict:
        item['api']['name'] = format_str(item['api']['name'])
        item['api']['priority'] = 10
        item['api']['serviceName'] =  format_str(item['api']['serviceName'], 1)
        item['gatewayService']['name'] =  format_str(item['gatewayService']['name'])
        item['api']['vars'] = [{
            "paramLocation": "COOKIE",
            "paramName": "yunlsp-version",
            "paramValue": "a1",
            "operator": "EQ"
        }]

    with open("/Users/tx/Desktop/api_format.json","w") as f:
        json.dump(load_dict, f)
        print("加载入文件完成...")
