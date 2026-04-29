import pytest
from PageObject.p02_web_gjxt.web_login_page import LoginPage
from PageObject.p02_web_gjxt.web_article_page import ArticlePage
from PageObject.p02_web_gjxt.web_file_page import FilePage

@pytest.fixture(scope="function")
def init_login():
    """
    稿件系统登录操作
    :return:
    """
    lp = LoginPage()
    lp.login("standard_user", "secret_sauce")

@pytest.fixture(scope="function")
def delete_article():
    """
    稿件系统删除稿件操作
    :return:
    """
    lp = LoginPage()
    lp.login("standard_user", "secret_sauce")
    yield
    ap = ArticlePage()
    ap.delete_article()

@pytest.fixture(scope="function")
def add_del_folder():
    """
    文件系统添加删除文件夹操作
    :return:
    """
    lp = LoginPage()
    lp.login("standard_user", "secret_sauce")
    fp = FilePage()
    fp.add_folder("name", "desc")
    yield
    fp.delete_folder()