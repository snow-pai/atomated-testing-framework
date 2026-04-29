import logging
import time
import os
from Base.basePath import BasePath as BP
from Base.baseUtils import read_config_ini

config = read_config_ini(BP.CONFIG_FILE)['日志打印配置']
rq = 'log_' + time.strftime('%Y-%m-%d', time.localtime()) + '.log'

class BaseLogger(object):

    def __init__(self,name):
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(config['level'])
        self.streamHandler = logging.StreamHandler()
        
        # 确保日志目录存在
        Log = BP.LOG_PATH
        if not os.path.exists(Log):
            os.makedirs(Log)
        
        self.fileHandler = logging.FileHandler(os.path.join(BP.LOG_PATH,rq),'a',encoding='utf-8')
        self.formatter = logging.Formatter(config['format'])
        self.streamHandler.setFormatter(self.formatter)
        self.fileHandler.setFormatter(self.formatter)
        self.streamHandler.setLevel(config['stream_handler_level'])
        self.fileHandler.setLevel(config['file_handler_level'])
        self.logger.addHandler(self.streamHandler)
        self.logger.addHandler(self.fileHandler)


    def get_logger(self):
        return self.logger

if __name__ == '__main__':
    logger = BaseLogger('baseLogger.py').get_logger()
    # print(logger)
    # print(config['level'])
    # print(os.path.join(BP.LOG_PATH,rq))
    # print(config['format'])

    logger.info('info')