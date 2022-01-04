# -*- coding: UTF-8 -*-

"""
feature:
    周期性脚本任务

"""

import time
import os
import sched
import yaml
import threading

schedule = sched.scheduler(time.time, time.sleep)


def perform_command(cmd, inc):
    # 在inc秒后再次运行自己，即周期运行
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    os.system(cmd)


def timming_exe(cmd, inc=60):
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    schedule.run()  # 持续运行，直到计划时间队列变成空为止


# 获取配置文件数据
def get_config(config_name):
    with open(config_name, encoding='utf-8') as f:
        return yaml.safe_load(f)


def printHello():
    print("start")
    timer = threading.Timer(5,printHello)
    timer.start()

if __name__ == "__main__":
    # 数据源
    # config = get_config('sql_config.yaml')
    # timming_exe('python3 sync_data.py', config['timer'])
    timer = threading.Timer(1,printHello)
    timer.start()
