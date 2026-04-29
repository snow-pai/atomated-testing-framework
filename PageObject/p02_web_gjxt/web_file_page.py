import os

from Base.baseAutoWeb import BaseAutoWeb
from Base.baseLogger import BaseLogger
import time
from ExtTools.dbbase import MySqlHelp
from Base.basePath import BasePath
import pyautogui
logger = BaseLogger("web_file_page.py").get_logger()

class FilePage(BaseAutoWeb):

    """
    文件上传页面
    """
    def __init__(self):
        super().__init__("03文件上传下载元素信息")

    def add_folder(self, name, desc):
        """
        添加文件夹
        :param name: 文件夹名称
        :param desc: 文件夹描述
        :return:
        """
        logger.info("开始执行添加文件夹操作")
        self.click("file/file_page")
        time.sleep(2)
        self.click("file/add_btn")
        time.sleep(2)
        self.send_keys("file/folder_name", name)
        self.send_keys("file/folder_desc", desc)
        self.click("file/save_folder")
        logger.info("添加文件夹操作执行完成")

    def assert_folder(self, name):
        """
        断言文件夹新增页面验证
        :param name: 文件夹名称
        :return:
        """
        assert self.get_text("file/first_name") == name, "【断言】文件夹新增验证失败"
        logger.info("【断言】文件夹新增验证成功")

    def assert_folder_database(self, name, desc):
        """
        断言文件夹新增数据库验证
        :param name: 文件夹名称
        :param desc: 文件夹描述
        :return:
        """
        dbInfo = self.config['数据库配置']
        db = MySqlHelp(host=dbInfo['host'], user=dbInfo['user'], password=dbInfo['password'],
                       database=dbInfo['database'], port=dbInfo['port'])
        result = db.mysql_db_select("SELECT name,description FROM dlfolder order by createDate desc limit 1")[0]
        assert result[0] == name, "【断言】文件夹新增数据库验证失败"
        assert result[1] == desc, "【断言】文件夹新增数据库验证失败"
        logger.info("【断言】文件夹新增数据库验证成功")

    def delete_folder(self):
        """
        删除文件夹
        :return:
        """
        logger.info("开始执行删除文件夹操作")
        self.click("file/file_page")
        time.sleep(2)
        self.click("file/first_del")
        self.is_alert_present().accept()
        logger.info("删除文件夹操作执行完成")

    def assert_delete_folder(self, name):
        """
        断言文件夹删除页面验证
        :param name: 文件夹名称
        :return:
        """
        assert self.get_text("file/msg_success") == "您的请求执行成功。", "【断言】文件夹删除页面验证失败"
        logger.info("【断言】文件夹删除页面验证成功")

    def upload_file(self, name, desc):
            """
            上传文件
            :param name: 重命名文件名称
            :param desc: 文件描述
            :return:
            """
            logger.info("开始执行上传文件操作")
            self.click("file/file_page")
            time.sleep(2)
            self.click("file/upload_btn")
            time.sleep(2)
            self.switch_to_iframe("file/iFrame_file")
            file_path = os.path.join(BasePath.TEMP_PATH,"upload_file.txt")
            self.send_keys("file/input_file", file_path)
            self.send_keys("file/rename_file", name)
            self.send_keys("file/desc_file", desc)
            self.click("file/sub_file")
            self.switch_to_iframe_out()
            logger.info("上传文件操作执行完成")

    def assert_upload_file(self, name, desc):
        """
        断言文件上传页面验证
        :param name: 重命名文件名称
        :param desc: 文件描述
        :return:
        """
        file_info = self.get_text("file/first_file")
        assert file_info.split("\n")[0] == name, "【断言】文件上传页面验证失败"
        assert file_info.split("\n")[1] == desc, "【断言】文件上传页面验证失败"
        logger.info("【断言】文件上传页面验证成功")

    def assert_upload_file_database(self, name, desc):
        """
        断言文件上传数据库验证
        :param name: 重命名文件名称
        :param desc: 文件描述
        :return:
        """
        dbInfo = self.config['数据库配置']
        db = MySqlHelp(host=dbInfo['host'], user=dbInfo['user'], password=dbInfo['password'],
                       database=dbInfo['database'], port=dbInfo['port'])
        result = db.mysql_db_select("SELECT title,description FROM dlfileentry order by createDate desc limit 1")[0]
        assert result[0] == name.split(".")[0], "【断言】文件上传数据库验证失败"
        assert result[1] == desc, "【断言】文件上传数据库验证失败"
        logger.info("【断言】文件上传数据库验证成功")

    def download_file(self):
        """
        下载文件
        :return:
        """
        logger.info("开始执行下载文件操作")
        # self.click("file/first_file")
        url = self.get_attribute("file/first_file", "href")
        self.get_url(url)
        time.sleep(2)
        pyautogui.hotkey("alt", "s")
        time.sleep(2)
        logger.info("下载文件操作执行完成")

    def assert_download_file(self, name):
        """
        断言文件下载验证
        :param name: 重命名文件名称
        :return:
        """
        # download_path = r"C:\Users\Administrator\Downloads"
        download_path = r"/Users/snow/Downloads"
        file_path = os.path.join(download_path,name)
        assert os.path.exists(file_path), "【断言】文件下载验证失败"
        logger.info("【断言】文件下载验证成功")
        for file in os.listdir(download_path):
            path_all = os.path.join(download_path, file)
            os.unlink(path_all)






