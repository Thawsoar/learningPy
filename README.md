# 记录用Python解决的一些问题

[TOC]

## feature: upload_md_imgs.py
> 解析本地markdown文件获取本地图片的地址并上传至github图床后替换本地图片路径

### Usage:


- 配置Github 图床
    > 新建配置文件config.yaml
    
    ```yaml
    GithubName: example
    Repository: FigureBed
    Branch: master
    Authorization: example
    Name: Thawsoar
    Email: 1306750238@qq.com
    ```

- 配置shell 别名
    ```shell
    alias uploadImg='python3 upload_md_imgs.py $para1'
    
    source ~/.bash_profile
    ```

- 使用方式
  1. 命令行交互
       ```shell
       python3 upload_md_imgs.py
       ```
       or
       ```shell
       uploadImg
       ```
  2. 命令行传参
       ```shell
       python3 upload_md_imgs.py example.md
       ```
       or
       ```shell
       uploadImg example.md
       ```

## feature: tag_to_md.py
> 1. 根据指定目录, 遍历这个目录下的所有 *.md 文件
> 2. 解析 *.md 文件的头, 格式为如下, 解析 tag 标签,   空格隔开
> 3. 解析到的所有 tag , 在指定目录生成指定的 tag 文件

### Usage

- 配置shell 别名
    ```shell
    alias tagToMd='python3 tag_to_md.py $para1 $para2'
    
    source ~/.bash_profile
    ```

- 使用方式
  1. 命令行交互
       ```shell
       python3 tagToMd.py
       ```
       or
       ```shell
       tagToMd
       ```
  2. 命令行传参
       ```shell
       python3 tagToMd.py [指定解析目录] [指定生成的目录]
       ```
       or
       ```shell
       tagToMd [指定解析目录] [指定生成的目录]
       ```

## feature: zen.py

> Alfred4 workflow  禅道相关的快捷操作

- [x] 查看未解决的bug列表，回车跳转详情
- [ ] 关闭bug提交注释后调用企业微信api发送消息给对应测试


## feature: perform_task_timer.py

- 前提： 需要同步的两个数据库的表结构相同
- 功能：
  - 将两个数据库的相同的表结构数据通过id同步，更新或者插入
  - 每个表一个线程同步数据
  - 单独开一个进程用于定期清除日志
- 配置：
  - {from_db} 数据来源的数据库配置
  - {to_db} 需要被同步的数据库配置
  - {tables} 需要配置的表名
  - {size}支持配置每页条数，分页同步数据


### Usage
- 配置文件sql_config.yaml
```yaml
# 数据库连接配置

# 数据源
from_db:
  host: example
  port: example
  user: example
  password: example
  database: example

# 需要同步的数据库
to_db:
  host: localhost
  port: 3306
  user: root
  password: password
  database: egg-server

# 需要同步的名称
tables:
  - wx_shop_auth_info
  - wx_shop_token
  - wx_component_verify_ticket
  - wx_component_token
  - wx_authorization_info

# 执行脚本 每{timer}秒执行脚本 {immediately}立刻执行一次后周期性执行 {once}只执行一次
timer: 1
immediately: True
once: False

# 分页同步{size}条数据
size: 50


```
- 使用方式

    ```shell
    python3 sync_data.py
    ```


