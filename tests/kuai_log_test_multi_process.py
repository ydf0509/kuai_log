import time

from kuai_log import get_logger
from multiprocessing import Process

logger1 = get_logger('f1',log_filename='f1c.log',log_path='/pythonlogs',is_add_file_handler=True)
logger2 = get_logger('f2',log_filename='f2c.log',log_path='/pythonlogs',is_add_file_handler=True)


def fun():
    for i in range(10000):
        logger1.warning(f'hi {i}')
        logger2.debug(f'hello {i}')


if __name__ == '__main__':
    Process(target=fun).start()
    Process(target=fun).start()

    time.sleep(10000)