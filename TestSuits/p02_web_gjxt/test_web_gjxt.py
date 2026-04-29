from Base.baseData import DataDriver
from PageObject.p02_web_gjxt.web_login_page import LoginPage
import pytest
from PageObject.p02_web_gjxt.web_article_page import ArticlePage
from PageObject.p02_web_gjxt.web_file_page import FilePage

class TestCase01():
    """WEB自动化-商城管理系统-登录管理功能模块"""

    @pytest.mark.parametrize('case_data',DataDriver().get_case_data('01登录功能'))
    def test_login_case01(self,driver,case_data):
        """
        WEB自动化用例-用户登录测试
        :return:
        """
        lp = LoginPage()
        lp.login(case_data['username'], case_data['password'])
        lp.assert_login_ok(case_data['flag'])


class TestCase02():
    """WEB自动化-商城管理系统-稿件管理功能模块"""

    @pytest.mark.usefixtures("init_login")
    @pytest.mark.parametrize('case_data',DataDriver().get_case_data('02稿件管理'))
    def test_article_case01(self,driver,init_login,case_data):
        """
        WEB自动化用例-添加稿件测试
        :return:
        """
        ap = ArticlePage()
        ap.add_article(case_data['title'], case_data['content'])
        ap.assert_add_article_ok(case_data['title'])
        ap.assert_add_database_ok(case_data['title'], case_data['content'])

    @pytest.mark.parametrize('case_data',DataDriver().get_case_data('03稿件删除'))
    def test_article_case02(self,driver,init_login,case_data):
        """
        WEB自动化用例-删除稿件测试
        :return:
        """
        ap = ArticlePage()
        ap.add_article(case_data['title'], case_data['content'])
        ap.delete_article()
        ap.assert_delete_article_ok(case_data['title'])
        ap.assert_delete_database_ok([case_data['title']])


    @pytest.mark.parametrize('case_data',DataDriver().get_case_data('04稿件修改'))
    def test_article_case03(self,driver,delete_article,case_data):
        """
        WEB自动化用例-修改稿件测试
        :return:
        """
        ap = ArticlePage()
        ap.add_article(case_data['title'], case_data['content'])
        ap.edit_article(case_data['title'], case_data['content'])
        ap.assert_add_article_ok(case_data['title'])
        ap.assert_add_database_ok(case_data['title'], case_data['content'])

    @pytest.mark.parametrize('case_data',DataDriver().get_case_data('05稿件查询'))
    def test_article_case04(self,driver,delete_article,case_data):
        """
        WEB自动化用例-查询稿件测试
        :return:
        """
        ap = ArticlePage()
        ap.add_article(case_data['title'], case_data['content'])
        ap.select_article(case_data['title'])
        ap.assert_select_article_ok(case_data['title'])
        ap.assert_select_database_ok([case_data['title']])


class TestCase03():
    """WEB自动化-商城管理系统-文档上传下载功能模块"""

    @pytest.mark.usefixtures("init_login")
    @pytest.mark.parametrize('case_data',DataDriver().get_case_data('06文件夹新增和删除'))
    def test_file_case01(self,driver,init_login,case_data):
        """
        WEB自动化用例-文件夹新增和删除测试
        :return:
        """
        fp = FilePage()
        fp.add_folder(case_data['name'], case_data['desc'])
        fp.assert_folder(case_data['name'])
        fp.assert_folder_database(case_data['name'], case_data['desc'])
        fp.delete_folder()
        fp.assert_delete_folder()

    @pytest.mark.parametrize('case_data',DataDriver().get_case_data('07文件上传'))
    def test_file_case02(self,driver,add_del_folder,case_data):
        """
        WEB自动化用例-文件上传测试
        :return:
        """
        fp = FilePage()
        fp.upload_file(case_data['name'], case_data['desc'])
        fp.assert_upload_file(case_data['name'], case_data['desc'])
        fp.assert_upload_file_database(case_data['name'], case_data['desc'])

    @pytest.mark.parametrize('case_data',DataDriver().get_case_data('08文件下载'))
    def test_file_case03(self,driver,add_del_folder,case_data):
        """
        WEB自动化用例-文件下载测试
        :return:
        """
        fp = FilePage()
        fp.upload_file(case_data['name'], case_data['desc'])
        fp.download_file()
        fp.assert_download_file(case_data['name'])