# 自动化测试框架

## 📦 安装指南

### 环境要求

- **Python**: >= 3.8
- **操作系统**: Windows / macOS / Linux
- **浏览器**: Chrome / Firefox / Edge（Web自动化需要）
- **数据库**: MySQL / SQLite（数据库测试需要）

### 安装步骤

#### 1. 克隆项目

```bash
git clone <repository_url>
cd atomated-testing-framework
```

#### 2. 创建虚拟环境（推荐）

```bash
# 使用venv
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

#### 3. 安装依赖

```bash
# 最小安装（仅核心功能）
pip install -r requirements-core.txt

# 完整安装（推荐，包含所有功能）
pip install -r requirements.txt

# 开发环境安装
pip install -r requirements-dev.txt
```

#### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并配置：

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 数据库配置
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=test

# 邮件配置
SMTP_HOST=smtp.qq.com
SMTP_PORT=465
SMTP_USER=your_email@qq.com
SMTP_PASSWORD=your授权码

# 测试配置
TEST_ENV=dev
BROWSER=chrome
```

### 5. 配置浏览器驱动

#### 使用 webdriver-manager（推荐）

自动下载，无需手动配置：

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

#### 手动安装

将浏览器驱动放入 `Driver/` 目录：

| 浏览器 | 驱动文件 | 下载地址 |
|--------|----------|----------|
| Chrome | chromedriver.exe / chromedriver | [ChromeDriver](https://chromedriver.chromium.org/downloads) |
| Firefox | geckodriver.exe / geckodriver | [GeckoDriver](https://github.com/mozilla/geckodriver/releases) |
| Edge | msedgedriver.exe / msedriver | [EdgeDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) |

### 6. 验证安装

```bash
# 验证Python环境
python --version

# 验证核心依赖
python -c "import pytest; import selenium; import requests; print('依赖安装成功')"

# 运行示例测试
python -m pytest TestSuits/project02_auto_test/ -v
```

---

## 🚀 快速开始

### 运行Web自动化测试

```bash
# 方式1：命令行运行
python RunMain/run.py

# 方式2：GUI界面运行
python RunMain/runClient.py

# 方式3：直接运行pytest
pytest TestSuits/p02_web_gjxt/ -v --html=Reports/HTML/report.html
```

### 运行HTTP接口测试

```bash
pytest TestSuits/p03_http_gjxt/ -v --html=Reports/HTML/report.html
```

### 运行客户端GUI测试

```bash
pytest TestSuits/p01_client_xsglxt/ -v
```

---

## 📁 项目结构

```
atomated-testing-framework/
├── Base/                    # 核心基础模块
│   ├── baseAutoWeb.py      # Web自动化基类
│   ├── baseAutoHttp.py     # HTTP接口自动化基类
│   ├── baseAutoClient.py   # 客户端GUI自动化基类
│   ├── baseData.py         # 数据驱动类
│   ├── baseLogger.py       # 日志管理
│   └── basePath.py         # 路径配置
├── ExtTools/               # 扩展工具
│   ├── dbbase.py          # 数据库操作
│   └── shellbase.py       # SSH远程操作
├── PageObject/            # 页面对象层
├── TestSuits/             # 测试用例层
├── Config/               # 配置文件
├── Data/                 # 测试数据
│   ├── DataElement/      # 页面元素数据
│   └── DataDriver/       # 测试数据驱动
├── Driver/               # 浏览器驱动
├── Reports/              # 测试报告
├── Log/                  # 日志文件
├── RunMain/              # 运行入口
├── requirements.txt      # 依赖清单
└── conftest.py          # pytest配置
```

---

## ⚙️ 配置说明

### 配置文件位置

`Config/配置文件.ini`

### 配置项说明

```ini
[客户端自动化配置]
duration = 0.2              # 鼠标移动速度
interval = 0.25             # 按键间隔时间
minSearchTime = 5           # 图片搜索最小时间
confidence = 0.97           # 图片识别置信度

[WEB自动化配置]
browser = Chrome            # 浏览器类型

[日志打印配置]
level = INFO               # 日志级别
format = %()s - %()s...    # 日志格式

[邮件发送配置]
host = smtp.qq.com         # SMTP服务器
port = 465                 # 端口
send_email = xxx@qq.com     # 发送方
receive_email = [...]       # 接收方列表

[数据库配置]
host = 127.0.0.1
port = 3306
user = root
password = xxx
database = test

[项目运行设置]
AUTO_TYPE = HTTP            # 自动化类型：HTTP/WEB/CLIENT
REPORT_TYPE = HTML          # 报告类型：HTML/ALLURE/XML
DATA_DRIVER_TYPE = YamlDriver  # 数据驱动：YamlDriver/ExcelDriver
TEST_PROJECT_NAME = p03_http_gjxt  # 项目名称
TEST_URL = https://xxx      # 测试地址
SEND_EMAIL = yes            # 是否发送邮件
```

---

## 🔧 常见问题

### Q1: 导入模块失败

```bash
# 确保在项目根目录运行
cd atomated-testing-framework
pip install -r requirements.txt
```

### Q2: ChromeDriver版本不匹配

```python
# 使用webdriver-manager自动匹配
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

### Q3: 邮件发送失败

1. 检查SMTP配置
2. 确保邮箱已开启SMTP服务
3. 使用授权码而非登录密码

### Q4: 数据库连接失败

1. 检查MySQL服务是否启动
2. 验证用户名密码
3. 确认数据库已创建

---

## 📚 文档

- [代码审查报告](./CODE_REVIEW_REPORT.md) - 详细代码审查结果
- [API文档](./docs/API.md) - 接口文档（待补充）

---

## 📄 许可证

MIT License
