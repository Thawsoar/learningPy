# -*- coding: utf-8 -*-

#   __
#  /__)  _  _     _   _ _/   _
# / (   (- (/ (/ (- _)  /  _)
#


"""
 GET_MD_IMGS
~~~~~~~~~~~~~~~~~~~~~
feature: 解析markdown文件获取本地图片的地址并上传至github图床
step:
1. 传入指定本地markdown文件地址获取图片地址列表
2. 获取图片地址列表 上传至github 图床
3. 替换本地地址
"""
import io
import sys
import pypandoc
import panflute
import urllib

import upload_file
import replace_str


def action(elem, pydoc):
    if isinstance(elem, panflute.Image):
        pydoc.images.append(elem)
    elif isinstance(elem, panflute.Link):
        pydoc.links.append(elem)


if __name__ == '__main__':
    print(sys.argv)
    filePath = ''
    if len(sys.argv) > 1:
        filePath = sys.argv[1]
    else:
        try:
            filePath = input("请输入Markdown文件路径: ")
        except EOFError:
            print('👋🏻👋🏻 bye!')
        except KeyboardInterrupt:
            print('已取消操作，👋🏻👋🏻 bye!')
        else:
            print("你输入的路径: {}".format(filePath))
    if len(filePath.strip()) == 0:
        print('👋🏻👋🏻 bye!')
    else:
        # filePath = '/Users/tx/Desktop/test.md'
        try:
            data = pypandoc.convert_file(filePath, 'json', encoding='utf-8')
            doc = panflute.load(io.StringIO(data))
            doc.images = []
            doc.links = []
            doc = panflute.run_filter(action, doc=doc)
            for image in doc.images:
                # 去除空格 %20
                url = urllib.parse.unquote(image.url)
                # 上传至github
                res_img_url = upload_file.handle_local_file(url)
                # 替换本地图片地址
                replace_str.alter(filePath, url, res_img_url['url'])
        except EOFError:
            print('🙅 ‍中止操作')
        except (RuntimeError, TypeError, NameError):
            print('🙅🏻‍ ️Markdown文件路径不正确')
            pass




