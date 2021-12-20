# -*- coding: utf-8 -*-


"""
函数说明:获取指定目录下的、指定后缀的文件名及路径+文件名的拼接
    例如：.md、.json
Parameters:
    path - 目录所在的路径 例如 path=/Users/tx/Desktop/post'
    suffix  -  后缀,例如'.md'
Returns:
    input_template_all - 指定后缀的所有文件名 xx.md
    input_template_all_Path - 文件名和该路径的拼接 例如：/Users/tx/Desktop/post/test_1.md'
"""
# 参考：https://www.runoob.com/python/os-walk.html

import os
import string


def get_file_name(path, suffix):
    input_template_all = []
    input_template_all_path = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            # print(os.path.join(root, name))
            if os.path.splitext(name)[1] == suffix:
                input_template_all.append(name)
                input_template_all_path.append(os.path.join(root, name))
        
    return input_template_all, input_template_all_path


# 新建文件并且写入字符串
def touch_file(filename, text):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(text)
        print('🙏 成功生成文件：{}'.format(filename))


if __name__ == '__main__':
    dirPath = '/Users/tx/Desktop/post'
    res = get_file_name(dirPath, '.md')
    print(res)
    values = {'layout': 'layout', 'title': 'title', 'tag': 'tag'}

    s = '---\nlayout: {layout}\ntitle: {title}\ntag: {tag}\n---'
    print('FORMAT:', s.format(**values))

    touch_file('/Users/tx/Desktop/post_md/test_2/java.md',  s.format(**values).strip())
