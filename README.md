
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

