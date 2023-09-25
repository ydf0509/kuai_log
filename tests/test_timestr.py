

import time

# print(time.gmtime())

from kuai_log._datetime import datetime,aware_now
import pysnooper_click_able
# datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

@pysnooper_click_able.snoop(depth=10000)
def f():
    for i in range(1):
        # t = time.strftime('%Y-%m-%dT%H:%M:%S%z')
        t = aware_now()
        if i %1000 == 0:
            # print(aware_now())
            print(t)



f()


time.sleep(100)