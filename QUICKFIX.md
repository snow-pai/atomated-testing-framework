# 快速修复指南

本文档提供了代码审查中发现的关键问题的修复方案。

---

## 🚨 P0 - 必须立即修复

### 1. baseAutoClient.py - 缺少 os 模块导入

**文件**: `Base/baseAutoClient.py`

**问题**: 第50行使用 `os.path.join` 但未导入 `os` 模块

**修复**:
```python
# 在文件顶部添加
import os
import time
import pyautogui
import pyperclip
```

---

### 2. baseYaml.py - 语法错误

**文件**: `Base/baseYaml.py` 第51行

**问题**:
```python
if not isinstance(data,list):  # 缺少冒号
```

**修复**:
```python
if not isinstance(data, list):
```

---

### 3. p03_http_gjxt/conftest.py - 多处错误

**文件**: `TestSuits/p03_http_gjxt/conftest.py`

**问题1**: 第1行导入未使用的符号
```python
from symbol import yield_expr  # 删除此行
```

**问题2**: 第33-34行装饰器位置错误
```python
# 错误写法
@pytest.fixture(scope="function")
@pytest.mark.parametrize('case_data',DataDriver().get_case_data('06文件夹新增和删除'))
def folder_add_delete(case_data):

# 正确写法
@pytest.fixture(scope="function")
def folder_add_delete(request):
    case_data = request.getfixturevalue('case_data')

@pytest.fixture(scope="function")
@pytest.mark.parametrize('case_data', DataDriver().get_case_data('06文件夹新增和删除'))
def case_data_fixture(request):
    return request.param
```

**问题3**: 第42行语法错误
```python
# 错误
af.add_folder(case_data['name'], case_data['desc']])

# 正确
af.add_folder(case_data['name'], case_data['desc'])
```

---

## 🟠 P1 - 高优先级

### 4. baseContainer.py - 单例线程安全

**文件**: `Base/baseContainer.py`

**当前代码**:
```python
def __new__(cls, *args, **kwargs):
    if cls._instance == False:
        cls._instance = super().__new__(cls, *args, **kwargs)
    return cls._instance
```

**修复后**:
```python
import threading

class GlobalVar(object):
    """全局变量管理器"""
    _lock = threading.Lock()
    _global_var_dict = {}
    _instance = None

    def set_var(self, name, value):
        """设置变量"""
        self._global_var_dict[name] = value

    def get_var(self, name):
        """获取变量"""
        return self._global_var_dict.get(name)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
```

---

### 5. baseExcel.py - 库不兼容

**文件**: `Base/baseExcel.py`

**问题**: xlrd/xlwt 仅支持 .xls，不支持 .xlsx

**修复** (使用 openpyxl):
```python
from openpyxl import load_workbook, Workbook

class ExcelRead():
    def __init__(self, excel_path, sheet_name='Sheet1'):
        self.workbook = load_workbook(excel_path)
        self.sheet = self.workbook[sheet_name]
        self.rows = self.sheet.max_row
        self.cols = self.sheet.max_column

    def dict_data(self):
        """将 Excel 数据转换为字典列表"""
        if self.rows <= 1:
            print("没有数据")
            return []
        
        result = []
        headers = [cell.value for cell in self.sheet[1]]
        
        for row_idx in range(2, self.rows + 1):
            row_dict = {}
            for col_idx, header in enumerate(headers, start=1):
                row_dict[header] = self.sheet.cell(row=row_idx, column=col_idx).value
            result.append(row_dict)
        
        return result
```

---

### 6. baseExcel.py - get_colinfo bug

**文件**: `Base/baseExcel.py` 第63行

**问题**:
```python
def get_colinfo(self, col):
    clo_data = []
    testdatas = self.dict_data()
    for data in testdatas:
        clo_data.append(data[clo_data])  # 错误！
    return clo_data
```

**修复**:
```python
def get_colinfo(self, col):
    """获取某一列的数据"""
    clo_data = []
    testdatas = self.dict_data()
    header = self.header[col - 1] if col <= len(self.header) else None
    if not header:
        return clo_data
    for data in testdatas:
        clo_data.append(data.get(header))
    return clo_data
```

---

### 7. baseAutoWeb.py - raise 语法错误

**文件**: `Base/baseAutoWeb.py` 多处

**问题**:
```python
except Exception as e:
    logger.error("...")
    raise ''  # 错误：应抛出异常对象
```

**修复** (多处):
```python
except TimeoutException:
    logger.error(f"元素定位超时: {locator}")
    raise TimeoutException(f"元素定位超时: {locator}")
except NoSuchElementException:
    logger.error(f"元素未找到: {locator}")
    raise NoSuchElementException(f"元素未找到: {locator}")
except Exception as e:
    logger.error(f"操作失败: {e}")
    raise
```

---

## 🟡 P2 - 中优先级

### 8. 移除硬编码路径

**文件**: `Base/baseGuiRun.py` 第246行

**问题**:
```python
from TestFramework_po.Base.baseContainer import GlobalVar  # 硬编码
```

**修复**:
```python
import sys
import os

# 在文件开头添加路径处理
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from Base.baseContainer import GlobalVar
```

---

### 9. 移除硬编码下载路径

**文件**: `PageObject/p02_web_gjxt/web_file_page.py` 第150行

**问题**:
```python
download_path = r"/Users/snow/Downloads"  # macOS硬编码路径
```

**修复**:
```python
import platform
import os

def get_download_path():
    """获取系统下载目录"""
    system = platform.system()
    if system == 'Windows':
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    elif system == 'Darwin':  # macOS
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:  # Linux
        return os.path.join(os.path.expanduser('~'), 'Downloads')

download_path = get_download_path()
```

---

### 10. SQL注入修复

**文件**: `PageObject/p02_web_gjxt/web_article_page.py` 多处

**问题**:
```python
db.mysql_db_select("select count(*) from journalarticle where title = '{}'".format(title))
```

**修复** (参数化查询):
```python
# 修改 dbbase.py 添加参数化查询方法
def mysql_db_select_safe(self, sql, params):
    try:
        self.create_connection()
        with self.connetcion.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchall()
        return result
    finally:
        self.connetcion.close()

# 使用
db.mysql_db_select_safe(
    "select count(*) from journalarticle where title = %s",
    (title,)
)
```

---

## 📝 修复清单

| 序号 | 问题 | 优先级 | 状态 |
|------|------|--------|------|
| 1 | baseAutoClient.py 缺少os导入 | P0 | ☐ |
| 2 | baseYaml.py 语法错误 | P0 | ☐ |
| 3 | p03_http_gjxt/conftest.py 错误 | P0 | ☐ |
| 4 | 单例模式线程安全 | P1 | ☐ |
| 5 | Excel库不兼容 | P1 | ☐ |
| 6 | get_colinfo bug | P1 | ☐ |
| 7 | raise 语法错误 | P1 | ☐ |
| 8 | 移除硬编码路径 | P2 | ☐ |
| 9 | 下载路径硬编码 | P2 | ☐ |
| 10 | SQL注入风险 | P2 | ☐ |

---

## ✅ 验证修复

修复完成后，运行以下命令验证：

```bash
# 1. 语法检查
python -m py_compile Base/baseAutoClient.py
python -m py_compile Base/baseYaml.py
python -m py_compile TestSuits/p03_http_gjxt/conftest.py

# 2. 运行测试
python -m pytest TestSuits/ -v

# 3. 代码检查
flake8 Base/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

---

**最后更新**: 2026-04-29
