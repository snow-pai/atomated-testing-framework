from Base.baseData import DataDriver
from PageObject.p03_http_gjxt.api_article_page import APIArticlePage
from PageObject.p03_http_gjxt.api_login_page import LoginPage
from PageObject.p03_http_gjxt.api_file_page import APIFilePage
import pytest

class TestApiCase01():
    """
    接口自动化-稿件管理系统-登录功能模块
    """
    @pytest.mark.parametrize('case_data',DataDriver().get_case_data('01稿件系统登录'))
    def test_api_login_case01(self,case_data):
        """
        接口自动化用例-用户登录测试
        :return:
        """
        lp = LoginPage()
        res = lp.login(case_data['username'], case_data['password'])
        lp.assert_login_ok(res, case_data['title'])

class TestApiCase02():
    """
    接口自动化-稿件管理系统-稿件管理模块
    """
    @pytest.mark.usefixtures("init_login")
    @pytest.mark.parametrize('case_data',DataDriver().get_case_data('02稿件新增'))
    def test_api_article_add_case(self,case_data):
        """
        接口自动化用例-稿件新增测试
        :return:
        """
        ap = APIArticlePage()
        ap.add_article(case_data['title'], case_data['content'])
        ap.assert_add_article_ok(case_data['title'])
        ap.assert_add_article_database_ok(case_data['title'], case_data['content'])

    @pytest.mark.usefixtures("init_login")
    @pytest.mark.parametrize('case_data',DataDriver().get_case_data('03稿件删除'))
    def test_api_article_delete_case(self,case_data):
        """
        接口自动化用例-稿件删除测试
        :return:
        """
        ap = APIArticlePage()
        ap.add_article(case_data['title'], case_data['content'])
        ap.delete_article(case_data['title'])
        ap.assert_delete_article_ok(case_data['title'])
        ap.assert_delete_article_database_ok(case_data['title'])

    @pytest.mark.parametrize('article_add_delete',DataDriver().get_case_data('04稿件修改'),indirect=True)
    def test_api_article_edit_case(self,article_add_delete):
        """
        接口自动化用例-稿件修改测试
        :return:
        """
        ap = APIArticlePage()
        ap.edit_article(article_add_delete['title'], article_add_delete['content'])
        ap.assert_add_article_ok(article_add_delete['title'])
        ap.assert_add_article_database_ok(article_add_delete['title'], article_add_delete['content'])

    @pytest.mark.parametrize('article_add_delete',DataDriver().get_case_data('05稿件查询'),indirect=True)
    def test_api_article_select_case(self,article_add_delete):
        """
        接口自动化用例-稿件查询测试
        :return:
        """
        ap = APIArticlePage()
        res = ap.select_article(article_add_delete['title'])
        ap.assert_select_article_ok(res, article_add_delete['title'])
        ap.assert_select_article_database_ok(article_add_delete['title'])

class TestApiCase03():
    """
    接口自动化-稿件管理系统-文件上传下载功能模块
    """
    @pytest.mark.usefixtures("init_login")
    @pytest.mark.parametrize('case_data',DataDriver().get_case_data('06文件夹新增和删除'))
    def test_api_folder_add_case(self,case_data):
        """
        接口自动化用例-文件夹操作测试
        :return:
        """
        af = APIFilePage()
        af.add_folder(case_data['name'], case_data['desc'])
        af.assert_add_folder_ok(case_data['name'])
        af.assert_add_folder_database_ok(case_data['name'], case_data['desc'])
        af.delete_folder(case_data['name'])
        af.assert_delete_folder_ok(case_data['name'])

    @pytest.mark.usefixtures("folder_add_delete")
    @pytest.mark.parametrize('case_data',DataDriver().get_case_data('07文件上传'))
    def test_api_file_upload_case(self,case_data):
        """
        接口自动化用例-文件上传测试
        :return:
        """
        af = APIFilePage()
        res = af.upload_file(case_data['name'], case_data['desc'])
        af.assert_upload_file_ok(res, case_data['name'])
        af.assert_upload_file_database_ok(case_data['name'], case_data['desc'])

    @pytest.mark.usefixtures("folder_add_delete")
    @pytest.mark.parametrize('case_data',DataDriver().get_case_data('08文件下载'))
    def test_api_file_download_case(self,case_data):
        """
        接口自动化用例-文件下载测试
        :return:
        """
        af = APIFilePage()
        af.upload_file(case_data['name'], case_data['desc'])
        res = af.select_file(case_data['name'])
        af.download_file(res, case_data['name'])
        af.assert_download_file_ok(case_data['name'])












