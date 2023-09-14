## 1 kuai_log

安装 pip install kuai_log

kuai_log 是最快的python日志,比loguru和logging快30倍.

kuai_log的控制台日志自动彩色.

kuai_log的文件日志多进程切割安全.

kuai_log的文件日志支持更友好的json文件写入,更适合elk采集.(例如logger.info直接记录一个字典,会自动转换)

### 1.2 为什么用 kuai_log

```
内置的logging功能十分丰富强大扩展性好,但很多人不懂他的丰富功能,所以平时也没用到那些功能. 
例如logging 树形的命名空间name,用户都不知道

用户只是简单的使用,那就可以不需要logging包了
```

## 2 性能比较

在 win11 + r7 4800h上

```
loguru 写入文件和打印控制台,10万次日志耗费48秒

logging 写入文件和打印控制台,10万次日志耗费45秒

nb_log 写入文件和打印控制台,10万次日志耗费7秒

kuai_log 写入文件和打印控制台,10万次日志耗费1.7秒
```

## 3 kuai_log 写入 10万次文件和打印控制台代码:

```python
import logging
import time

from kuai_log import get_logger

logger = get_logger(name='test', level=logging.DEBUG, log_filename='t5.log',
                    log_path='/pythonlogs', is_add_file_handler=True,
                    )

t_start = time.time()
for i in range(10):
    logger.debug(i)
print(time.time() - t_start)
```

### 3.2 kuai_log的日志级别和常用的日志是一样的.debug info warning error critical 

```python
import logging
import time

from kuai_log import get_logger

logger = get_logger(name='test77', level=logging.DEBUG, log_filename='t777.log',
                    log_path='/pythonlogs', is_add_file_handler=True,
                    json_log_path='/python_logs_json', is_add_json_file_handler=True,
                    )

t_start = time.time()
for i in range(1):
    logger.debug(i)
    logger.info(i)
    logger.warning(i)
    logger.error(i)
    logger.critical(i)

print(time.time() - t_start)
```

## 4 kuai_log 用法比logging和loguru简单.

### 4.1 有些人问需要实例化生成logger,没有 from loguru import logger直接用爽?

```
用户是每个name的日志行为是独立的,所以用户在大项目中有很多个日志,不同的表现行为,
例如有的函数里面日志界别高才输出,有的模块需要日志级别低就输出,
例如有的模块的日志需要写入文件,有的模块的日志不需要写入文件,
所以用不同的name来区分日志是最好的
```

### 4.2 用户想偷懒,学习loguru直接导入就使用,想不需要手动实例化生成logger

kuai_log 自带一个已经实例化好的 k_logger 对象,你还嫌麻烦?

```python
from kuai_log import k_logger

k_logger.debug('hello')
```

## 5 kuai_log为什么快?

因为logging日志系统功能非常丰富强大,扩展性好,代码较为复杂,kuai_log没有基于logging包来封装,是完全从0写的,代码简单自然就性能好了.

kuai_log实现的文件日志多进程rotate切割安全,使用了特殊的方式,所以技能保证切割不报错又能保证性能.

nb_log是基于logging封装的,kuai_log是手写的.

## 6 kuai_log 日志截图

[![pPRvwGD.png](https://z1.ax1x.com/2023/09/14/pPRvwGD.png)](https://imgse.com/i/pPRvwGD)