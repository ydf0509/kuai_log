

import time

# print(time.gmtime())

from kuai_log._datetime import datetime,aware_now

# datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

for i in range(1000000):
    if i %1000 == 0:
        print(aware_now())