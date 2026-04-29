import os
import sys
import pytest
import subprocess
from Base.basePath import BasePath as BP
from Base.baseUtils import read_config_ini, file_all_dele
from Base.baseContainer import GlobalVar
from Base.baseSendEmail import HandleEmail
from Base.baseGuiRun import BaseGuiRun

config = read_config_ini(BP.CONFIG_FILE)
gm = GlobalVar()
gm.set_var('CONFIG_INFO', config)


class RunClient(BaseGuiRun):
    """图形化客户端运行入口（继承 BaseGuiRun）"""
    
    def run_with_gui(self, auto_mode=False):
        """图形化选择用例并执行
        
        Args:
            auto_mode: 是否自动模式（True=执行所有用例，False=GUI 选择）
        """
        if auto_mode:
            # 自动模式：先收集用例再执行
            print('\n=== 开始收集测试用例 ===')
            subprocess.run([sys.executable, '-m', 'pytest', '--co', '-q', BP.TEST_SUIT_DIR])
            print(f'用例收集完成，文件路径：{BP.TESTCASES}')
            
            selected_cases = self._get_all_cases_from_yaml()
            if selected_cases:
                print(f'\n自动模式：执行所有 {len(selected_cases)} 个测试用例...')
                self.run_cases(selected_cases)
            else:
                print('\n未找到任何测试用例！')
        else:
            # GUI 模式：显示界面让用户操作
            print('正在启动图形化界面...')
            super().run()  # 调用基类 run 方法显示 GUI
    
    def _get_all_cases_from_yaml(self):
        """从 testcases.yaml 读取所有用例路径"""
        from TestFramework_po.Base.baseYaml import read_yaml
        
        testcases = read_yaml(BP.TESTCASES)
        if not testcases:
            return []
        
        all_cases = []
        for case_key, case_info in testcases.items():
            # case_key 格式：TestSuits/project02_auto_test/test_case01.py::TestCase
            for method_name in case_info.keys():
                if method_name != 'comment':
                    # 构造完整的用例路径（使用绝对路径）
                    full_path = f'{BP.TEST_SUIT_DIR}/{case_key.replace("TestSuits/", "")}::{method_name}'
                    all_cases.append(full_path)
        
        return all_cases
    
    def run_cases(self, selected_cases):
        """执行测试用例（复用 run.py 逻辑）"""
        # 切换到项目根目录，确保 pytest 能找到测试文件
        os.chdir(BP.PROJECT_ROOT)
        print(f'当前工作目录：{os.getcwd()}')
        
        config = gm.get_var('CONFIG_INFO')['项目运行设置']
        
        if config['REPORT_TYPE'] == 'ALLURE':
            pytest.main(['-s', '-v', '--alluredir={}'.format(BP.ALLURE_RESULT_PATH)] + selected_cases)
            os.system('allure generate {} -o {} --clean'.format(BP.ALLURE_RESULT_PATH, BP.ALLURE_REPORT_PATH))
            file_all_dele(BP.ALLURE_RESULT_PATH)
        elif config['REPORT_TYPE'] == 'HTML':
            report_path = os.path.join(BP.HTML_PATH, 'auto_reports.html')
            pytest.main(['-s', '-v', '--html={}'.format(report_path), '--self-contained-html'] + selected_cases)
        elif config['REPORT_TYPE'] == 'XML':
            report_path = os.path.join(BP.XML_PATH, 'auto_reports.xml')
            pytest.main(['-s', '-v', '--junitxml={}'.format(report_path)] + selected_cases)
        else:
            print("暂不支持此报告类型：{}".format(config['REPORT_TYPE']))
        
        # 邮件发送
        if config['SEND_EMAIL'] == 'YES':
            email = HandleEmail()
            text = "本邮件由系统自动发出，无需回复：\n各位同事，大家好，以下附件为本次测试报告！"
            email.send_public_email(text=text, filetype=config['REPORT_TYPE'])
            print("邮件发送成功：{}".format(config['REPORT_TYPE']))
        
        print('\n测试执行完成！')


if __name__ == '__main__':
    client = RunClient()
    # 设置为 True 可自动执行所有用例，无需 GUI 界面
    # 设置为 False 则显示 GUI 界面手动选择用例
    auto_mode = False  # 修改为 True 启用自动模式
    client.run_with_gui(auto_mode=auto_mode)
