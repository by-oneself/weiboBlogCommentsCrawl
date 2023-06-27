import pymysql
import requests
import re
from functools import partial
from datetime import datetime
from dateutil.parser import parse as parse_date
from multiprocessing.dummy import Pool as ThreadPool
import time
from setting import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, WEIBO_BLOG_TABLE_NAME, HEADERS, BLOG_COMMENT_TABLE_NAME

cookie = 'XSRF-TOKEN=j4v-HZBRjDTZcQEfst-IoDA8; PC_TOKEN=47e1ef6988; login_sid_t=a691949d3ee68f0ed70c92fa6a3fe000; cross_origin_proto=SSL; WBStorage=4d96c54e|undefined; _s_tentry=passport.weibo.com; Apache=2117067849409.8438.1686301185755; SINAGLOBAL=2117067849409.8438.1686301185755; ULV=1686301185757:1:1:1:2117067849409.8438.1686301185755:; wb_view_log=1512*9822; WBtopGlobal_register_version=2023060916; ALF=1717837200; SSOLoginState=1686301202; SUB=_2AkMT3mUPdcPxrARXn_wWzW3hb41H-jygCwz5An7uJhIyOhhq7g03qSVutBF-XBPW5JX86WTBrZr3blUDWjDcQH1v; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WFbsHH66GyTcvB6nuLDyEAg5JpX5KzhUgL.FoMcS0B0eKq0e052dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSoMXe02ce0e7; WBPSESS=Dt2hbAUaXfkVprjyrAZT_BYbDhLQYgIxi7NGiMmUpKTxM6MQw-5jNb0rYyG6fywLkaTMh6cy1sFRp5GV1BtSbG5LK1NPG1q9pU_R6vV-xHatbM-2viMAAaOEO2dq8chv2T0GPVY2u9mu4si9yVeXxw=='  # 微博的cookie
headers = HEADERS


def check_table_exists(connection, table_name):
    cursor = connection.cursor()
    query = f"SHOW TABLES LIKE '{table_name}'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result is not None


