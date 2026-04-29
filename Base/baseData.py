import os
from site import abs_paths
from string import Template
import yaml
from Base.baseContainer import GlobalVar
from Base.baseExcel import ExcelRead
from Base.baseLogger import BaseLogger
from Base.basePath import BasePath as BP
from Base.baseUtils import read_config_ini
from Base.baseYaml import read_yaml

logger = BaseLogger('baseData.py').get_logger()


def init_file_path(pic_path):
    '''遍历文件夹下所有 yaml 文件路径
    
    参数:
        pic_path (str): YAML 文件所在的根目录路径
    
    返回:
        dict: 文件名（不含扩展名）到完整文件路径的映射字典
        
    说明:
        递归遍历指定目录下的所有子目录和文件，将 YAML 文件的路径信息
        以文件名为 key 存储到字典中，用于后续的文件查找和访问
    '''
    path = {}
    path_lists = [path_list for path_list in os.walk(pic_path)]
    print(path_lists)
    for path_tuple in path_lists:
        for file_path in path_tuple:
            if isinstance(file_path, str):
                value = file_path
            elif isinstance(file_path, list):
                for file_name in file_path:
                    path[file_name.split('.')[0]] = os.path.join(value,file_name)

    return path

def init_file_exist(file_path, yaml_name):
    '''判断文件是否存在
    
    参数:
        file_path (dict): 文件名到完整路径的映射字典
        yaml_name (str): 要检查的 YAML 文件名（不含扩展名）
    
    返回:
        str: YAML 文件的绝对路径
        
    异常:
        FileNotFoundError: 当指定的 YAML 文件不存在时抛出此异常
        
    说明:
        从文件路径字典中查找指定的 YAML 文件，如果不存在则记录错误日志
        并抛出文件未找到异常，确保后续操作能访问到有效的文件路径
    '''
    abs_path = file_path.get(yaml_name)
    if not abs_path:
        raise FileNotFoundError('el:{}不存在检查文件名或检查配置文件TEST_PROJECT!'.format(yaml_name))
    return abs_path

class DataElement():
    '''逻辑层数据读取类
    
    用于管理和读取测试框架中的元素数据，支持 YAML 格式的数据文件读取，
    并提供模板变量替换功能，实现动态数据的注入和更新
    
    属性:
        gm: 全局变量管理器实例
        yaml_name (str): YAML 文件名称
        config (dict): 项目配置文件内容
        config (dict): 项目运行配置信息
        api_path (dict): API 元素文件路径映射
        abs_path (str): 当前 YAML 文件的绝对路径（非客户端模式）
    '''
    def __init__(self,yaml_name=None):
        '''初始化 DataElement 实例
        
        参数:
            yaml_name (str, optional): YAML 文件名称，默认为 None
            
        说明:
            初始化全局变量、配置文件，并根据运行配置自动类型
            决定是否加载具体的 YAML 文件路径
        '''
        self.gm = GlobalVar()
        self.yaml_name = yaml_name
        self.config = read_config_ini(BP.CONFIG_FILE)
        self.config = self.config['项目运行设置']
        self.api_path = init_file_path(os.path.join(BP.DATA_ELEMENT_PATH, self.config['TEST_PROJECT_NAME']))
        if not self.config["AUTO_TYPE"] == 'CLIENT':
            self.abs_path = init_file_exist(self.api_path, self.yaml_name)


    def get_element_data(self, change_data=None):
        """获取元素数据
        
        参数:
            change_data (dict, optional): 需要替换的模板变量字典，键为变量名，值为替换值

        返回:
            dict: 解析后的 YAML 文件内容
            
        说明:
            当提供 change_data 时，使用 Template 模板引擎替换 YAML 文件中的变量占位符，
            实现动态数据注入；否则直接读取 YAML 文件内容。支持测试数据的参数化和复用
        """
        if change_data:
            with open(self.abs_path, 'r', encoding='utf-8') as f:
                cfg = f.read()
                content = Template(cfg).safe_substitute(**change_data)
                return yaml.load(content,Loader=yaml.FullLoader)
        else:
            result = read_yaml(self.abs_path)
            # 添加类型检查
            if not isinstance(result, dict):
                logger.error(f"YAML 文件解析结果不是字典类型：{type(result)}")
                logger.error(f"文件路径：{self.abs_path}")
                raise TypeError(f"{self.yaml_name} 解析失败，必须是字典格式")
            return result

class DataDriver():
    '''数据驱动类

    用于实现测试数据的驱动功能，支持从 YAML 文件中读取数据并根据测试需求进行参数化处理
    '''
    def __init__(self):
        '''初始化 DataDriver 实例

        说明:
            初始化全局变量管理器实例，为后续的数据驱动操作做好准备
        '''
        self.gm = GlobalVar()
        self.config = read_config_ini(BP.CONFIG_FILE)
        self.config = self.config['项目运行设置']

    def get_case_data(self, yaml_name):
        """获取用例数据

        参数:
            yaml_name (str): YAML 文件名称

        返回:
            dict: 解析后的 YAML 文件内容

        说明:
            根据 YAML 文件名称从项目配置文件中获取对应的测试数据路径，
            并调用 DataElement 类的 get_element_data 方法获取数据。
            支持测试数据的参数化和复用
        """
        data_type = self.config['DATA_DRIVER_TYPE']
        abs_path = init_file_path(os.path.join(BP.DATA_DRIVER_PATH, data_type,self.config['TEST_PROJECT_NAME']))
        data_path = init_file_exist(abs_path, yaml_name)
        if data_type == 'YamlDriver':
            return read_yaml(data_path)
        elif data_type == 'ExcelDriver':
            return ExcelRead(data_path).dict_data()

if __name__ == '__main__':
    # path = r"D:\sakura-project\snow-prject\snow-python\TestFramework_po\Data\DataElement\project01_auto_test"
    # res = init_file_path(path)
    # print(res)
    data = DataElement('01登录页面元素信息')
    change_data = {
        'username':'用户',
        'password':'密码'
    }
    res = data.get_element_data(change_data)
    print(res)