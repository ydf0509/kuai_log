
import time

from nb_log import get_logger


logger = get_logger(name='test', log_level_int=10, log_filename='t6abcnb.log', log_path='/pythonlogs'
                    # formatter_template='{file_name} - {function} - {name} - {levelname} - {message}',
                    # formatter_template='{levelname} - {message}'
                    )
t_start = time.time()
for i in range(100000):
    logger.debug(111)
    # logger.info(111)
    # logger.warning(111)
    # logger.error(111)
    # logger.critical(111)

print(time.time() - t_start)