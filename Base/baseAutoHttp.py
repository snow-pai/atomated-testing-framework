import requests
import urllib3
from Base.baseData import DataElement
from Base.baseLogger import BaseLogger
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urljoin
logger = BaseLogger('baseAutoHttp.py').get_logger()

class BaseAutoHttp(DataElement):
    """
    封装接口自动化基础类和方法
    """

    session = requests.session()

    def __init__(self,yaml_name):
        """
        初始化
        """
        super().__init__(yaml_name)
        self.duration = 10

    def request_base(self,apiName,change_data=None,**kwargs):
        """
        封装通用接口请求方法
        :param method: 请求方法
        :param url: 请求地址
        :param kwargs: 请求参数
        :return:
        """
        try:
            logger.info("【{}:{}接口调用开始】".format(self.yaml_name,apiName))
            yaml_data = self.get_element_data(change_data)[apiName]
            # print(yaml_data)
            yaml_data['url'] = urljoin(self.config['TEST_URL'], yaml_data['url'])
            # print(yaml_data['url'])
            logger.info("获取【{}】文件【{}】接口请求参数：{}".format(self.yaml_name,apiName,yaml_data))
            logger.info("接口请求方式：{}".format(yaml_data['method']))
            logger.info("接口请求地址：{}".format(yaml_data['url']))
            if 'data' in yaml_data.keys():
                logger.info("接口的请求体：{}".format(yaml_data['data']))
            elif 'json' in yaml_data.keys():
                logger.info("接口的请求体：{}".format(yaml_data['json']))
            # method=yaml_data['method'],url=yaml_data['url'],headers=yaml_data['headers']
            urllib3.disable_warnings(InsecureRequestWarning)
            res = BaseAutoHttp.session.request(**yaml_data, **kwargs)
            logger.info("接口的响应时间：{}".format(res.elapsed.total_seconds()))
            logger.info("POST-接口的响应状态码：{}".format(res.status_code))
            logger.info("POST-接口的响应体：{}".format(res.text))
            logger.info("【{}:{}接口调用结束】".format(self.yaml_name,apiName))
            return res
        except Exception as e:
            logger.error('接口请求失败：{}'.format(e))


if __name__ == '__main__':
    api = BaseAutoHttp('接口元素信息-登录')
    api.request_base('home_api')