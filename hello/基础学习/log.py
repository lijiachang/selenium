# coding=utf-8

import logging

logger = logging.getLogger() #生成logging对象
hdlr = logging.FileHandler("sendlo.txt") # 日志名和生成位置
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s") #生成日志内容的格式
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)

logger.debug("this is a debug message!")
logger.error("this is a error message!")
