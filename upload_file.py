# -*- coding: utf-8 -*-

#   __
#  /__)  _  _     _   _ _/   _
# / (   (- (/ (/ (- _)  /  _)
#

"""
 UPLOAD_FILE
~~~~~~~~~~~~~~~~~~~~~
feature: 上传图片至GITHUB图床
step:
1. 配置config.yaml  github图床仓库
2.
    2.1 从剪贴板上读取复制的图片数据  上传至github
    2.2 传入指定本地图片地址 上传至github
3. 返回结果  将图床地址格式化成markdown语法  赋值到剪切板里
"""

import io
import os
import re
import json
import time
import base64
import requests
import subprocess

from urllib import parse
# Pillow
from PIL import Image, ImageGrab
# PyObjC
from AppKit import NSPasteboard, NSURLPboardType

import yaml

# 配置文件数据
config_obj = {}


# 从剪切板获取完整的文件路径
def get_path():
    # https://developer.apple.com/documentation/appkit/nspasteboard/pasteboardtype
    pb = NSPasteboard.generalPasteboard()
    url = pb.stringForType_(NSURLPboardType)

    if url is None:
        return None
    else:
        plist_bytes = url.url("utf-8")
        path_byte = re.findall(rb'<string>file://(.+?)</string>', plist_bytes)[0]
        path_utf8 = path_byte.decode('utf-8')
        return parse.unquote(path_utf8)


# 把数据推送到 github
def push(file_base64, filename):
    # 检查配置项
    if check_config() is None:
        return 0
    url = 'https://api.github.com/repos/{GithubName}/{Repository}/contents/{Filename}'.format(
        GithubName=config_obj['GithubName'],
        Repository=config_obj['Repository'],
        Filename=filename
    )

    headers = {
        "Authorization": 'token {Authorization}'.format(
            Authorization=config_obj['Authorization']
        )
    }

    data = json.dumps({
        "message": "auto commit",
        "committer": {
            "name": config_obj['Name'],
            "email": config_obj['Email'],
        },
        "content": file_base64
    })

    response = requests.put(url=url, data=data, headers=headers)

    return response


# 从文件路径得到文件后缀
def get_extension(file_path):
    return os.path.splitext(file_path)[1]


# 用 Base64 对给定的 Bytes 进行编码
def bytes_to_base64(data):
    return base64.b64encode(data).decode('utf-8')


# 拼接文件名
def get_filename(extension):
    return time.strftime("%Y%m%d%H%M%S", time.localtime()) + extension


# 处理 github 返回的响应
def handle_response(response, filename, extension):
    if response.status_code == 201:
        url_dict = build_url(filename, extension)
        copy_to_clipboard(url_dict['md_url'])
        icon = "✅"
    else:
        icon = "❌"
    print(icon + " " + response.reason + " " + url_dict['url'])
    return url_dict


# 处理本地文件
def handle_local_file(file_path):
    with open(file_path, 'rb') as f:
        print(file_path)
        extension = get_extension(file_path)
        file_base64 = bytes_to_base64(f.read())

        filename = get_filename(extension)

        response = push(file_base64, filename)

        return handle_response(response, filename, extension)


# 处理剪切板的文件，与本地文件不同的是，剪切板的文件好像是在内存中，它并没有一个文件路径(有待研究)
def handle_clipboard():
    image = ImageGrab.grabclipboard()

    if isinstance(image, Image.Image):

        buffer = io.BytesIO()

        image_format = "png"

        extension = "." + image_format

        image.save(buffer, image_format)

        file_base64 = bytes_to_base64(buffer.getvalue())

        filename = get_filename(extension)

        response = push(file_base64, filename)

        return handle_response(response, filename, extension)
    else:
        print("❌ 剪切板的内容不是图片")


# 把给定的字符串复制到剪切板
def copy_to_clipboard(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)

    p.stdin.write(data.encode("utf-8"))

    p.stdin.close()

    p.communicate()


# 判断是否是图片
def is_image(extension):
    return extension in [".png", ".jpeg", ".gif", "jpg"]


# 按照 jsdelivr 的规则构建 url
def build_url(filename, extension):
    url = 'https://cdn.jsdelivr.net/gh/{GithubName}/{Repository}@{Branch}/{Filename}'.format(
        GithubName=config_obj['GithubName'],
        Repository=config_obj['Repository'],
        Branch=config_obj['Branch'],
        Filename=filename
    )

    if is_image(extension):
        md_url = markdown(url)

    return {'url': url, 'md_url': md_url}


# 按照 markdown 语法拼接 url
def markdown(url):
    return "![](" + url + ")"


# 获取配置文件数据
def get_config():
    with open('config.yaml', encoding='utf-8') as f:
        # print(yaml.safe_load(f))
        return yaml.safe_load(f)


# 检查配置文件
def check_config():
    global config_obj
    config_obj = get_config()
    config_success = 1
    for key, value in config_obj.items():
        if value is None:
            print('🖕 请完善配置文件[' + key + ']字段')
            config_success = 0
            break
        # print(config)
    if config_success:
        print('👍 成功解析配置文件')
    return config_success


if __name__ == '__main__':
    path = get_path()
    print(path)
    if path is None:
        toast = handle_clipboard()
    else:
        toast = handle_local_file(path)
