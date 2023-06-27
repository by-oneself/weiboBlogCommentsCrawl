# Weibo Comment Crawler

[English](README_EN.md) | [中文](README.md)

**Disclaimer: This script is intended for educational and research purposes only. It is strictly prohibited to use it for any commercial or illegal activities. The author is not responsible for any issues or illegal actions that may arise from using this script. Please use it in compliance with applicable laws and regulations.**

This is a Python script for crawling comments from Weibo using the Weibo API. The script retrieves blog data from a MySQL database and then retrieves comments for each blog post and saves them back to the database.

## Dependencies

To run this script, you need to install the following dependencies:

- PyMySQL~=1.0.3: Used for connecting to and operating on the MySQL database.
- requests~=2.31.0: Used for sending HTTP requests and retrieving web data.
- python-dateutil~=2.8.2: Used for parsing dates and times.

## File Structure

The project includes the following files:

- `main.py`: The main script file that contains the logic for retrieving blog data from the MySQL database, crawling comment data, and saving it back to the database.
- `setting.py`: Configuration file that includes MySQL database and request header configurations.
- `requirements.txt`: Contains a list of project dependencies.

## Configuration

Before running the script, you need to make some configurations:

1. In the `setting.py` file, modify the following variables based on your MySQL database settings:
   - `MYSQL_HOST`: Host address of the MySQL database.
   - `MYSQL_PORT`: Port number of the MySQL database.
   - `MYSQL_USER`: Username of the MySQL database.
   - `MYSQL_PASSWORD`: Password of the MySQL database.
   - `MYSQL_DATABASE`: The name of the database to use.
   - `WEIBO_BLOG_TABLE_NAME`: The table name for storing blog data.
   - `BLOG_COMMENT_TABLE_NAME`: The table name for storing comment data.
   - `WEIBO_COOKIE`: Your Weibo login cookie. Please ensure that it has sufficient permissions to access comment data.

2. If you need to modify other request header parameters, modify the `HEADERS` variable accordingly.

## Usage

1. Ensure that you have correctly configured the MySQL database and request headers.

2. Install the project dependencies. You can use the following command to install the required packages:

   ```shell
   pip install -r requirements.txt
   ```

3. Run the `main.py` script. Execute the following command:

   ```shell
   python main.py
   ```

   The script will retrieve blog data from the MySQL database, crawl comment data for each blog post, and save it back to the database.

   Note: Due to the limitations of the Weibo API, it may take some time to retrieve the complete comment data, especially for a large number of blog posts. The script uses multi-threading to speed up the crawling process with 1 thread as the default.

4. Check the output information to monitor the crawling progress and any potential errors.

5. After the crawling is complete, you can view the table in the MySQL database where the comment data is stored.

## Notes

- To use this script for crawling Weibo comment data, you need to provide a valid Weibo login cookie to ensure that you have permission to access the comment data. Please make sure that your cookie is valid and has sufficient permissions to access the required comment data.
- Crawling comment data may be subject to limitations imposed by the Weibo API, such as hourly request limits. Please adjust and control accordingly to avoid triggering limitations or bans from the Weibo API.
- Please note that Weibo may make changes to its API or restrict access, so the availability and stability of this script may be affected.

## Disclaimer

The use of this script requires adherence to the following points:

1. The use of this script is at your own risk. The author is not

 responsible for the usage, functionality, and results of the script.
2. Please ensure that your usage complies with applicable laws and regulations and adhere to Weibo's terms of use and privacy policy. Be mindful not to infringe upon the rights of others.
3. Please exercise caution and avoid abusing this script to avoid placing excessive load on Weibo servers or impacting the normal usage of other users.
4. The author recommends that you carefully read and understand Weibo's relevant regulations before using this script and ensure that your operations are legal and compliant.

If you decide to use this script, please ensure your own legality and responsibility and bear the corresponding risks.

For any questions or inquiries, please contact the author at [2546406321@qq.com].