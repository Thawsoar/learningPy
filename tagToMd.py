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


if __name__ == '__main__':
    filePath = '/Users/tx/Desktop/test.md'
    if len(filePath) < 1:
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
            tagStr = doc.get_metadata('tag')
            tagList = tagStr.split(' ')
            print(tagList)

        except EOFError:
            print('🙅 ‍中止操作')
        except (RuntimeError, TypeError, NameError):
            print('🙅🏻‍ ️Markdown文件路径不正确')
            pass




