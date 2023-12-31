# 微博评论爬虫

[English](README_EN.md) | [中文](README.md)

**免责声明：本脚本仅供学习和研究目的使用，严禁用于任何商业或违法活动。对于使用本脚本可能引发的任何问题或违法行为，作者概不负责。请使用者在遵守法律法规的前提下使用本脚本。**

这是一个使用Python编写的微博评论爬虫脚本，使用微博API从微博中抓取评论数据。脚本从MySQL数据库中获取博文数据，然后针对每篇博文获取评论并将其保存回数据库。


## 依赖环境

要运行此脚本，您需要安装以下依赖项：

- PyMySQL~=1.0.3：用于连接和操作MySQL数据库。
- requests~=2.31.0：用于发送HTTP请求和获取网页数据。
- python-dateutil~=2.8.2：用于解析日期和时间。

## 文件结构

项目包含以下文件：

- `main.py`：主要的脚本文件，包含了从MySQL数据库中获取博文数据、爬取评论数据并保存回数据库的逻辑。
- `setting.py`：配置文件，包含MySQL数据库和请求头的相关配置。
- `requirements.txt`：包含项目的依赖项列表。

## 配置

在运行脚本之前，您需要进行一些配置：

1. 在 `setting.py` 文件中，根据您的MySQL数据库设置，修改以下变量：
   - `MYSQL_HOST`：MySQL数据库的主机地址。
   - `MYSQL_PORT`：MySQL数据库的端口号。
   - `MYSQL_USER`：MySQL数据库的用户名。
   - `MYSQL_PASSWORD`：MySQL数据库的密码。
   - `MYSQL_DATABASE`：要使用的数据库名称。
   - `WEIBO_BLOG_TABLE_NAME`：存储博文数据的表名。
   - `BLOG_COMMENT_TABLE_NAME`：存储评论数据的表名。
   - `WEIBO_COOKIE`：您的微博登录cookie。请确保具有足够的权限来访问评论数据。

2. 如果需要修改其他请求头参数，请根据实际情况修改 `HEADERS` 变量。

## 使用方法

1. 确保您已正确配置MySQL数据库和请求头。

2. 安装项目的依赖项。可以使用以下命令安装所需的包：

   ```shell
   pip install -r requirements.txt
   ```

3. 运行 `main.py` 脚本。执行以下命令：

   ```shell
   python main.py
   ```

   脚本将从MySQL数据库中获取博文数据，然后爬取每篇博文的评论数据并将其保存回数据库。

   注意：由于微博API的限制，您可能需要一些时间才能获取完整的评论数据，特别是对于大量博文的情况。脚本使用了多线程来加速爬取过程，默认使用

1个线程。

4. 查看输出信息以监视爬取进度和可能出现的错误。

5. 爬取完成后，您可以在MySQL数据库中查看存储评论数据的表。

## 注意事项

- 使用此脚本爬取微博评论数据需要提供有效的微博登录cookie，以确保有权限访问评论数据。请确保您的cookie有效，并具有足够的权限来访问所需的评论数据。
- 爬取评论数据可能会受到微博API的限制，例如每小时的请求次数限制。请根据需要进行适当的调整和控制，以避免触发微博API的限制或封禁。
- 微博可能会对其API进行更改或限制访问，因此该脚本的可用性和稳定性可能会受到影响。

## 免责声明

使用此脚本需要遵守以下几点：

1. 使用该脚本需要您自行承担责任。作者对该脚本的使用、功能和结果不承担任何责任。
2. 请确保您的使用符合法律法规，并遵守微博的使用条款和隐私政策。请注意不要侵犯他人的权益。
3. 请注意不要滥用该脚本，以免给微博服务器带来过大的负载或影响其他用户的正常使用。
4. 作者建议您在使用该脚本之前，详细阅读并理解微博的相关规定，并确保您的操作是合法且符合规定的。

如果您决定使用该脚本，请确保自己的合法性和责任，并承担相应的风险。

如有任何问题或疑问，请联系作者：[2546406321@qq.com]。