import xlrd
import xlwt


class ExcelRead():

    def __init__(self,excel_path,sheet_name='Sheet1'):
        self.data = xlrd.open_workbook(excel_path)
        self.sheet = self.data.sheet_by_name(sheet_name)

        ## 获取表头  即获取第一行的key值
        self.header = self.sheet.row_values(0)
        ## 获取所有行数和列数
        self.rows = self.sheet.nrows
        self.cols = self.sheet.ncols

    def dict_data(self):
        """
        将 Excel 数据转换为字典列表（第一行为表头作为 key）

        :return: 字典列表，每个字典代表一行数据
        """
        if self.rows <= 1:
            print("没有数据")
        else:
            r = []
            j = 1
            for i in range(self.rows - 1):
                s = {}
                values = self.sheet.row_values(j)
                j = j + 1
                for x in range(self.cols):
                    s[self.header[x]] = values[x]
                r.append(s)
            return r

    def get_rowinfo(self, row):
        """
        获取 Excel 指定行的数据（字典格式）

        :param row: 行号（从 1 开始计数，第 1 行为表头）
        :return: 指定行的数据字典
        """
        if row <= 1:
            print("没有数据")
        else:
            # 获取所有行的字典数据
            testdatas = self.dict_data()
            # 提取指定行的数据（列表索引从 0 开始，需要减 2）
            rowdata = testdatas[row-2]
        return rowdata

    def get_colinfo(self, col):
        """
        获取 Excel 某一列的数据（列表格式）

        :param col: 列号（从 1 开始计数）
        :return: 某一列的数据列表
        """
        clo_data = []
        testdatas = self.dict_data()
        for data in testdatas:
            clo_data.append(data[clo_data])
        return clo_data

    def get_cellinfo(self, row, col):
        """
        获取 Excel 单元格的数据

        :param row: 行号（从 1 开始计数，第 1 行为表头）
        :param col: 列号（从 1 开始计数）
        :return: 单元格的数据
        """
        if row <= 1:
            rowdata = None
        else:
            testdatas = self.dict_data()
            rowdata = testdatas[row-2][col]
        return rowdata

class ExcelWrite():
    """
    Excel写入类
    """
    def __init__(self,sheet_name='Sheet1'):
        """
        初始化方法
        :param excel_path: Excel 文件路径
        :param sheet_name: 表单名称
        """
        self.workbook = xlwt.Workbook(encoding='utf-8')
        ## 获取工作表中的sheet对象
        self.sheet = self.workbook.add_sheet(sheet_name)

    def set_header(self, list_data):
        """
        设置表头
        :param header: 表头列表
        """
        if not isinstance(list_data, list):
            raise Exception("表头数据必须是列表：{}".format(list_data))
        headers = list(list_data[0].keys())
        nums = len(headers)
        for i in range(nums):
            self.sheet.write(0, i, label=headers[i])

    def write_data(self,list_data,excel_path):
        """
        写入数据
        :param list_data: 数据列表
        """
        if not isinstance(list_data, list):
            raise Exception("数据必须是列表：{}".format(list_data))
        self.set_header(list_data)
        rows_num = len(list_data)
        for i in range(rows_num):
            values_data = list(list_data[i].values())
            cows_num = len(values_data)
            for j in range(cows_num):
                self.sheet.write(i+1, j, values_data[j])
        self.workbook.save(excel_path)

if __name__ == '__main__':
    excel_path = r'D:\sakura-project\snow-prject\snow-python\TestFramework_po\Data\DataDriver\ExcelDriver\project01_auto_test\data.xlsx'
    sheet = 'Sheet1'
    excel = ExcelRead(excel_path, sheet)
    res = excel.dict_data()
    print(res)