import re
from Base.baseAutoHttp import BaseAutoHttp, logger
from Base.baseLogger import BaseLogger
from ExtTools.dbbase import MySqlHelp
logger = BaseLogger("api_article_page.py").get_logger()

class APIArticlePage(BaseAutoHttp):
    """
    文章接口
    """
    def __init__(self):
        super().__init__("02稿件管理接口信息")

    def add_article(self, title, content):
        """
        添加文章接口请求方法
        :param title: 文章标题
        :param content: 文章内容
        :return:
        """
        change_data = {
            "title": title,
            "content": content
        }
        res = self.request_base("add_api", change_data=change_data)
        return res.text

    def select_article(self, title=''):
        """
        查询文章接口请求方法
        :param title:
        :return:
        """
        change_data = {
            "title": title
        }
        res = self.request_base("select_api", change_data=change_data)
        re_info = re.findall('_15_version=1.0">(.*?)</a>', res.text)[:7]
        # print(re_info)
        return re_info

    def assert_add_article_ok(self, title):
        """
        添加文章接口断言方法
        :param title:
        :return:
        """
        res = self.select_article(title)
        assert res[1] == title, "【断言】添加文章接口验证失败"
        print("【断言】添加文章接口验证成功")
        logger.info("【断言】添加文章接口验证成功")
        assert res[3] == "不批准", "【断言】添加文章接口验证失败"
        logger.info("【断言】添加文章接口验证成功")

    def assert_add_article_database_ok(self, title, content):
        """
        添加文章接口数据库断言方法
        :param title:
        :param content:
        :return:
        """
        dbInfo = self.config['数据库配置']
        db = MySqlHelp(host=dbInfo['host'], user=dbInfo['user'], password=dbInfo['password'],
                       database=dbInfo['database'], port=dbInfo['port'])
        result = db.mysql_db_select("SELECT title,content,approved FROM journalarticle order by createDate desc limit 1")[0]
        assert result[0] == title, "【断言】添加文章接口数据库验证失败:{}".format(title)
        logger.info("【断言】添加文章接口数据库验证成功:{}".format(title))
        assert result[1] == content, "【断言】添加文章接口数据库验证失败:{}".format(content)
        logger.info("【断言】添加文章接口数据库验证成功:{}".format(content))
        assert result[2] == 0, "【断言】添加文章接口数据库验证失败:0"
        logger.info("【断言】添加文章接口数据库验证成功:0")

    def delete_article(self,title):
        """
        删除文章接口请求方法
        :return:
        """
        id = self.select_article(title)[0]
        change_data = {
            "_15_deleteArticleIds": "{}_version_1.0".format(id),
            "_15_rowIds": "{}_version_1.0".format(id)
        }
        res = self.request_base("delete_api", change_data=change_data)
        return res.text

    def assert_delete_article_ok(self,title):
        """
        删除文章接口断言方法
        :return:
        """
        res = self.select_article(title)
        assert res == [], "【断言】删除文章接口验证失败"
        print("【断言】删除文章接口验证成功")
        logger.info("【断言】删除文章接口验证成功")

    def assert_delete_article_database_ok(self,title):
        """
        删除文章接口数据库断言方法
        :return:
        """
        dbInfo = self.config['数据库配置']
        db = MySqlHelp(host=dbInfo['host'], user=dbInfo['user'], password=dbInfo['password'],
                       database=dbInfo['database'], port=dbInfo['port'])
        result = db.mysql_db_select("SELECT count(*) FROM journalarticle where title='{}'".format(title))[0]
        assert result[0] == 0, "【断言】删除文章接口数据库验证失败"
        logger.info("【断言】删除文章接口数据库验证成功")

    def edit_article(self,title,content):
        """
        修改文章接口请求方法
        :param title:
        :param content:
        :return:
        """
        id = self.select_article(title)[0]
        change_data = {
            "title": title,
            "content": content,
            "articleId": id,
            "deleteArticleIds": "{}_version_1.0".format(id),
            "expireArticleIds": "{}_version_1.0".format(id)
        }
        res = self.request_base("edit_api", change_data=change_data)
        return res.text

    def assert_select_article_ok(self, res, title):
        """
        查询文章接口断言方法
        :param res:
        :param title:
        :return:
        """
        assert res[1] == title, "【断言】查询文章接口验证失败"
        logger.info("【断言】查询文章接口验证成功")

    def assert_select_article_database_ok(self,title):
        """
        查询文章接口数据库断言方法
        :return:
        """
        dbInfo = self.config['数据库配置']
        db = MySqlHelp(host=dbInfo['host'], user=dbInfo['user'], password=dbInfo['password'],
                       database=dbInfo['database'], port=dbInfo['port'])
        result = db.mysql_db_select("SELECT count(*) FROM journalarticle where title='{}'".format(title))[0]
        assert result[0] == 1, "【断言】查询文章接口数据库验证失败"
        logger.info("【断言】查询文章接口数据库验证成功")




















