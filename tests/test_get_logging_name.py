import flask
import logging
import requests
# 获取所有的日志记录器名称
logger_names = logging.Logger.manager.loggerDict.keys()

# 打印日志记录器名称
for name in logger_names:
    print(name)