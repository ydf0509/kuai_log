
import time
import loguru
from loguru import logger  # type: loguru._logger.Logger

print(type(logger))
logger.add('/pythonlogs/logurutest_{time}.log',rotation="00:00")


t_start = time.time()
for i in range(100000):
    logger.debug(i)


print(time.time() - t_start)