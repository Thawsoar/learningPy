# -*- coding: UTF-8 -*-

"""
feature:
    前提： 需要同步的两个数据库的表结构相同
    功能： 将两个数据库的相同的表结构数据通过id同步，更新或者插入
          每个表一个线程同步
    配置：
          {from_db} 数据来源的数据库配置
          {to_db} 需要被同步的数据库配置
          {tables} 需要配置的表名
          {size}支持配置每页条数，分页同步数据

steps:
    1. 连接数据库
    2. 查询源数据
    3. 生成更新语句sql
    4. 处理源数据
    5. 批量同步
    6. 关闭数据库

"""

import pymysql
import yaml
import logging
import math
import time
import threading
import os
import multiprocessing as mp
from tqdm import tqdm


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# 创建一个handler，用于写入日志文件
logger_path = 'sync_data_log.txt'
fh = logging.FileHandler(logger_path, mode='a')
logger.addHandler(fh)
# # 创建一个handler，输出到控制台
# ch = logging.StreamHandler()
# ch.setFormatter(logging.Formatter("%(message)s"))
# logger.addHandler(ch)


# 清除日志
def clear_log():
    # 大于10M清除日志
    if os.path.getsize(logger_path) > 1024 * 10:
        os.remove(logger_path)


# 每n秒执行一次清除日志操作
def timer(n):
    while True:
        print(time.strftime('%Y-%m-%d %X', time.localtime()))
        clear_log()  # 此处为要执行的任务
        time.sleep(n)


# 获取配置文件数据
def get_config(config_name):
    with open(config_name, encoding='utf-8') as f:
        return yaml.safe_load(f)


# 获取表结构 字段
def get_table_head(cursor):
    head = []
    for field in cursor.description:
        head.append(field[0])
    return tuple(head)


# 打开数据库连接
def sync_table(table_name):
    # 请求锁
    lock.acquire()
    logger.info("%s 线程启动: %s" % (table_name, time.ctime(time.time())))
    # 游标查询第一条数据的所有字段
    query_one_sql = f"SELECT * FROM `{config['from_db']['database']}`.`{table_name}` LIMIT 0,1"
    from_cursor.execute(query_one_sql)
    # 获取表头字段
    table_head_field = get_table_head(from_cursor)

    # 查询表的总条数
    query_count_sql = f"SELECT COUNT(*) FROM `{config['from_db']['database']}`.`{table_name}`"
    from_cursor.execute(query_count_sql)

    # 总条数
    count = from_cursor.fetchone()[0]
    # 每页条数
    size = config['size']
    # 页数
    page = math.ceil(count / size)
    # Example Sql
    # INSERT INTO wx_shop_auth_info(id, shop_id, app_id, auth_code) VALUES(23, 23, '77', '234234')
    # ON DUPLICATE KEY UPDATE id=VALUES(id),shop_id=VALUES(shop_id),app_id=VALUES(app_id),auth_code=VALUES(auth_code)
    # 更新或者插入数据sql
    replace_sql = f"INSERT INTO `{config['to_db']['database']}`.`{table_name}` {table_head_field} ".replace("'", "")
    insert_sql_str = ''
    update_sql_str = ''
    for index, field in enumerate(table_head_field):
        # 拼接sql语句
        insert_sql_str = insert_sql_str + '%s'
        update_sql_str = update_sql_str + f"{field}=VALUES({field})"
        if index < len(table_head_field) - 1:
            insert_sql_str = insert_sql_str + ', '
            update_sql_str = update_sql_str + ', '
    replace_sql = f"{replace_sql} VALUES({insert_sql_str}) ON DUPLICATE KEY UPDATE {update_sql_str}"
    logger.info(f'{table_name}表成功生成sql语句')
    logger.info(f'{table_name}表数据开始同步\n')
    start = time.time()
    # 遍历页数更新数据
    for i in range(page):
        from_cursor.execute(f"SELECT * FROM `{config['from_db']['database']}`.`{table_name}` LIMIT {i},{(i + 1) * size}")
        # 每页的数据
        data = from_cursor.fetchall()
        logger.info(f'{table_name}表第{i + 1}页数据准备完成')
        # 执行批量更新操作
        try:
            to_cursor.executemany(replace_sql, data)
            to_db.commit()
            logger.info(f'{table_name}表第{i + 1}页数据同步成功\n')
        except Exception as ex:
            to_db.rollback()
            logger.warning(f' ❌{table_name}第表{i + 1}页数据失败\n')
            logging.exception(ex)
    end = time.time()
    logger.info(f'✅ {table_name}表数据同步成功, 共耗时{end - start}\n')
    logger.info(f'退出线程: {table_name} 耗时{end - start}')
    # 释放锁
    lock.release()


def main():
    # 数据源
    try:
        global from_db
        global to_db
        global from_cursor
        global to_cursor
        global lock
        global all_thread
        logger.info('🙏🙏🙏 开始同步 ' + '-' * 50)
        from_db = pymysql.connect(charset="utf8", **config['from_db'])
        logger.info(f"成功连接数据库{config['from_db']['database']}")
        # 需要同步的数据库
        to_db = pymysql.connect(charset="utf8", **config['to_db'])
        logger.info(f"成功连接数据库{config['to_db']['database']}\n")
        # 使用 cursor() 方法创建游标对象
        from_cursor = from_db.cursor()
        to_cursor = to_db.cursor()
        # 创建锁
        lock = threading.Lock()
        # 开启线程 执行同步操作
        all_thread = []
        try:
            for tableName in config['tables']:
                thread = threading.Thread(target=sync_table, args=(tableName,))
                thread.start()
                all_thread.append(thread)
            for t in all_thread:
                t.join()
            logger.info('退出主线程\n')
            # 主线程结束时间
            print(time.strftime("主线程结束时间: %Y-%m-%d %H:%M:%S", time.localtime()))
        except Exception as e:
            print("Error: 无法启动线程", e)
            logging.exception(e)
        # 关闭数据库连接
        from_db.close()
        to_db.close()
        logger.info(f"关闭连接数据库{config['from_db']['database']}")
        logger.info(f"关闭连接数据库{config['to_db']['database']}")
        logger.info('🤟🤟🤟同步完成' + '-' * 50 + '\n\n')
    except Exception as e:
        print("Error: ", e)
        logging.exception(e)
    # time.sleep(10)

    # 周期性任务
    if not config['once']:
        print(time.strftime("周期性任务: %Y-%m-%d %H:%M:%S", time.localtime()))
        sche_timer = threading.Timer(config['timer'], main)
        sche_timer.start()


if __name__ == "__main__":
    config = get_config('sql_config.yaml')
    # 是否只执行一次
    if config['once']:
        main()
    else:
        # 是否立刻执行一次后周期性执行
        first_task = 1 if config['immediately'] else config['timer']
        print(first_task)
        timer = threading.Timer(first_task, main)
        timer.start()

    # 单独开一个进程清除日志
    p1 = mp.Process(target=timer, args=(3600,))
    p1.start()
    p1.join()



