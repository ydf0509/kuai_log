

import time
import logging


import logging
from logging import handlers

logger_raw = logging.getLogger("test_logging")
logger_raw.setLevel(logging.DEBUG)

logger_raw.warning('日志太简单太丑了，并且没记录到文件')

# 添加控制台日志
handler_console = logging.StreamHandler()
formatter1 = logging.Formatter('%(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s',"%Y-%m-%d %H:%M:%S")
handler_console.setFormatter(formatter1)
logger_raw.addHandler(handler_console)

# 添加文件日志handler
handler_file = logging.handlers.RotatingFileHandler('test_logging.log',mode='a')
formatter2 = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S")
handler_file.setFormatter(formatter2)
logger_raw.addHandler(handler_file)


t_start = time.time()
for i in range(100000):
    logger_raw.error("日志现在格式变好了，并且记录到文件了")
    # logger.info(111)
    # logger.warning(111)
    # logger.error(111)
    # logger.critical(111)

print(time.time() - t_start)