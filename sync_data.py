# -*- coding: UTF-8 -*-

"""
feature:
    前提： 需要同步的两个数据库的表结构相同
    功能： 将一个数据库的表数据通过id同步到另外一个数据库相同的表
steps:
    连接数据库
"""

import pymysql
import yaml
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='sync_data_log.txt')
logger = logging.getLogger(__name__)


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
def sysn_table(table_name):
    # 使用 execute()  方法执行 SQL 查询
    from_cursor.execute("SELECT * FROM `{}`.`{}`".format(config['from_db']['database'], table_name))

    # 使用 fetchall方法获取所有数据.
    data = from_cursor.fetchall()
    table_head_field = get_table_head(from_cursor)
    # 更新sql的语句
    update_sql = 'UPDATE `{}`.`{}` SET '.format(config['to_db']['database'], table_name)
    field_sql = ''
    for index, field in enumerate(table_head_field):
        # 拼接sql语句
        if field != 'id':
            field_sql = field_sql + field + '=(%s)'
            if index < len(table_head_field) - 1:
                field_sql = field_sql + ', '
    update_sql = update_sql + field_sql + ' where id=(%s)'
    logger.info('{}表成功生成sql语句'.format(table_name))
    # 拼接字段数据
    update_data = []  # 更新的数据
    for item in data:
        field_list = list(item)
        field_list.append(item[0])
        field_list.pop(0)
        update_data.append(tuple(field_list))
    logger.info('{}表同步数据准备完成'.format(table_name))
    # 执行批量更新操作
    try:
        to_cursor.executemany(update_sql, update_data)
        to_db.commit()
        logger.info('✅ {}表同步数据成功\n'.format(table_name))
    except:
        to_db.rollback()
        logger.warning('❌ {}表同步数据失败\n'.format(table_name))
        logging.exception("exception")


if __name__ == "__main__":
    logger.info('🙏🙏🙏 开始同步 ' + '-' * 50)
    # 数据源
    config = get_config('sql_config.yaml')
    try:
        from_db = pymysql.connect(charset="utf8", **config['from_db'])
        logger.info('成功连接数据库{}'.format(config['from_db']['database']))
        # 需要同步的数据库
        to_db = pymysql.connect(charset="utf8", **config['to_db'])
        logger.info('成功连接数据库{}\n'.format(config['to_db']['database']))
        # 使用 cursor() 方法创建游标对象
        from_cursor = from_db.cursor()
        to_cursor = to_db.cursor()
        # 遍历需要同步数据的表 执行同步操作
        for tableName in config['tables']:
            logger.info('开始同步表{}'.format(tableName))
            sysn_table(tableName)
        # 关闭数据库连接
        from_db.close()
        to_db.close()
        logger.info('关闭连接数据库{}'.format(config['from_db']['database']))
        logger.info('关闭连接数据库{}'.format(config['to_db']['database']))
        logger.info('✅ 🤟🤟🤟同步完成\n\n\n')
    except:
        logger.error('❌连接数据库失败')


