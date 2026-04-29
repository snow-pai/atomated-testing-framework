import re
from Base.baseAutoHttp import BaseAutoHttp
from Base.baseLogger import BaseLogger

logger = BaseLogger("api_login_page.py").get_logger()

class LoginPage(BaseAutoHttp):
    """
    登录接口
    """
    def __init__(self):
        super().__init__("01登录页面接口信息")

    def login(self, username, password):
        """
        登录接口请求方法
        :param username: 用户名
        :param password: 密码
        :return:
        """
        self.request_base("home_api")
        change_data = {
            "_58_login": username,
            "_58_password": password
        }
        res = self.request_base("login_api", change_data = change_data)
        return  res.text

    def assert_login_ok(self,res,title):
        """
        登录接口断言方法
        :param res: 登录接口响应结果
        :return:
        """
        page_title = re.findall("<title>(.*?)</title>", res)[0]
        assert page_title == title, "【断言】登录接口验证失败"
        logger.info("【断言】登录接口验证成功")