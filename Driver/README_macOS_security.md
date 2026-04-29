# macOS 解决 chromedriver 被拦截的方法

## 问题原因
Apple 的 Gatekeeper 安全机制阻止了未签名的 chromedriver 运行。

## 解决方法（3 选 1）

### 方法 1：使用系统设置（最简单）

1. 打开 **系统偏好设置** → **安全性与隐私**
2. 在 **通用** 标签页底部，会看到 "已阻止使用 'chromedriver'" 的提示
3. 点击 **仍要打开** 按钮
4. 输入你的 Mac 密码确认
5. 完成！现在可以运行 chromedriver 了

### 方法 2：右键打开（推荐）

1. 打开 Finder，找到 chromedriver 文件：
   ```
   /Users/snow/snow-sakura/snow-prject/snow-python/TestFramework_po/Driver/chromedriver
   ```

2. **按住 Control 键**的同时，右键点击 chromedriver 文件

3. 选择 **打开**

4. 在弹出的警告对话框中，点击 **打开** 按钮

5. 完成！以后直接运行就可以了

### 方法 3：使用终端命令（高级）

打开终端（Terminal），执行以下命令：

```bash
# 移除隔离属性
xattr -d com.apple.quarantine /Users/snow/snow-sakura/snow-prject/snow-python/TestFramework_po/Driver/chromedriver

# 添加执行权限
chmod +x /Users/snow/snow-sakura/snow-prject/snow-python/TestFramework_po/Driver/chromedriver
```

## 验证是否成功

在终端执行：
```bash
ls -l /Users/snow/snow-sakura/snow-prject/snow-python/TestFramework_po/Driver/chromedriver
```

应该看到类似这样的输出（有 x 执行权限标志）：
```
-rwxr-xr-x  1 yourname  staff  ...  chromedriver
```

## 运行测试

修复后，运行测试：
```bash
cd /Users/snow/snow-sakura/snow-prject/snow-python
python TestFramework_po/PageObject/p02_web_gjxt/web_login_page.py
```

---

**提示**：如果以上方法都不行，可能需要降低 macOS 的安全级别（不推荐）：
- 重启 Mac，按住 Command + R 进入恢复模式
- 打开终端，输入：`csrutil disable`
- 重启 Mac

但通常不需要这么做，用上面 3 个方法之一就够了！
