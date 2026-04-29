import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(PROJECT_ROOT, 'TestFramework_po'))
import pytest
from Base.basePath import BasePath as BP
from Base.baseUtils import read_config_ini,file_all_dele
from Base.baseContainer import GlobalVar
from Base.baseSendEmail import HandleEmail

config = read_config_ini(BP.CONFIG_FILE)
gm = GlobalVar()
gm.set_var('CONFIG_INFO', config)
gm.set_var('DATA_DRIVER_PATH',os.path.join(BP.DATA_DRIVER_PATH,config['项目运行设置']['DATA_DRIVER_TYPE']))


def run_main():
    config = gm.get_var('CONFIG_INFO')['项目运行设置']
    test_case = os.path.join(BP.TEST_SUIT_DIR,config['TEST_PROJECT_NAME'])
    if config['REPORT_TYPE'] == 'ALLURE':
        pytest.main(['-s','-v','--alluredir={}'.format(BP.ALLURE_RESULT_PATH),test_case])
        os.system('allure generate {} -o {} --clean'.format(BP.ALLURE_RESULT_PATH, BP.ALLURE_REPORT_PATH))
        file_all_dele(BP.ALLURE_RESULT_PATH)
    elif config['REPORT_TYPE'] == 'HTML':
        report_path = os.path.join(BP.HTML_PATH, 'auto_reports.html')
        pytest.main(['-s','-v','--html={}'.format(report_path),'--self-contained-html',test_case])
    elif config['REPORT_TYPE'] == 'XML':
        report_path = os.path.join(BP.XML_PATH, 'auto_reports.xml')
        pytest.main(['-s','-v','--junitxml={}'.format(report_path),test_case])
    else:
        print("暂不支持此报告类型:{}".format(config['REPORT_TYPE']))

    ## 邮件发送
    if config['SEND_EMAIL'] == 'YES':
        email = HandleEmail()
        text = "本邮件由系统自动发出，无需回复：\n各位同事，大家好，以下附件为本次测试报告！"
        email.send_public_email(text=text,filetype=config['REPORT_TYPE'])
        print("邮件发送成功:{}".format(config['REPORT_TYPE']))



if __name__ == '__main__':
    run_main()