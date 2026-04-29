import time
import pyautogui
import pyperclip
from Base.baseData import DataElement
from Base.baseUtils import *
from Base.baseLogger import BaseLogger
from Base.basePath import BasePath as BP

## 实例化日志类对象 用来打印当前py文件的执行日志
logger = BaseLogger('baseAutoClient.py').get_logger()

class BaseGuiAutoClient(DataElement):
    """
    封装客户端自动化测试的常用操作
    """
    def __init__(self):
        """
        初始化
        """
        super().__init__()
        self.duration = float(self.config['客户端自动化配置']['duration'])
        self.interval = float(self.config['客户端自动化配置']['interval'])
        self.minSearchTime = float(self.config['客户端自动化配置']['minSearchTime'])
        self.confidence = float(self.config['客户端自动化配置']['confidence'])
        self.grayscale = bool(self.config['客户端自动化配置']['grayscale'])

    def _is_file_exist(self,ele):
        abs_paths = self.api_path.get(ele)
        print(abs_paths)
        if not abs_paths:
            raise FileNotFoundError('ele:{}不存在，请检查文件名或者配置文件'.format(ele))
        return abs_paths

    def isexist(self,ele,serchTime=None):
        '''检查图片是否出现在屏幕'''
        picPath = self._is_file_exist(ele)
        if not serchTime:
            serchTime = self.minSearchTime
        coprdinates = pyautogui.locateOnScreen(picPath,minSearchTime=serchTime,
                                               confidence=self.confidence,grayscale=self.grayscale)
        if coprdinates:
            logger.debug('查找图片{}存在'.format(ele.split('.')[0]))
            return pyautogui.center(coprdinates)
        else:
            logger.debug('查找图片{}不存在'.format(ele.split('.')[0]))
            return None

    # 屏幕截图
    def screenshot(self,name,type):
        pyautogui.screenshot(os.path.join(BP.SCREENSHOT_PATH,name))
        logger.error('类型:{}，查找图片{}位置，当前屏幕无此内容，已截图'.format(type,name))
        raise pyautogui.ImageNotFoundException

    def click_picture(self,ele,clicks=1,button='left',is_click= True):
        '''点击图片'''
        pos_x_y = self.isexist(ele)
        if not pos_x_y:
            self.screenshot(ele,'click_picture')
        pyautogui.moveTo(*pos_x_y)
        if is_click:
            pyautogui.click(*pos_x_y,clicks=clicks,button=button,duration=self.duration,interval=self.interval)
            time.sleep(self.duration)
        logger.debug('移动到图片{},位置{},点击：{}成功'.format(ele,is_click,pos_x_y))

    # 屏幕图片相对点击
    def rel_click_picture(self,ele,rel_x=0,rel_y=0,clicks=1,button='left',is_click= True):
        # 图片位置点击
        pos_x_y = self.isexist(ele)
        if not pos_x_y:
            self.screenshot(ele,'rel_click_picture')
        pyautogui.moveTo(*pos_x_y,duration=self.duration)
        pyautogui.moveRel(rel_x,rel_y,duration=self.duration)
        if is_click:
            pyautogui.click(clicks=clicks,button=button,duration=self.duration,interval=self.interval)
            time.sleep(self.duration)
        logger.debug('查找图片{},位置 {},偏移{},点击：{}成功'.format(ele,pos_x_y,(rel_x,rel_y),is_click))

    # 鼠标的绝对位置点击
    def abs_click(self,abs_x=None,abs_y=None,clicks=1,button='left'):
        # 鼠标的绝对位置点击
        pyautogui.click(abs_x,abs_y,clicks=clicks,button=button,duration=self.duration,interval=self.interval)
        logger.debug('鼠标在坐标{},{} 点击{}键{}次'.format(abs_x,abs_y,button,clicks))

    # 鼠标的相对位置点击
    def rel_click(self,rel_x=0,rel_y=0,clicks=1,button='left'):
        # 鼠标的相对位置点击
        pyautogui.moveRel(rel_x,rel_y)
        pyautogui.click(clicks=clicks,button=button,duration=self.duration,interval=self.interval)
        logger.debug('鼠标在坐标{},{} 点击{}键{}次'.format(rel_x,rel_y,button,clicks))

    def moveTo(self,pos_x,pos_y,rel= False):
        '''移动鼠标到指定位置'''
        if rel:
            pyautogui.moveRel(pos_x,pos_y,duration=self.duration)
            logger.debug('鼠标偏移{},{}'.format(pos_x,pos_y))
        else:
            pyautogui.moveTo(pos_x,pos_y,duration=self.duration)
            logger.debug('鼠标移动到{},{}'.format(pos_x,pos_y))

    def dragTo(self,pos_x,pos_y,button='left',rel= False):
        '''拖拽鼠标到指定位置'''
        if rel:
            pyautogui.dragRel(pos_x,pos_y,button=button,duration=self.duration)
            logger.debug('鼠标相对拖拽{},{}'.format(pos_x,pos_y))
        else:
            pyautogui.dragTo(pos_x,pos_y,button=button,duration=self.duration)
            logger.debug('鼠标拖拽到{},{}'.format(pos_x,pos_y))

    def scroll(self,amount_to_scroll,moveToX=None,moveToY=None,direction='up'):
        '''鼠标滚轮滚动'''
        pyautogui.scroll(clicks=amount_to_scroll,x=moveToX,y=moveToY)
        logger.debug('鼠标在{}位置滚动{}值'.format(moveToX,moveToY),amount_to_scroll)


    def type(self,*args):
        '''键盘输入长文本'''
        pyautogui.write(*args,interval=self.interval)
        logger.debug('输入文本{}'.format(*args))

    def input_string(self,text,clear=False):
        # 输入字符串-中文
        pyperclip.copy(text)
        if not clear:
            pyautogui.hotkey('ctrl', 'v')

    def press(self,key):
        '''键盘单个按键操作'''
        pyautogui.press(key)
        logger.debug('按下按键{}'.format(key))

    def hotkey(self,*keys):
        '''键盘组合按键操作'''
        pyautogui.hotkey(*keys)
        logger.debug('按下组合按键{}'.format(*keys))

if __name__ == '__main__':
    gui = BaseGuiAutoClient()
    time.sleep(5)
    gui.type('hello world')