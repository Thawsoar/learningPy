import os
import time

# 1. 需要备份的文件和目录
# 以列表的形式指明
# Windows 的例子：
# source = ['"C:\\My Documents"', 'C:\\Code']
# Mac OS X 和 Linux 的例子：
source = ['/Users/tx/Desktop/test']
# 注意到当路径中有空格时
# 你需要使用双重引号

# 2. 备份文件存放路径
# 即主备份路径
# Windows 的例子：
# target_dir = 'E:\\Backup'
# Mac OS X 和 Linux 的例子：
target_dir = '/Users/tx/Desktop/backup'
# 记得把对应的路径改成你想备份到的地方

# 如果目的路径不存在，则创建
if not os.path.exists(target_dir):
    os.mkdir(target_dir)  # 创建文件夹

# 3. 备份文件被打包为一个 zip 文件
# 4. 当前日期是主备份目录下的一个子文件夹
today = target_dir + os.sep + time.strftime('%Y%m%d')
# 当前时间作为备份文件的文件名
now = time.strftime('%H%M%S')

# zip 文件名
target = today + os.sep + now + '.zip'

# 如果不存在，则创建子文件夹
if not os.path.exists(today):
    os.mkdir(today)
    print('Successfully created directory', today)

# 5. 用 zip 命令打包文件
zip_command = 'zip -r {0} {1}'.format(target,
                                      ' '.join(source))

# 运行备份程序
print('Zip command is:')
print(zip_command)
print('Running:')
if os.system(zip_command) == 0:
    print('Successful backup to', target)
else:
    print('Backup FAILED')
