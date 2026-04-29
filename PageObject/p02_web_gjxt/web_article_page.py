from Base.baseAutoWeb import BaseAutoWeb, logger
from Base.baseLogger import BaseLogger
import time
from ExtTools.dbbase import MySqlHelp

logger = BaseLogger('web_article_page.py').get_logger()
class ArticlePage(BaseAutoWeb):
    """
    文章详情页面
    
    WEB 自动化执行错误，有三种方式解决
    1、在元素信息文件中的定位是否正确
    2、自动化执行过程是否过快，元素还没有加载出来，可以适当增加等待时间
    3、元素是否在 iframe 中，如果在 iframe 中，需要切换到 iframe 中才能操作或者切换会外部再来执行
    """
    def __init__(self):
        super().__init__("02稿件管理元素信息")

    def add_article(self, title, content):
        """
        页面添加稿件流程
        :param title: 文章标题
        :param content: 文章内容
        :return:
        """
        logger.info("开始执行添加稿件操作")
        # 点击添加文章按钮
        self.click("article/add_article_btn")
        time.sleep(2)
        # 输入文章标题
        self.send_keys("article/title", title)
        # 输入文章内容
        time.sleep(2)
        self.switch_to_iframe("article/add_iframe")
        self.send_keys("article/content", content)
        time.sleep(2)
        self.switch_to_iframe_out()
        # 点击保存按钮
        self.click("article/save")
        # 查询添加的文章
        time.sleep(2)
        self.click("article/search_btn")
        logger.info("添加稿件操作执行完成")

    def assert_add_article_ok(self,title):
        """
        断言添加稿件页面验证
        :return:
        """
        # 验证页面包含 文章列表 文本
        assert self.get_text("article/first") == title, "【断言】稿件新增验证失败"
        logger.info("【断言】稿件新增验证成功")
        assert self.get_text("article/state") == "不批准", "【断言】稿件新增验证失败"
        logger.info("【断言】稿件状态验证成功")

    def assert_add_database_ok(self,title,content):
        """
        断言添加稿件数据库验证
        :return:
        """
        dbInfo = self.config['数据库配置']
        db = MySqlHelp(host=dbInfo['host'], user=dbInfo['user'], password=dbInfo['password'], database=dbInfo['database'],port=dbInfo['port'])
        res = db.mysql_db_select("select title,content,approved from journalarticle order by createDate desc limit 1")[0]
        print(res)
        assert res[0] == title, "【断言】数据库稿件新增验证失败"
        assert content  in res[1], "【断言】数据库稿件新增验证失败"
        assert res[2] == 0, "【断言】数据库稿件新增验证失败"
        logger.info("【断言】数据库稿件新增验证成功")

    def delete_article(self):
        """
        页面删除稿件流程
        :return:
        """
        logger.info("开始执行删除稿件操作")
        self.click("article/check")
        self.click("article/delete")
        self.is_alert_present().accept()
        time.sleep(2)
        logger.info("删除稿件操作执行完成")

    def assert_delete_article_ok(self,title):
        """
        断言删除稿件页面验证
        :return:
        """
        assert self.get_text("article/first") != title, "【断言】稿件删除验证失败"
        logger.info("【断言】稿件删除验证成功")

    def assert_delete_database_ok(self,title):
        """
        断言删除稿件数据库验证
        :return:
        """
        dbInfo = self.config['数据库配置']
        db = MySqlHelp(host=dbInfo['host'], user=dbInfo['user'], password=dbInfo['password'], database=dbInfo['database'],port=dbInfo['port'])
        res = db.mysql_db_select("select count(*) from journalarticle where title = '{}'".format(title))[0]
        print(res)
        assert res[0] == 0, "【断言】数据库稿件删除验证失败"
        logger.info("【断言】数据库稿件删除验证成功")

    def edit_article(self, title, content):
        """
        页面修改稿件流程
        :param title: 文章标题
        :param content: 文章内容
        :return:
        """
        logger.info("开始执行修改稿件操作")
        self.click("article/edit_first_article")
        time.sleep(2)
        # 文章标题 - 清空输入框内容后再输入
        self.clear("article/title")
        time.sleep(2)
        self.send_keys("article/title", title)
        # 输入文章内容
        time.sleep(2)
        self.switch_to_iframe("article/add_iframe")
        self.clear("article/content")
        self.send_keys("article/content", content)
        time.sleep(2)
        self.switch_to_iframe_out()
        # 点击保存按钮
        self.click("article/save")
        # 查询修改的文章
        time.sleep(2)
        self.click("article/search_btn")
        logger.info("编辑稿件操作执行完成")

    def select_article(self,title):
        """
        页面查询稿件流程
        :param title: 稿件标题
        :return:
        """
        logger.info("开始执行查询稿件操作")
        self.clear("article/select_input")
        self.send_keys("article/select_input", title)
        self.click("article/search_btn")
        self.click("article/check")
        logger.info("查询稿件操作执行完成")

    def assert_select_article_ok(self,title):
        """
        断言查询稿件页面验证
        :return:
        """
        assert self.get_text("article/first") == title, "【断言】稿件查询验证失败"
        logger.info("【断言】稿件查询验证成功")

    def assert_select_database_ok(self,title):
        """
        断言查询稿件数据库验证
        :return:
        """
        dbInfo = self.config['数据库配置']
        db = MySqlHelp(host=dbInfo['host'], user=dbInfo['user'], password=dbInfo['password'], database=dbInfo['database'],port=dbInfo['port'])
        res = db.mysql_db_select("select count(*) from journalarticle where title = '{}'".format(title))[0]
        print(res)
        assert res[0] == 1, "【断言】数据库稿件查询验证失败"
        logger.info("【断言】数据库稿件查询验证成功")









