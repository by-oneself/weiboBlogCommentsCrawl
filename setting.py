# setting.py

# MySQL数据库配置
WEIBO_BLOG_TABLE_NAME = 'weibo'  # 博文表名
BLOG_COMMENT_TABLE_NAME = 'blog_comment'  # 评论表名

# MySQL数据库配置
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3000
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DATABASE = 'weibo'

# 微博的Cookie
WEIBO_COOKIE = 'xxxx'
# 请求头配置
HEADERS = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.baidu.com/',
    'Connection': 'keep-alive',
    'Cookie': WEIBO_COOKIE,
}
