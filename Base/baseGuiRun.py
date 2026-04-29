import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from Base.basePath import BasePath as BP
from Base.baseYaml import read_yaml

class TestCaseTreeWidget(QWidget):
    """测试用例树形展示组件"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_test_cases()
    
    def init_ui(self):
        """初始化 UI 界面"""
        self.setWindowTitle('自动化测试管理平台')
        self.setGeometry(100, 100, 1000, 800)
        
        # 创建主布局
        layout = QVBoxLayout()
        
        # 创建顶部按钮区域
        top_layout = QHBoxLayout()
        
        # 收集用例按钮
        self.collect_btn = QPushButton('📋 收集用例')
        self.collect_btn.setMinimumWidth(120)
        self.collect_btn.setMinimumHeight(30)
        self.collect_btn.clicked.connect(self.collect_test_cases)
        
        # 运行测试按钮
        self.run_btn = QPushButton('▶️ 运行测试')
        self.run_btn.setMinimumWidth(120)
        self.run_btn.setMinimumHeight(30)
        self.run_btn.clicked.connect(self.run_selected)
        self.run_btn.setEnabled(False)  # 初始禁用，收集用例后启用
        
        # 全选按钮
        self.select_all_btn = QPushButton('✓ 全选')
        self.select_all_btn.setMinimumWidth(100)
        self.select_all_btn.setMinimumHeight(30)
        self.select_all_btn.clicked.connect(self.select_all)
        
        # 取消全选按钮
        self.deselect_all_btn = QPushButton('✗ 取消全选')
        self.deselect_all_btn.setMinimumWidth(100)
        self.deselect_all_btn.setMinimumHeight(30)
        self.deselect_all_btn.clicked.connect(self.deselect_all)
        
        top_layout.addWidget(self.collect_btn)
        top_layout.addWidget(self.run_btn)
        top_layout.addWidget(self.select_all_btn)
        top_layout.addWidget(self.deselect_all_btn)
        top_layout.addStretch()
        
        # 创建树形组件
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(['用例名称', '用例描述'])
        
        # 两列均分
        header = self.tree.header()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        
        # 启用滚动条
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tree.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 创建结果显示区域
        result_group = QGroupBox('测试执行结果')
        result_layout = QVBoxLayout()
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMaximumHeight(200)
        
        # 添加状态标签
        self.status_label = QLabel('就绪')
        self.status_label.setStyleSheet('color: gray; padding: 5px;')
        
        result_layout.addWidget(self.result_text)
        result_layout.addWidget(self.status_label)
        result_group.setLayout(result_layout)
        
        # 添加到主布局
        layout.addLayout(top_layout)
        layout.addWidget(self.tree)
        layout.addWidget(result_group)
        
        self.setLayout(layout)
    
    def load_test_cases(self):
        """加载测试用例到树形组件"""
        self.tree.clear()
        
        # 读取测试用例文件
        testcases_path = BP.TESTCASES
        print(f'\n[GUI 调试] 检查文件：{testcases_path}')
        print(f'[GUI 调试] 文件存在：{os.path.exists(testcases_path)}')
        
        if not os.path.exists(testcases_path):
            QMessageBox.warning(self, '警告', '未找到测试用例文件！')
            return
        
        testcases = read_yaml(testcases_path)
        print(f'[GUI 调试] 读取到的用例：{testcases}')
        
        if not testcases:
            QMessageBox.warning(self, '警告', '用例文件为空！')
            return
        
        # 遍历测试目录
        test_suit_dir = BP.TEST_SUIT_DIR
        print(f'[GUI 调试] 测试目录：{test_suit_dir}')
        
        for root, dirs, files in os.walk(test_suit_dir):
            # 跳过__pycache__目录
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, test_suit_dir)
                    # 统一路径分隔符，并添加 TestSuits 前缀
                    rel_path = 'TestSuits/' + rel_path.replace('\\', '/')
                    
                    print(f'\n[GUI 调试] 处理文件：{rel_path}')
                    
                    # 创建根节点（文件）
                    file_item = QTreeWidgetItem(self.tree)
                    file_item.setText(0, rel_path)
                    file_item.setIcon(0, self.style().standardIcon(QStyle.SP_FileIcon))
                    
                    # 读取用例信息
                    if testcases:
                        for case_key, case_info in testcases.items():
                            # case_key 格式：TestSuits/project02_auto_test/test_case01.py::TestCase
                            case_file_path = case_key.split('::')[0]
                            # 统一路径分隔符进行比较
                            case_file_path = case_file_path.replace('\\', '/')
                            rel_path_normalized = rel_path.replace('\\', '/')
                            
                            print(f'[GUI 调试] 比较路径：{rel_path_normalized} == {case_file_path}')
                            
                            if rel_path_normalized == case_file_path:
                                # 类节点
                                class_parts = case_key.split('::')
                                class_name = class_parts[1] if len(class_parts) > 1 else 'TestCase'
                                class_item = QTreeWidgetItem(file_item)
                                class_item.setText(0, class_name)
                                class_item.setIcon(0, self.style().standardIcon(QStyle.SP_DirClosedIcon))
                                
                                # 用例方法节点
                                for method_name, method_doc in case_info.items():
                                    if method_name not in ['comment']:
                                        method_item = QTreeWidgetItem(class_item)
                                        # 第一列：用例名称（函数名）
                                        method_item.setText(0, method_name)
                                        # 第二列：用例函数描述（docstring）
                                        if method_doc:
                                            method_item.setText(1, method_doc)
                                        else:
                                            method_item.setText(1, f'def {method_name}()')
                                        
                                        # 设置复选框
                                        method_item.setCheckState(0, Qt.Unchecked)
                                        # 存储完整的文件路径（包含类名）
                                        method_item.setData(0, Qt.UserRole, file_path)
                                        method_item.setData(1, Qt.UserRole, class_name)  # 存储类名
                                        method_item.setData(2, Qt.UserRole, method_name)  # 存储方法名
                                        print(f'[GUI 调试] 添加用例方法：{method_name}, 类名：{class_name}')
                
                # 展开所有节点
                self.tree.expandAll()
        
        print(f'[GUI 调试] 加载完成，顶级节点数：{self.tree.topLevelItemCount()}')
    
    def collect_test_cases(self):
        """收集测试用例"""
        import subprocess
        print('\n=== 开始收集测试用例 ===')
        subprocess.run([sys.executable, '-m', 'pytest', '--co', '-q', BP.TEST_SUIT_DIR])
        print(f'用例收集完成，文件路径：{BP.TESTCASES}')
        
        # 重新加载用例
        self.load_test_cases()
        
        # 启用运行按钮
        if self.tree.topLevelItemCount() > 0:
            self.run_btn.setEnabled(True)
            self.status_label.setText('✅ 用例收集完成，请勾选用例并点击运行')
        else:
            self.status_label.setText('❌ 未找到测试用例')
    
    def select_all(self):
        """全选所有用例"""
        for i in range(self.tree.topLevelItemCount()):
            file_item = self.tree.topLevelItem(i)
            for j in range(file_item.childCount()):
                class_item = file_item.child(j)
                for k in range(class_item.childCount()):
                    method_item = class_item.child(k)
                    method_item.setCheckState(0, Qt.Checked)
    
    def deselect_all(self):
        """取消全选所有用例"""
        for i in range(self.tree.topLevelItemCount()):
            file_item = self.tree.topLevelItem(i)
            for j in range(file_item.childCount()):
                class_item = file_item.child(j)
                for k in range(class_item.childCount()):
                    method_item = class_item.child(k)
                    method_item.setCheckState(0, Qt.Unchecked)
    
    def run_selected(self):
        """运行选中的测试用例"""
        selected_cases = []
        
        # 遍历所有节点收集选中的用例
        for i in range(self.tree.topLevelItemCount()):
            file_item = self.tree.topLevelItem(i)
            for j in range(file_item.childCount()):
                class_item = file_item.child(j)
                for k in range(class_item.childCount()):
                    method_item = class_item.child(k)
                    if method_item.checkState(0) == Qt.Checked:
                        file_path = method_item.data(0, Qt.UserRole)
                        method_name = method_item.data(1, Qt.UserRole)
                        selected_cases.append(f'{file_path}::{method_name}')
        
        if not selected_cases:
            QMessageBox.information(self, '提示', '请勾选要运行的测试用例！')
            return
        
        # 在结果区域显示开始信息
        self.result_text.clear()
        self.result_text.append(f'\n=== 开始执行 {len(selected_cases)} 个测试用例 ===\n')
        self.status_label.setText('⏳ 正在执行测试...')
        
        # 执行测试
        import os
        import pytest
        from io import StringIO
        from TestFramework_po.Base.baseContainer import GlobalVar
        from TestFramework_po.Base.baseUtils import read_config_ini
        from TestFramework_po.Base.baseSendEmail import HandleEmail
        
        # 切换到项目根目录
        os.chdir(BP.PROJECT_ROOT)
        
        config = read_config_ini(BP.CONFIG_FILE)
        gm = GlobalVar()
        gm.set_var('CONFIG_INFO', config)
        config = config['项目运行设置']
        
        # 构造 pytest 参数
        report_path = os.path.join(BP.HTML_PATH, 'auto_reports.html')
        pytest_args = ['-s', '-v', f'--html={report_path}', '--self-contained-html'] + selected_cases
        
        # 捕获输出
        output = StringIO()
        
        class Plugin:
            def pytest_runtest_logreport(self, report):
                if report.when == 'call':
                    status = '✅ PASSED' if report.passed else '❌ FAILED'
                    output.write(f'{report.nodeid}: {status}\n')
                    self.result_text.append(f'{report.nodeid}: {status}')
                    self.result_text.repaint()
        
        plugin = Plugin()
        plugin.result_text = self.result_text
        
        # 执行测试
        exit_code = pytest.main(pytest_args, plugins=[plugin])
        
        # 显示结果
        self.result_text.append(f'\n=== 测试执行完成 ===')
        self.result_text.append(f'报告已生成：{report_path}')
        
        # 发送邮件
        if config.get('SEND_EMAIL', 'NO').upper() == 'YES':
            self.result_text.append('\n正在发送邮件...')
            try:
                email = HandleEmail()
                text = "本邮件由系统自动发出，无需回复：\n各位同事，大家好，以下附件为本次测试报告！"
                email.send_public_email(text=text, filetype='HTML')
                self.result_text.append('✅ 邮件发送成功！')
                self.status_label.setText('✅ 测试完成，邮件已发送')
            except Exception as e:
                self.result_text.append(f'❌ 邮件发送失败：{str(e)}')
                self.status_label.setText('❌ 邮件发送失败')
        else:
            self.status_label.setText('✅ 测试完成')
    



class BaseGuiRun:
    """GUI 运行基础类"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = TestCaseTreeWidget()
    
    def run(self):
        """运行 GUI 应用"""
        self.window.show()
        # 不再调用 sys.exit，让程序继续运行
        self.app.exec_()
    
    def get_selected_cases(self):
        """获取选中的用例"""
        return self.window.selected_cases if hasattr(self.window, 'selected_cases') else []


if __name__ == '__main__':
    # 运行 GUI
    gui = BaseGuiRun()
    gui.run()
