
##  解析本地markdown文件获取本地图片的地址并上传至github图床后替换本地图片路径

### Example:


- 配置Github 图床
    > 配置文件config.yaml
    
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

