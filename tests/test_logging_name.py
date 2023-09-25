import logging
import time

from kuai_log import get_logger



l1 = logging.getLogger('l1.c')
import tornado
import fastapi
print(logging.getLogger('l1') is l1)
l1.info('xixi1')


logger = get_logger('l1')

# l1._log = logger.log

print(l1._log)

l1.info('xixi2')



# class InterceptHandler(logging.Handler):
#     def emit(self, record: logging.LogRecord) -> None:
#         print(record)
#         print(record.getMessage())
#         logger.log(record.levelno,record.getMessage(),record.args,record.exc_info,stack_info=2)
#
# l1.addHandler(InterceptHandler())

# l1._log = logger.log

l1.error('xixi3')

l1.log(10,'logggg')
print('over')
time.sleep(1000000)