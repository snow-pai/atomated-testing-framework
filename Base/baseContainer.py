## 全局变量管理器

class GlobalVar(object):
    """全局变量管理器"""
    _global_var_dict = {}
    _instance = False

    def set_var(self, name, value):
        """设置变量"""
        self._global_var_dict[name] = value

    def get_var(self, name):
        """获取变量"""
        try:
            return self._global_var_dict.get(name)
        except KeyError as e:
            print("获取变量失败：{}".format(e))

    def __new__(cls, *args, **kwargs):
        #单例，固定写法#
        if cls._instance == False:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

# if __name__ == '__main__':
#     gv = GlobalVar()
#     gv.set_var("name", "小王")
#     print(gv.get_var("name"))
#
# gv1 = GlobalVar()  # 创建记事本 1
# gv2 = GlobalVar()  # 创建记事本 2
# gv3 = GlobalVar()  # 创建记事本 3
#
# # 这是 3 个不同的记事本
# gv1.set_var("名字", "张三")
# print(gv2.get_var("名字"))  # 输出：空！因为 gv2 的本子上没记这个名字
