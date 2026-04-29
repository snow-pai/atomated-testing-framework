from symbol import yield_expr

import pytest
from PageObject.p03_http_gjxt.api_login_page import LoginPage
from PageObject.p03_http_gjxt.api_article_page import APIArticlePage
from PageObject.p03_http_gjxt.api_file_page import APIFilePage


@pytest.fixture(scope="function")
def init_login():
    """
    稿件系统登录操作
    :return:
    """
    lp = LoginPage()
    lp.login("standard_user", "secret_sauce")

@pytest.fixture(scope="function")
def article_add_delete(request):
    """
    稿件系统添加删除稿件操作
    :return:
    """
    case_data = request.params
    lp = LoginPage()
    lp.login("standard_user", "secret_sauce")
    ap = APIArticlePage()
    ap.add_article(case_data['title'], case_data['content'])
    yield case_data
    ap.delete_article(case_data['title'])

@pytest.fixture(scope="function")
@pytest.mark.parametrize('case_data',DataDriver().get_case_data('06文件夹新增和删除'))
def folder_add_delete(case_data):
    """
    稿件系统添加删除文件夹操作
    :return:
    """
    lp = LoginPage()
    lp.login("standard_user", "secret_sauce")
    af = APIFilePage()
    af.add_folder(case_data['name'], case_data['desc']])
    yield
    af.delete_folder(case_data['name'])