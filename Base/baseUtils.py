from configparser import RawConfigParser
from Base.basePath import BasePath
import os
import zipfile

## 读取配置文件内容
def read_config_ini(configPath):
    '''读取配置文件.ini'''
    config = RawConfigParser()
    config.read(configPath,encoding="utf-8")
    return config

def make_zip(zip_path,pname):
    '''打包zip'''
    zip_file = zipfile.ZipFile(pname,'w', zipfile.ZIP_DEFLATED)
    pre_len = len(os.path.dirname(zip_path))
    for parent, dirnames, filenames in os.walk(zip_path):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zip_file.write(pathfile, arcname)
    zip_file.close()
    return pname

def file_all_dele(path):
    '''删除所有文件'''
    for file_name in os.listdir(path):
        os.unlink(os.path.join(path,file_name))


if __name__ == '__main__':
    print(read_config_ini(os.path.join(BasePath.CONFIG_PATH,"配置文件.ini")))
    print(read_config_ini(os.path.join(BasePath.CONFIG_PATH,"配置文件.ini"))["客户端自动化配置"]["duration"])
