import logging
import time
import logging.handlers

# 初始化设置
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s')
# 创建
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建handler
handler1 = logging.FileHandler("log.log")
handler1.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s|%(name)-12s+ %(levelname)-8s++%(message)s')
handler1.setFormatter(formatter)

handler2 = logging.StreamHandler()
handler2.setLevel(logging.ERROR)

logger.addHandler(handler1)
# logger.addHandler(handler2)

# logger.info('test')