def create_blog_comment_table(connection):
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS `{BLOG_COMMENT_TABLE_NAME}` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        bid VARCHAR(255),
        user_id VARCHAR(255),
        comment_id VARCHAR(255),
        content TEXT,
        reposts_count INT,
        comments_count INT,
        attitudes_count INT,
        created_at DATETIME,
        nickname VARCHAR(255),
        address VARCHAR(255)
    )
    """
    cursor.execute(query)
    cursor.close()


def fetch_data_from_mysql(connection):
    """从MySQL数据库中获取数据"""
    cursor = connection.cursor()
    query = f"SELECT bid, user_id FROM {WEIBO_BLOG_TABLE_NAME}"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data


def save_data_to_mysql(connection, data):
    """将数据保存到MySQL数据库中"""
    cursor = connection.cursor()
    query = "INSERT INTO `{BLOG_COMMENT_TABLE_NAME}` (bid, user_id, comment_id, content, reposts_count, comments_count, attitudes_count, created_at, nickname, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, data)
    connection.commit()
    cursor.close()


def extract_comment_data(result):
    """提取评论数据"""
    comment_id = result[0]
    content = re.findall(r'<span class="ctt">(.*?)</span>', result[1], re.S)[0].replace('<br />', '\n')

    reposts_count = 0
    comments_count = 0
    attitudes_count = 0

    reposts_match = re.search(r'Reposts\[(\d+)\]', result[1])
    if reposts_match:
        reposts_count = int(reposts_match.group(1))

    comments_match = re.search(r'Comments\[(\d+)\]', result[1])
    if comments_match:
        comments_count = int(comments_match.group(1))

    attitudes_match = re.search(r'赞\[(\d+)\]', result[1])
    if attitudes_match:
        attitudes_count = int(attitudes_match.group(1))

    created_at = None
    created_at_match = re.search(r'<span class="ct">(.*?)&nbsp;', result[1])
    if created_at_match:
        created_at_str = created_at_match.group(1).strip()

        # 使用dateutil库解析相对时间
        created_at = parse_date(created_at_str, fuzzy=True)

        # 如果解析结果不包含年份，则设置为当前年份
        if created_at.year == 1900:
            created_at = created_at.replace(year=datetime.now().year)

    user_match = re.search(r'<a href="/u/(\d+)">(.*?)</a>', result[1])
    if user_match:
        user_id = user_match.group(1)
        nickname = user_match.group(2).strip()
    else:
        user_match = re.search(r'<a href="/(.*?)">(.*?)</a>', result[1])
        if user_match:
            user_id = user_match.group(1)  # 使用空字符串表示没有找到用户ID
            nickname = user_match.group(2).strip()
        else:
            raise ValueError("无法提取用户ID和昵称")

    address_match = re.search(r'来自(来自)?(.*?)</span>', result[1])
    if address_match:
        address = address_match.group(2).strip()
    else:
        address = ""  # 如果无法提取地址信息，则使用空字符串表示

    return user_id, comment_id, content, reposts_count, comments_count, attitudes_count, created_at, nickname, address


def scrape_comment_data(comment, connection):
    print('开始')
    """爬取评论数据"""
    bid = comment['bid']
    url = f'https://weibo.cn/comment/{bid}'
    try:
        response = requests.get(url, headers=headers, verify=False)
        print(response.status_code)
        if response.status_code == 200:
            # 提取评论总页数
            total_pages_match = re.search(r'/(\d+)页</div>', response.text)
            if total_pages_match:
                total_pages = int(total_pages_match.group(1))
            else:
                total_pages = 1
            # 逐页爬取评论数据
            for page in range(1, total_pages + 1):
                page_url = f'https://weibo.cn/comment/{bid}?page={page}'
                retry_count = 5  # 重试次数
                while retry_count > 0:
                    try:
                        page_response = requests.get(page_url, headers=headers, verify=False)
                        if page_response.status_code == 200:
                            pattern = re.compile(r'<div class="c" id="C_(\d+)">(.*?)</div>', re.S)
                            results = pattern.findall(page_response.text)
                            if not results:
                                print(f"未能从页面 {page_url} 中提取到评论数据")
                                break  # 跳出当前页的请求，继续下一页的爬取
                            for result in results:
                                try:
                                    data = extract_comment_data(result)
                                    data = (bid, *data)  # 在返回的data元组中添加bid
                                    print(data)
                                    save_data_to_mysql(connection, data)
                                except ValueError as e:
                                    print(f"无法提取评论数据: {e}")
                            else:
                                print(f"已完成页面 {page_url} 中的评论数据爬取")
                                retry_count = 0  # 请求成功，重试次数置为0
                        else:
                            print(f"请求页面 {page_url} 时返回错误代码: {page_response.status_code}")
                            retry_count -= 1
                            if retry_count == 0:
                                print(f"多次重试后无法请求页面 {page_url}")
                            else:
                                print(f"5秒后重新请求页面 {page_url}...")
                                time.sleep(5)
                    except requests.exceptions.RequestException as e:
                        print(f"请求页面 {page_url} 时发生错误: {e}")
                        retry_count -= 1
                        if retry_count == 0:
                            print(f"多次重试后无法请求页面 {page_url}")
                        else:
                            print(f"5秒后重新请求页面 {page_url}...")
                            time.sleep(5)
        else:
            print(f"请求URL {url} 时返回错误代码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"请求URL {url} 时发生错误: {e}")



def main():
    try:
        # 连接MySQL数据库
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        # 检查表是否存在
        if not check_table_exists(connection, BLOG_COMMENT_TABLE_NAME):
            # 表不存在，创建表
            create_blog_comment_table(connection)

        # 获取要爬取的数据
        # weibos = fetch_data_from_mysql(connection)
        weibos = [{'bid': 'N4bAAdZYq', 'user_id': '6136709296'}]
        print(weibos)

        # 使用线程池进行爬取
        pool = ThreadPool(1)  # 设置线程池大小为1
        func = partial(scrape_comment_data, connection=connection)
        pool.map(func, weibos)
        pool.close()
        pool.join()

        # 关闭数据库连接
        connection.close()

    except pymysql.Error as e:
        print(f"MySQL Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
