import os.path
import re

from click import style

from Base.baseAutoHttp import BaseAutoHttp
from Base.baseLogger import BaseLogger
from ExtTools.dbbase import MySqlHelp
from Base.basePath import BasePath

logger = BaseLogger("api_file_page.py").get_logger()

class APIFilePage(BaseAutoHttp):
    """
    文件接口
    """
    def __init__(self):
        super().__init__("03文件上传下载接口信息")


    def add_folder(self,name,desc):
        """
        添加上传文件夹接口请求方法
        :param name: 文件夹名称
        :param desc: 文件夹描述
        :return:
        """
        change_data = {
            "folderName": name,
            "folderDescription": desc
        }
        res = self.request_base("add_folder", change_data=change_data)
        return res.text

    def select_folder(self,name):
        """
        查询上传文件夹接口请求方法
        :param name: 文件夹名称
        :return:
        """
        result = self.request_base("select_folder")
        re_info = re.findall('2Fdocument_Library%2Fview&_20_folderId=(.*?)">(.*?)</a>',result.text)
        return re_info

    def assert_add_folder_ok(self,name):
        """
        添加上传文件夹接口断言方法
        :param name: 文件夹名称
        :return:
        """
        res = self.select_folder(name)[0]
        assert name in res, "【断言】添加上传文件夹接口验证失败"
        logger.info("【断言】添加上传文件夹接口验证成功")

    def assert_add_folder_database_ok(self,name,desc):
        """
        添加上传文件夹接口数据库断言方法
        :param name: 文件夹名称
        :param desc: 文件夹描述
        :return:
        """
        dbInfo = self.config['数据库配置']
        db = MySqlHelp(host=dbInfo['host'], user=dbInfo['user'], password=dbInfo['password'],
                       database=dbInfo['database'], port=dbInfo['port'])
        result = db.mysql_db_select("select name,description from dlfolder order by createDate limit 1")[0]
        assert result[0] == name, "【断言】添加上传文件夹接口数据库验证失败"
        assert result[1] == desc, "【断言】添加上传文件夹接口数据库验证失败"
        logger.info("【断言】添加上传文件夹接口数据库验证成功")

    def delete_folder(self,name):
        """
        删除上传文件夹接口请求方法
        :param name: 文件夹名称
        :return:
        """
        res = self.select_folder()
        id = None
        for i in res:
            if name in i:
                id = i[0]
        change_data = {
            "folderId": id
        }
        res = self.request_base("delete_folder", change_data=change_data)
        return res.text

    def assert_delete_folder_ok(self,name):
        """
        删除上传文件夹接口断言方法
        :param name: 文件夹名称
        :return:
        """
        res = self.select_folder()
        assert name not in str(res), "【断言】删除上传文件夹接口验证失败"
        logger.info("【断言】删除上传文件夹接口验证成功")

    def upload_file(self,name,desc):
        """
        上传文件接口请求方法
        :param name:文件名称
        :param desc:文件描述
        :param file_path: 文件路径
        :return:
        """
        folder_id = self.select_folder()[0][0]
        change_data = {
            "title": name,
            "description": desc,
            "folderId": folder_id,

        }
        file_path = os.path.join(BasePath.TEMP_PATH, "upload_file.txt")
        file = {
            "_20_file": ("upload_file.txt", open(file_path, "r", encoding="utf-8","text/plain"))
        }
        res = self.request_base("upload_file", change_data=change_data, files=file)
        return res.text

    def assert_upload_file_ok(self,res,name):
        """
        上传文件接口断言方法
        :param res:上传的文件内容
        :return:
        """
        name = re.findall('id="_20_title" name="_20_title" style="width: 350px" type="text" value="(.*?)"',res)[0]
        assert name == name, "【断言】上传文件接口验证失败"
        logger.info("【断言】上传文件接口验证成功")

    def assert_upload_file_database_ok(self,name,desc):
        """
        上传文件接口数据库断言方法
        :param name: 文件名称
        :param desc: 文件描述
        :return:
        """
        dbInfo = self.config['数据库配置']
        db = MySqlHelp(host=dbInfo['host'], user=dbInfo['user'], password=dbInfo['password'],
                       database=dbInfo['database'], port=dbInfo['port'])
        result = db.mysql_db_select("select name,description from DLFileEntry order by createDate limit 1")[0]
        assert result[0] == name.split(".")[0], "【断言】上传文件接口数据库验证失败"
        assert result[1] == desc, "【断言】上传文件接口数据库验证失败"
        logger.info("【断言】上传文件接口数据库验证成功")

    def select_file(self,keywords):
        """
        查询上传文件接口请求方法
        :param keywords: 关键字
        :return:
        """
        folder_id = self.select_folder()[0][0]
        change_data = {
            "folderId": folder_id,
            "keywords": keywords.split(".")[0]
        }
        res = self.request_base("select_file", change_data=change_data)
        return res.text

    def download_file(self,res,name):
        """
        下载文件接口请求方法
        :param name: 文件名称
        :return:
        """
        res = re.findall('&_20_foLderId=(.*?)&_20_name=(.*?)">',res)[0]
        change_data = {
            "folderId": res[0],
            "name": res[1]
        }
        self.request_base("download_files", change_data=change_data)
        file_path = os.path.join(BasePath.TEMP_PATH,name)
        with open(file_path, "wb") as f:
            f.write(res.content)

    def assert_download_file_ok(self,name):
        """
        下载文件接口断言方法
        :param name: 文件名称
        :return:
        """
        file_path = os.path.join(BasePath.TEMP_PATH, name)
        assert os.path.exists(file_path), "【断言】下载文件接口验证失败"
        logger.info("【断言】下载文件接口验证成功")










