#!/usr/bin/python3
"""
多线程并发
"""
import threading
import time

exitFlag = 0


class CustomThread (threading.Thread):
    def __init__(self, thread_id, name, fun):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.fun = fun

    def run(self):
        print("开启线程：" + self.name)
        process_data(self.fun, self.name)
        print("退出线程：" + self.name)


def test(test):
    print("test:" + test)
    time.sleep(3)


def process_data(fun, thread_name):
    print(thread_name)
    fun(thread_name)
    print("%s processing" % thread_name)


# 创建新线程
def create_thread(thread_list, fun):
    thread_id = 1

    # 创建新线程
    for tName in thread_list:
        thread = CustomThread(thread_id, tName, fun)
        thread.start()
        all_thread.append(thread)
        thread_id += 1
    return all_thread


def close_thread():
    # 等待所有线程完成
    for t in all_thread:
        t.join()
    print("退出主线程")


if __name__ == "__main__":
    threadList = ["Thread-1", "Thread-2", "Thread-3"]
    all_thread = []
    exitFlag = 0
    create_thread(threadList, test)
    # 线程执行的函数
    process_fun = None
    # 通知线程是时候退出
    exitFlag = 1
    close_thread()


