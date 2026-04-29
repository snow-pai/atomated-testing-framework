import os

class BasePath(object):

    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIG_PATH = os.path.join(PROJECT_ROOT, 'Config')
    CONFIG_FILE = os.path.join(CONFIG_PATH, '配置文件.ini')
    DATA_PATH = os.path.join(PROJECT_ROOT, 'Data')
    DATA_DRIVER_PATH = os.path.join(DATA_PATH, 'DataDriver')
    DATA_ELEMENT_PATH = os.path.join(DATA_PATH, 'DataElement')
    TEMP_PATH = os.path.join(DATA_PATH, 'Temp')
    SCREENSHOT_PATH = os.path.join(TEMP_PATH, 'Screenshots')
    SCREENSHOT_PIC = os.path.join(SCREENSHOT_PATH, 'error_pic.png')
    DRIVER_PATH = os.path.join(PROJECT_ROOT, 'Driver')
    LOG_PATH = os.path.join(PROJECT_ROOT, 'Log')
    REPORT_PATH = os.path.join(PROJECT_ROOT, 'Reports')
    ALLURE_PATH = os.path.join(REPORT_PATH, 'ALLURE')
    ALLURE_REPORT_PATH = os.path.join(ALLURE_PATH, 'Report')
    ALLURE_RESULT_PATH = os.path.join(ALLURE_PATH, 'Result')
    HTML_PATH = os.path.join(REPORT_PATH, 'HTML')
    XML_PATH = os.path.join(REPORT_PATH, 'XML')
    TEST_SUIT_DIR = os.path.join(PROJECT_ROOT, 'TestSuits')
    TESTCASES = os.path.join(TEMP_PATH, 'testcases.yaml')
    TEMPCASES = os.path.join(TEMP_PATH, 'tempcases.yaml')

if __name__ == '__main__':
    print(BasePath.DATA_DRIVER_PATH)