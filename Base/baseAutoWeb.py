from Base.baseData import DataElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from Base.baseLogger import BaseLogger

logger = BaseLogger('baseAutoWeb.py').get_logger()

class BaseAutoWeb(DataElement):
    """
    封装WEB自动化基础类和方法
    """

    def __init__(self,yaml_name):
        super().__init__(yaml_name)
        self.driver = self.gm.get_var('driver')
        self.t = 0.5
        self.timeout = 10

    def get_loactor_data(self,locator,change_data=None):
        """
        获取元素定位方式
        :param locator: 元素定位方式
        :return: 元素定位方式
        """
        res = self.get_element_data(change_data)
        items = locator.split('/')
        locator_date = res[items[0]][items[1]]
        return locator_date

    def find_element(self,locator,change_data=None):
        """
        元素定位方法，返回元素对象
        :param locator:
        :param change_data:
        :return:
        """
        try:
            locator = self.get_loactor_data(locator, change_data)
            if not isinstance(locator, tuple):
                logger.error('locator参数类型错误，必须列表或者元组类型:loc = ["id","value1"]')
            ele = WebDriverWait(self.driver, self.timeout, self.t).until(EC.presence_of_element_located(locator))
            logger.info("已定位元素信息：定位方式->%s,value值->%s" % (locator[0], locator[1]))
            return ele
        except Exception as e:
            logger.error("元素%s未找到" % str(locator))
            raise e
    
    def find_elements(self,locator,change_data=None):
        """
        元素定位方法，返回元素对象
        :param locator:
        :param change_data:
        :return:
        """
        try:
            locator = self.get_loactor_data(locator, change_data)
            if not isinstance(locator, tuple):
                logger.error('locator 参数类型错误，必须列表或者元组类型:loc = ["id","value1"]')
            ele = WebDriverWait(self.driver, self.timeout, self.t).until(EC.presence_of_all_elements_located(locator))
            logger.info("已定位元素信息：定位方式->%s,value 值->%s" % (locator[0], locator[1]))
            return ele
        except Exception as e:
            logger.error("元素%s未找到" % str(locator))
            raise e

    def get_url(self,url):
        """
        获取当前页面的url
        :return:
        """
        self.driver.get(url)
        self.driver.maximize_window()
        logger.info("已打开%s" % url)

    def click(self,locator,change_data=None):
        """
        元素点击方法
        :param locator:
        :param change_data:
        :return:
        """
        try:
            ele = self.find_element(locator, change_data)
            # 先获取文本，避免点击后页面刷新导致元素失效
            ele_text = ele.text
            ele.click()
            logger.info("已点击元素：%s" % ele_text)
        except Exception as e:
            logger.error("元素%s未找到" % str(locator))
            raise e

    def clear(self,locator,change_data=None):
        """
        元素清空方法
        :param locator:
        :param change_data:
        :return:
        """
        try:
            ele = self.find_element(locator, change_data)
            ele.clear()
            logger.info("已清空元素：%s" % ele.text)
        except Exception as e:
            logger.error("元素%s未找到" % str(locator))

    def send_keys(self,locator,text,change_data=None):
        """
        元素输入方法
        :param locator:
        :param text:
        :param change_data:
        :return:
        """
        try:
            ele = self.find_element(locator, change_data)
            ele.send_keys(text)
            logger.info("已输入元素：%s" % text)
        except Exception as e:
            logger.error("元素%s未找到" % locator)

    def get_title(self):
        """
        获取当前页面的title
        :return:
        """
        try:
            title = self.driver.title
            logger.info("已获取当前页面title：%s" % title)
            return title
        except Exception as e:
            logger.error("获取title失败")
            raise ''

    def get_text(self,locator,change_data=None):
        """
        获取元素文本值
        :param locator:
        :param change_data:
        :return:
        """
        try:
            content = self.find_element(locator, change_data)
            text = content.text
            logger.info("已获取元素文本：%s" % text)
            return text
        except Exception as e:
            logger.error("元素%s未找到" % str(locator))
            raise ''

    def get_attribute(self,locator,attribute,change_data=None):
        """
        获取元素属性值
        :param locator:
        :param attribute:
        :param change_data:
        :return:
        """
        try:
            ele = self.find_element(locator, change_data)
            attribute_value = ele.get_attribute(attribute)
            logger.info("已获取元素属性值：%s" % attribute_value)
            return attribute_value
        except Exception as e:
            logger.error("元素%s未找到" % str(locator))
            raise ''

    def is_selected(self,locator,change_data=None):
        """
        判断元素是否被选中
        :param locator:
        :param change_data:
        :return:
        """
        try:
            ele = self.find_element(locator, change_data)
            selected = ele.is_selected()
            logger.info("已判断元素是否被选中：%s" % selected)
            return selected
        except Exception as e:
            logger.error("元素%s未找到" % str(locator))
            raise ''

    def is_title(self,_title= ''):
        """
        判断当前页面的title是否为指定title
        :param title:
        :return:
        """
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.title_is(_title))
            print(result.get_attribute('innerHTML'))
            logger.info("已判断当前页面title是否为指定title：%s" % result)
            return result
        except Exception as e:
            return  False

    def is_title_contains(self,_title= ''):
        """
        判断当前页面的title是否包含指定title
        :param title:
        :return:
        """
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.title_contains(_title))
            print(result.get_attribute('innerHTML'))
            logger.info("已判断当前页面title是否包含指定title：%s" % result)
            return result
        except Exception as e:
            return  False

    def is_text_in_element(self,locator,_text='',change_data=None):
        """
        判断文本是否符合预期
        :param locator:
        :param text:
        :param change_data:
        :return:
        """
        try:
            locator = self.get_loactor_data(locator, change_data)
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.text_to_be_present_in_element(locator, _text))
            logger.info("已判断文本是否符合预期：%s" % result)
            return result
        except Exception as e:
            return  False

    def is_text_in_element_value(self,locator,_value='',change_data=None):
        """
        判断元素的value是否符合预期
        :param locator:
        :param text:
        :param change_data:
        :return:
        """
        try:
            locator = self.get_loactor_data(locator, change_data)
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.text_to_be_present_in_element_value(locator, _value))
            logger.info("已判断元素的value是否符合预期：%s" % result)
            return result
        except Exception as e:
            return  False

    def is_alert_present(self,timeout=5):
        """
        判断页面是否有alert
        :return:
        """
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.alert_is_present())
            logger.info("已判断页面是否有alert：%s" % result)
            return result
        except Exception as e:
            return  False

    def is_element_clickable(self,locator,change_data=None):
        """
        判断元素是否可点击
        :param locator:
        :param change_data:
        :return:
        """
        try:
            locator = self.get_loactor_data(locator, change_data)
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.element_to_be_clickable(locator))
            logger.info("已判断元素是否可点击：%s" % result)
            return result
        except Exception as e:
            return  False


    def is_element_selected(self,locator,change_data=None):
        """
        判断元素是否被选中
        :param locator:
        :param change_data:
        :return:
        """
        try:
            locator = self.get_loactor_data(locator, change_data)
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.element_located_to_be_selected(locator))
            logger.info("已判断元素是否被选中：%s" % result)
            return result
        except Exception as e:
            return  False

    def is_element_invisible(self,locator,change_data=None):
        """
        判断元素是否可见
        :param locator:
        :param change_data:
        :return:
        """
        try:
            locator = self.get_loactor_data(locator, change_data)
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.invisibility_of_element_located(locator))
            logger.info("已判断元素是否可见：%s" % result)
            return result
        except Exception as e:
            return  False


    def mouse_move_to(self,locator,change_data=None):
        """
        鼠标悬停
        :param locator:
        :param change_data:
        :return:
        """
        try:
            # locator = self.get_loactor_data(locator, change_data)
            ele = self.find_element(locator, change_data)
            ActionChains(self.driver).move_to_element(ele).perform()
            logger.info("已鼠标悬停元素：%s" % locator)
            return ele
        except Exception as e:
            logger.error("元素%s未找到" % str(locator))
            raise ''

    def mouse_drag_to(self,locator,xoffset,yoffset,change_data=None):
        """
        鼠标拖拽
        :param locator:
        :param change_data:
        :return:
        """
        try:
            # locator = self.get_loactor_data(locator, change_data)
            ele = self.find_element(locator, change_data)
            ActionChains(self.driver).drag_and_drop_by_offset(ele,xoffset,yoffset).perform()
            logger.info("已鼠标拖拽元素：%s" % locator)
            return ele
        except Exception as e:
            logger.error("元素%s未找到" % str(locator))
            raise ''

    def js_focus_element(self,locator,change_data=None):
        """
        聚焦元素
        :param locator:
        :param change_data:
        :return:
        """
        try:
            # locator = self.get_loactor_data(locator, change_data)
            target = self.find_element(locator, change_data)
            self.driver.execute_script("arguments[0].scrollIntoView();", target)
            logger.info("已聚焦元素：%s" % locator)
            return target
        except Exception as e:
            logger.error("元素%s未找到" % str(locator))
            raise ''

    def js_scroll_to_end(self,x=0):
        """
        滚动到底部
        :param x:
        :return:
        """
        try:
            js = "window.scrollTo(%s,document.body.scrollHeight)" % x
            self.driver.execute_script(js)
            logger.info("已滚动到底部")
            return True
        except Exception as e:
            logger.error("滚动到底部失败")
            return False

    def js_scroll_to_top(self):
        """
        滚动到顶部
        :return:
        """
        try:
            js = "window.scrollTo(0,0)"
            self.driver.execute_script(js)
            logger.info("已滚动到顶部")
            return True
        except Exception as e:
            logger.error("滚动到顶部失败")
            return False

    def keyboard_sendkeys_to(self,locator,text,change_data=None):
        """
        模拟键盘输入
        :param locator:
        :param text:
        :param change_data:
        :return:
        """
        try:
            # locator = self.get_loactor_data(locator, change_data)
            ele = self.find_element(locator, change_data)
            ActionChains(self.driver).send_keys_to_element(ele,text).perform()
            logger.info("已模拟键盘输入：%s" % text)
            return ele
        except Exception as e:
            logger.error("元素%s未找到" % str(locator))
            raise ''

    def get_alert_text(self):
        """
        获取alert的文本信息
        :return:
        """
        try:
            confirm = self.driver.switch_to.alert
            logger.info("已获取alert文本：%s" % confirm.text)
            return confirm.text
        except Exception as e:
            logger.error("获取alert文本失败")
            return ''

    def alert_accept(self):
        """
        点击alert的OK按钮
        :return:
        """
        try:
            confirm = self.driver.switch_to.alert
            confirm.accept()
            logger.info("已点击alert的OK按钮")
            return True
        except Exception as e:
            logger.error("点击alert的OK按钮失败")
            return False

    def alert_dismiss(self):
        """
        点击alert的取消按钮
        :return:
        """
        try:
            confirm = self.driver.switch_to.alert
            confirm.dismiss()
            logger.info("已点击alert的取消按钮")
            return True
        except Exception as e:
            logger.error("点击alert的取消按钮失败")
            return False

    def allert_input_text(self,text):
        """
        输入alert的文本信息
        :param text:
        :return:
        """
        try:
            input_text = self.driver.switch_to.alert
            input_text.send_keys(text)
            logger.info("已输入alert文本：%s" % text)
            return True
        except Exception as e:
            logger.error("输入alert文本失败")
            return False

    def select_by_index(self,locator,index=0,change_data=None):
        """
        通过索引选择select的选项
        :param locator:
        :param index:
        :param change_data:
        :return:
        """
        try:
            # locator = self.get_loactor_data(locator, change_data)
            ele = self.find_element(locator, change_data)
            Select(ele).select_by_index(index)
            logger.info("已通过索引选择select的选项：%s" % index)
            return ele
        except Exception as e:
            logger.error("通过索引选择select的选项失败")
            raise ''

    def select_by_value(self,locator,value,change_data=None):
        """
        通过value选择select的选项
        :param locator:
        :param value:
        :param change_data:
        :return:
        """
        try:
            # locator = self.get_loactor_data(locator, change_data)
            ele = self.find_element(locator, change_data)
            Select(ele).select_by_value(value)
            logger.info("已通过value选择select的选项：%s" % value)
            return ele
        except Exception as e:
            logger.error("通过value选择select的选项失败")
            raise ''

    def select_by_text(self,locator,text,change_data=None):
        """
        通过text选择select的选项
        :param locator:
        :param text:
        :param change_data:
        :return:
        """
        try:
            # locator = self.get_loactor_data(locator, change_data)
            ele = self.find_element(locator, change_data)
            Select(ele).select_by_visible_text(text)
            logger.info("已通过text选择select的选项：%s" % text)
            return ele
        except Exception as e:
            logger.error("通过text选择select的选项失败")
            raise ''

    def get_select_options(self,locator,change_data=None):
        """
        获取select的所有选项
        :param locator:
        :param change_data:
        :return:
        """
        try:
            # locator = self.get_loactor_data(locator, change_data)
            ele = self.find_element(locator, change_data)
            options = Select(ele).options
            logger.info("已获取select的所有选项")
            return options
        except Exception as e:
            logger.error("获取select的所有选项失败")
            return ''

    def get_select_first_option(self,locator,change_data=None):
        """
        获取select的第一个选项
        :param locator:
        :param change_data:
        :return:
        """
        try:
            # locator = self.get_loactor_data(locator, change_data)
            ele = self.find_element(locator, change_data)
            option = Select(ele).first_selected_option
            logger.info("已获取select的第一个选项")
            return option
        except Exception as e:
            logger.error("获取select的选项失败")
            return ''

    def get_select_selected_options(self,locator,change_data=None):
        """
        获取select的所有已选中的选项
        :param locator:
        :param change_data:
        :return:
        """
        try:
            # locator = self.get_loactor_data(locator, change_data)
            ele = self.find_element(locator, change_data)
            options = Select(ele).all_selected_options
            logger.info("已获取select的所有已选中的选项")
            return options
        except Exception as e:
            logger.error("获取select的所有已选中的选项失败")
            return ''

    def get_select_is_multiple(self,locator,change_data=None):
        """
        获取select的属性multiple
        :param locator:
        :param change_data:
        :return:
        """
        try:
            # locator = self.get_loactor_data(locator, change_data)
            ele = self.find_element(locator, change_data)
            is_multiple = Select(ele).is_multiple
            logger.info("已获取select的属性multiple")
            return is_multiple
        except Exception as e:
            logger.error("获取select的属性multiple失败")
            return ''

    def switch_to_iframe(self,locator,change_data=None):
        """
        切换iframe
        :param locator:
        :param change_data:
        :return:
        """
        try:
            id_index_locator = self.get_loactor_data(locator, change_data)
            if isinstance(id_index_locator, int):
                self.driver.switch_to_iframe(id_index_locator)
            elif isinstance(id_index_locator, str):
                self.driver.switch_to_iframe(id_index_locator)
            elif isinstance(id_index_locator, tuple) or isinstance(id_index_locator, list):
                ele = self.find_element(locator)
                self.driver.switch_to_iframe(ele)
            else:
                self.driver.switch_to_iframe(id_index_locator)
            logger.info("iframe切换为{}".format(id_index_locator))
        except Exception as e:
            logger.error("iframe{}切换异常，{}".format(locator, e))

    def switch_to_iframe_out(self):
        """
        切换iframe到默认层
        :return:
        """
        try:
            self.driver.switch_to_default_content()
            logger.info("iframe已切换到默认页面")
        except Exception as e:
            logger.error("iframe切换到最外层失败{}".format(e))

    def switch_to_up(self):
        """
        切换iframe到上一层
        :return:
        """
        try:
            self.driver.switch_to_default_content()
            logger.info("iframe已切换到上一层")
        except Exception as e:
            logger.error("iframe切换到上一层失败{}".format(e))

    def get_handles(self):
        """
        获取当前所有窗口句柄
        :return:
        """
        try:
            handles = self.driver.window_handles
            logger.info("获取所有的handle: {}".format( handles))
            return handles
        except Exception as e:
            logger.error("获取所有handle失败{}".format(e))

    def switch_to_handle(self,index=-1):
        """
        切换窗口
        :param index: 第几个 -1是最后一个
        :return:
        """
        try:
            handle_list = self.driver.window_handles
            self.driver.switch_to_window(handle_list[index])
            logger.info("已切换到{}窗口".format(handle_list[index]))
        except Exception as e:
            logger.error("切换窗口失败{}".format(e))

    def switch_to_window(self,window_name):
        """
        切换窗口
        :param window_name:
        :return:
        """
        try:
            self.driver.switch_to_window(window_name)
            logger.info("已切换到{}窗口".format(window_name))
        except Exception as e:
            logger.error("切换窗口{}失败{}".format(window_name,e))




if __name__ == '__main__':
    web = BaseAutoWeb('Web元素信息 - 登录')
    res = web.get_loactor_data('login/loginbtn')
    print(res)