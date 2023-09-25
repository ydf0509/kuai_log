


import logging
import time

from kuai_log import get_logger

logger = get_logger(name='test_example', level=logging.DEBUG, log_filename='kuailog_ex.log',
                    log_path='/pythonlogs', is_add_file_handler=True,
                    json_log_path='/pythonlogs_json', is_add_json_file_handler=True,
                    )

t_start = time.time()
for i in range(1):
    logger.debug(i)
    logger.info(i)
    logger.warning(i)
    logger.error(i)
    logger.critical(i)

print(time.time() - t_start)

time.sleep(10000)
