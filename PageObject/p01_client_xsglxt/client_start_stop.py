from Base.baseGuiRun import TestCaseTreeWidget


class ClientPage(TestCaseTreeWidget):

    def __init__(self, parent=None):
        super(ClientPage, self).__init__(parent)
        self.setWindowTitle('客户端-启动/停止')