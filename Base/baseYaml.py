
import yaml
import os

def read_yaml(yaml_file):
    """读取 YAML 文件内容

    Args:
        yaml_file: YAML 文件名（默认 data.yaml）或完整路径

    Returns:
        解析后的 YAML 内容

    Raises:
        FileNotFoundError: 文件不存在
        yaml.YAMLError: YAML 格式错误
    """
    try:
        # 如果传入的是相对路径，转换为相对于脚本目录的绝对路径
        if not os.path.isabs(yaml_file):
            yaml_dir = os.path.dirname(os.path.abspath(__file__))
            yaml_file = os.path.join(yaml_dir, yaml_file)

        # 检查文件是否存在
        if not os.path.isfile(yaml_file):
            raise FileNotFoundError(f"{yaml_file} 文件不存在")

        # 安全地读取并解析 YAML 文件
        with open(yaml_file, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
            return content if content is not None else {}

    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"YAML 文件解析失败：{yaml_file}, 错误：{e}")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"文件编码错误：{yaml_file}, 错误：{e.reason}")

def write_yaml(yaml_path, data):
    '''yaml 写入封装'''
    # if not os.path.exists(yaml_path):
    #     raise FileNotFoundError("文件路径不存在，请检查文件路径是否正确！{}".format(yaml_path))
    if not isinstance(data, (list, dict)):
        raise TypeError("数据类型错误，请输入列表或字典类型数据：{}".format(data))
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(data=data, stream=f, allow_unicode=True)

def write_group_yaml(yaml_path,data):
    '''yaml写入封装'''
    # if not os.path.exists(yaml_path):
    #     raise FileNotFoundError("文件路径不存在，请检查文件路径是否正确！{}".format(yaml_path))
    if not isinstance(data,list):
        raise TypeError("数据类型错误，请输入列表类型数据：".format(data))
    with open(yaml_path,"w",encoding="utf-8") as f:
        yaml.dump_all(documents=data,stream=f,allow_unicode=True)