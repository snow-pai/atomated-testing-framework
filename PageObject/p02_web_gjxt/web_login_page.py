import time
from Base.baseAutoWeb import BaseAutoWeb, logger
from Base.baseLogger import BaseLogger
from Base.basePath import BasePath
from Base.baseUtils import read_config_ini

logger = BaseLogger("web_login_page.py").get_logger()

class LoginPage(BaseAutoWeb):
    """
    登录页面
    """
    def __init__(self):
        super().__init__("01登录页面元素信息")

    def login(self, username, password):
        """
        登录
        :param username:
        :param password:
        :return:
        """
        logger.info("开始执行登录操作")
        self.get_url(read_config_ini(BasePath.CONFIG_FILE)["项目运行设置"]["TEST_URL"])
        time.sleep(2)
        # 输入用户名
        self.clear("login/username")
        self.send_keys("login/username", username)
        time.sleep(2)
        # 输入密码
        self.clear("login/password")
        self.send_keys("login/password", password)
        time.sleep(2)
        # 点击登录按钮
        self.click("login/login_button")
        logger.info("登录操作执行完成")

    def assert_login_ok(self,flag):
        """
        断言登录成功
        :return:
        """
        if flag == "1":
            # 验证页面包含 Products 文本
            assert self.is_text_in_element(("xpath", "//div[contains(@class,'inventory_container')]"), "Products"),"【断言】断言失败"
            logger.info("登录成功")
            # 验证排序下拉框的默认选项
            assert self.get_select_first_option(("id", "header_sort")).text == "Name (A to Z)","【断言】断言失败"
            logger.info("登录成功")
        elif flag == "2":
            # 验证错误提示显示
            error_msg = self.get_attribute(("xpath", "//h3[@data-test='error']"), "innerText")
            assert error_msg, "【断言】应该有错误提示"
            logger.info("验证登录失败成功")
        elif flag == "3":
            # 验证图片加载问题
            img_broken = self.find_element(("xpath", "//img[contains(@src,'/static/media/image-placeholder')]"))
            assert img_broken, "【断言】应该显示图片占位符"
            logger.info("验证登录失败成功")


if __name__ == '__main__':
    from selenium import webdriver
    from TestFramework_po.Base.baseContainer import GlobalVar
    driver = webdriver.Chrome(executable_path=r"/Users/snow/snow-sakura/snow-prject/snow-python/TestFramework_po/Driver/chromedriver")
    GlobalVar().set_var("driver", driver)
    LoginPage().login("admin", "123456")

# if __name__ == '__main__':
#     from selenium import webdriver
#     from selenium.webdriver.chrome.options import Options
#     import os
#     import sys
#     import glob
#     import platform
#     from TestFramework_po.Base.baseContainer import GlobalVar
#
#     # 获取项目根目录
#     project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
#     driver_dir = os.path.join(project_root, 'Driver')
#
#     # 检测操作系统
#     os_name = platform.system()
#     machine = platform.machine()
#     logger.info(f"当前系统：{os_name} {machine}")
#
#     # 查找 chromedriver（优先查找不带 .exe 的文件）
#     chromedriver_path = None
#
#     # macOS/Linux 优先查找不带 .exe 的文件
#     if os_name in ['Darwin', 'Linux']:
#         # 先找不带后缀的
#         if os.path.exists(os.path.join(driver_dir, 'chromedriver')):
#             chromedriver_path = os.path.join(driver_dir, 'chromedriver')
#         # 再找模糊匹配（排除 .exe）
#         else:
#             matches = glob.glob(os.path.join(driver_dir, 'chromedriver*'))
#             for match in matches:
#                 if not match.endswith('.exe'):
#                     chromedriver_path = match
#                     break
#
#     # Windows 查找 .exe 文件
#     if os_name == 'Windows' and not chromedriver_path:
#         if os.path.exists(os.path.join(driver_dir, 'chromedriver.exe')):
#             chromedriver_path = os.path.join(driver_dir, 'chromedriver.exe')
#
#     if not chromedriver_path:
#         logger.error(f"❌ 找不到适合 {os_name} 的 chromedriver")
#         logger.error(f"请在 {driver_dir} 目录中放置正确的 chromedriver 文件")
#         logger.error(f"macOS 用户请下载：https://chromedriver.chromium.org/downloads")
#         logger.error(f"选择对应版本：{'ARM64' if machine == 'arm64' else 'Intel 64'}")
#         sys.exit(1)
#
#     logger.info(f"✅ 使用 chromedriver: {chromedriver_path}")
#
#     # 添加执行权限（macOS/Linux）
#     if os_name in ['Darwin', 'Linux'] and not os.access(chromedriver_path, os.X_OK):
#         os.chmod(chromedriver_path, 0o755)
#         logger.info(f"已添加执行权限：{chromedriver_path}")
#
#     # 配置 Chrome 选项
#     chrome_options = Options()
#
#     # macOS 特殊配置
#     if os_name == 'Darwin':
#         # 禁用沙箱模式（解决 macOS 权限问题）
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--disable-dev-shm-usage')
#         # 禁用 GPU 加速（更稳定）
#         chrome_options.add_argument('--disable-gpu')
#         # 设置窗口大小
#         chrome_options.add_argument('--window-size=1920,1080')
#
#     # 通用配置
#     chrome_options.add_argument('--start-maximized')
#     chrome_options.add_argument('--disable-extensions')
#     chrome_options.add_argument('--disable-infobars')
#
#     try:
#         # 启动 Chrome
#         logger.info("正在启动 Chrome 浏览器...")
#         driver = webdriver.Chrome(
#             executable_path=chromedriver_path,
#             options=chrome_options
#         )
#         logger.info("✅ Chrome 启动成功")
#
#         # 使用单例模式设置全局变量
#         GlobalVar().set_var("driver", driver)
#         LoginPage().login("admin", "123456")
#     except Exception as e:
#         logger.error(f"❌ Chrome 启动失败：{e}")
#         logger.error("\n请检查：")
#         logger.error("1. Chrome 浏览器是否已安装")
#         logger.error("2. Chrome 版本是否与 chromedriver 匹配")
#         logger.error("3. macOS 用户：系统偏好设置 → 安全性与隐私 → 隐私 → 辅助功能 → 添加 Chrome")
#         logger.error("\nChrome 下载地址：https://www.google.com/chrome/")
#         sys.exit(1)
