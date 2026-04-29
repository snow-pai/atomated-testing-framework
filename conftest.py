import sys
import os

from openpyxl.styles.builtins import output

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import base64
import pytest
from datetime import datetime
from io import BytesIO
from py.xml import html
from Base.baseUtils import *
from Base.basePath import BasePath as BP
from Base.baseContainer import GlobalVar
from Base.baseYaml import write_yaml

config = read_config_ini(BP.CONFIG_FILE)
gm = GlobalVar()
gm.set_var('CONFIG_INFO', config)
insert_js_html = False


def pytest_addoption(parser):

    '''添加命令行参数--browser、--host'''
    parser.addoption(
        "--browser", action="store", default=config['WEB自动化配置']['browser'], help="browser option:firefox or chrome or ie")

    # 添加host参数，设置默认测试环境地址
    parser.addoption(
        "--host", action="store", default=config['项目运行设置']['test_url'], help="test host ->http://192.168.1.1:8080")

@pytest.fixture(scope="function")
def driver(request):
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        name = request.config.getoption("--browser")
        _driver = None
        # 统一转为小写，兼容配置文件的大小写
        browser_name = name.lower() if name else ""
        print(f"\n尝试启动浏览器：{name} (标准化后：{browser_name})")
        print(f"当前系统：darwin arm64")
        
        if browser_name == "chrome":
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            driver_path = os.path.join(BP.DRIVER_PATH, "chromedriver")
            print(f"ChromeDriver 路径：{driver_path}")
            _driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
        elif name == "chromeheadless":
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            driver_path = os.path.join(BP.DRIVER_PATH, "chromedriver")
            print(f"ChromeDriver 路径：{driver_path}")
            _driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
            _driver.set_window_size(1920,1080)
        elif name == "firefox":
            _driver = webdriver.Firefox(executable_path=os.path.join(BP.DRIVER_PATH, "geckodriver.exe"))
        elif name == "ie":
            _driver = webdriver.Ie(executable_path=os.path.join(BP.DRIVER_PATH, "IEDriverServer.exe"))
        elif name == "edge":
            _driver = webdriver.Edge(executable_path=os.path.join(BP.DRIVER_PATH, "msedgedriver.exe"))
        elif name == "safari":
            _driver = webdriver.Safari()
        
        if _driver is None:
            raise Exception(f"浏览器 '{name}' 启动失败，_driver 为 None")
        
        GlobalVar().set_var("driver", _driver)
        _driver.implicitly_wait(10)
        print(f"✅ 浏览器启动成功：{name}")
        def fn():
            print("当全部用例执行完之后：teardown quit driver!")
            _driver.quit()
        request.addfinalizer(fn)
        return _driver
    except ImportError as e:
        print(f"❌ ImportError: {e}")
        pytest.exit(f"未安装 selenium: {e}")
    except Exception as e:
        print(f"❌ 启动失败详情：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        pytest.exit(f"启动 webdriver 错误：{e}")

## 摘要信息
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("自动化测试工程师1：工具人1")])

## 测试结果
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th("description")) # 插入列 1代表列的索引 如0,1,2
    cells.pop()

def pytest_html_results_table_row(report, cells):
   if hasattr(report, "description"):
       cells.insert(1, html.td(report.description))
       cells.pop()
   else:
       print("没有描述信息",report.longreprtext)

def _capture_screenshot_sel():
    '''WEB自动化截图'''
    driver = GlobalVar().get_var("driver")
    if not driver:
        pytest.exit("driver 获取为空")
    driver.get_screenshot_as_file(os.path.join(BP.SCREENSHOT_PIC))
    return driver.get_screenshot_as_base64()

def _capture_screenshot_pil():
    '''客户端自动化截图'''
    try:
        from PIL import ImageGrab
        output_buffer = BytesIO()
        img = ImageGrab.grab()
        img.save(BP.SCREENSHOT_PIC)
        img.save(output_buffer, format='png')
        bytes_value = output_buffer.getvalue()
        output_buffer.close()
        return base64.b64encode(bytes_value).decode()
    except ImportError:
        pytest.exit("未安装PIL")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    '''当测试失败的时候，自动截图展示到html报告中'''
    outcome = yield
    pytest_html = item.config.pluginmanager.getplugin("html")
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        if config['项目运行设置']['AUTO_TYPE'] == "WEB":
            screen_img = _capture_screenshot_sel()
        elif config['项目运行设置']['AUTO_TYPE'] == "CLIENT":
            screen_img = _capture_screenshot_pil()
        else:
            screen_img = None
        if (report.skipped and xfail) or (report.failed and not xfail) and screen_img:
            file_name = report.nodeid.replace("::", "_") + ".png"
            if config['项目运行设置']['REPORT_TYPE'] == 'HTML':
                if file_name:
                    html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px; height:auto; max-height:400px; object-fit:contain; cursor:pointer;" onclick="lookimg(this.src)" align="right"></div>' % screen_img
                    script = '''
                    <script>
                        function lookimg(str){
                            var newin = window.open();
                            newin.document.write("<img src='+str+'/>");
                        }
                    </script>
                    '''
                    extra.append(pytest_html.extras.html(html))
                    if not insert_js_html:
                        extra.append(pytest_html.extras.html(script))
            elif config['项目运行设置']['REPORT_TYPE'] == 'ALLURE':
                import allure
                with allure.step("添加失败截图..."):
                    allure.attach.file(BP.SCREENSHOT_PIC,"失败截图", allure.attachment_type.PNG)
    report.extra = extra
    report.description = str(item.function.__doc__)

def pytest_collection_modifyitems(session, config, items):
    '''收集用例后写入 testcases.yaml'''
    print(f'\n=== pytest_collection_modifyitems 被调用 ===')
    print(f'收集到的用例数量：{len(items)}')
    
    testcases = {}
    for item in items:
        print(f'处理用例：{item.nodeid}')
        case_class_name = '::'.join(item.nodeid.split('::')[0:2])
        case_name = item.nodeid.split('::')[-1]
        if not testcases.get(case_class_name, None):
            testcases[case_class_name] = {}
        if not testcases[case_class_name].get('comment', None):
            testcases[case_class_name]['comment'] = item.cls.__doc__
        testcases[case_class_name][case_name] = item.function.__doc__
    
    print(f'生成的 testcases: {testcases}')
    
    # 写入 testcases.yaml
    testcases_path = BP.TESTCASES
    write_yaml(testcases_path, testcases)
    print(f'已写入文件：{testcases_path}')
    print('=== 用例收集完成 ===\n')