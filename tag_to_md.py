# -*- coding: utf-8 -*-

#   __
#  /__)  _  _     _   _ _/   _
# / (   (- (/ (/ (- _)  /  _)
#


"""
 TAG_TO_MD
~~~~~~~~~~~~~~~~~~~~~
feature:

1. 根据指定目录, 遍历这个目录下的所有 *.md 文件
2. 解析 *.md 文件的头, 格式为如下, 解析 tag 标签,   空格隔开
3. 解析到的所有 tag , 在指定目录生成指定的 tag 文件

example:
---
title: tagpage
published: true
tag: JAVA PYTHON
---
===>
JAVA.md
---
layout: tagpage
title: "Tag: JAVA"
tag: JAVA
---

PYTHONE.md
---
layout: tagpage
title: "Tag: PYTHONE"
tag: PYTHONE
---

step:
1. 传入指定的目录，遍历这个目录下的所有 *.md 文件
2. 传入markdown文件路径，解析获取metaData数据
3. 根据metaData 解析 tag
4. 遍历tag 生成指定格式的文件
"""

import io
import sys
import pypandoc
import panflute
import read_write_file
import os


def action(elem, pydoc):
    if isinstance(elem, panflute.Image):
        pydoc.images.append(elem)
    elif isinstance(elem, panflute.Link):
        pydoc.links.append(elem)
    elif isinstance(elem, panflute.MetaInlines):
        pydoc.metaInlines.append(elem)
    elif isinstance(elem, panflute.Str):
        print(elem.text)
        pydoc.str.append(elem.text)


# 根据md文件路径获取 metaData  tag
def get_meta_by_md(file_path):
    data = pypandoc.convert_file(file_path, 'json', encoding='utf-8')
    doc = panflute.load(io.StringIO(data))
    tag_str = doc.get_metadata('tag')
    meta_title = doc.get_metadata('title')
    tag_list = []
    if tag_str is not None:
        tag_list = tag_str.split(' ')
    return {
        'title': meta_title,
        'tag_list': tag_list
    }


if __name__ == '__main__':
    # dirPath = '/Users/tx/Desktop/post'
    # outPutPath = dirPath + '_md'
    dirPath = ''
    outPutPath = ''
    if len(dirPath) < 1:
        if len(sys.argv) > 1:
            dirPath = sys.argv[1]
        else:
            try:
                dirPath = input("请输入需解析的文件夹目录: ")
            except EOFError:
                print('👋🏻👋🏻 bye!')
            except KeyboardInterrupt:
                print('已取消操作，👋🏻👋🏻 bye!')
            else:
                print("你输入的路径: {}".format(dirPath))

    if len(outPutPath) < 1:
        if len(sys.argv) > 2:
            outPutPath = sys.argv[2]
        else:
            try:
                outPutPath = input("请输入解析输出的文件夹目录: ")
            except EOFError:
                print('👋🏻👋🏻 bye!')
            except KeyboardInterrupt:
                print('已取消操作，👋🏻👋🏻 bye!')
            else:
                print("你输入的路径: {}".format(outPutPath))
    if len(dirPath.strip()) == 0:
        print('👋🏻👋🏻 bye bye!😑')
    else:
        try:
            if len(outPutPath.strip()) == 0:
                outPutPath = dirPath + '_md'
            suffix = '.md'
            mdList = read_write_file.get_file_name(dirPath, suffix)
            if len(mdList[1]) == 0:
                print('🖕 该目录下无markdown文件可以解析')
            else:
                for mdPath in mdList[1]:
                    metaData = get_meta_by_md(mdPath)
                    tagList = metaData['tag_list']
                    title = metaData['title']
                    basename = os.path.basename(mdPath)
                    newMdDirFileName = os.path.splitext(basename)[0]
                    print('👻 开始解析！{}'.format(basename))
                    for tagName in tagList:
                        newFileName = tagName + suffix
                        newPathTuple = (outPutPath, newMdDirFileName, newFileName)
                        newPath = os.path.join(*newPathTuple)
                        newMdValues = {
                            'layout': title,
                            'title': 'Tag: ' + tagName,
                            'tag': tagName
                        }
                        sTemplate = '---\nlayout: {layout}\ntitle: {title}\ntag: {tag}\n---'
                        newStr = sTemplate.format(**newMdValues)
                        read_write_file.touch_file(newPath, newStr)
                    print('✅ 已完成！{}'.format(basename))
                print('结束la !!! 😉')
        except EOFError:
            print('🙅 ‍中止操作')
        except (RuntimeError, TypeError, NameError):
            print('🙅🏻‍ ️文件夹路径不正确')
            pass
