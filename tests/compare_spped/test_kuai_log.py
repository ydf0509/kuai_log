import logging
import time

from kuai_log import get_logger

logger = get_logger(name='test', level=logging.DEBUG, log_filename='t5.log',
                    log_path='/pythonlogs', is_add_file_handler=True,
                    # formatter_template='{file_name} - {function} - {name} - {levelname} - {message}',
                    # formatter_template='{levelname} - {message}'
                    )

t_start = time.time()
for i in range(100000):
    logger.debug(i)
    # logger.debug({'b':i},extra={'aaa':i*2})
print(time.time() - t_start)
