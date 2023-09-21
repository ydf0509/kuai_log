

import time

# print(time.gmtime())
from datetime import datetime as dt
from kuai_log._datetime import datetime,aware_now
import pysnooper_click_able
# datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

t1 = time.time()
# @pysnooper_click_able.snoop(depth=10000)
def f():
    for i in range(1000000):
        if i %10000 == 0:
            aware_now()
            # print(aware_now())
            # print(dt.now().strftime('%Y-%m-%dT%H:%M:%S %z'))
            # now = dt.now()
            # year, month, day, hour, minute, second, weekday, yearday, xx = now.timetuple()
            # microsecond = now.microsecond
            # print(year, month, day, hour, minute, second, weekday, yearday,xx,microsecond)


f()

print(time.time() -t1)


time.sleep(100)

