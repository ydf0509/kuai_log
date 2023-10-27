


import requests
from kuai_log import get_logger
import logging

get_logger('urllib3.connectionpool')
import nb_log
# logger = logging.getLogger(None)
# logger.setLevel(10)

# nb_log.get_logger(None)
requests.get('https://www.baidu.com')