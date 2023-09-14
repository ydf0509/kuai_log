import datetime
import os
import queue
import sys
import threading
import time
import atexit

from kuai_log._datetime import aware_now


class Stream:
    @classmethod
    def stdout(cls, msg):
        print(msg)

    @classmethod
    def print(cls, *args, sep=' ', end='\n', file=None, flush=True, sys_getframe_n=2):
        args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
        msg = sep.join(args) + end
        print(msg)

class BulkStream:
    q = queue.SimpleQueue()
    _lock = threading.Lock()
    _has_start_bulk_stdout = False

    @classmethod
    def _bulk_real_stdout(cls):
        with cls._lock:
            msg_str_all = ''
            while not cls.q.empty():
                msg_str_all += str(cls.q.get()) + '\n'
            if msg_str_all:
                sys.stdout.write(msg_str_all)

    @classmethod
    def stdout(cls, msg):
        with cls._lock:
            cls.q.put(msg)

    @classmethod
    def print(cls, *args, sep=' ', end='\n', file=None, flush=True, sys_getframe_n=2):
        args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
        msg = sep.join(args) + end
        fra = sys._getframe(1)  # noqa
        line = fra.f_lineno
        full_path = fra.f_code.co_filename  # type :str
        # file_name = full_path.split('/')[-1].split('\\')[-1]
        full_path_and_line = f'"{full_path}:{line}"'
        fun = fra.f_code.co_name
        full_msg = f'{aware_now()} - {full_path_and_line} - {fun} - [print] - {msg}'
        color_msg = f'\033[0;34m{full_msg}\033[0m'
        with cls._lock:
            cls.q.put(color_msg)

    @classmethod
    def _when_exit(cls):
        # stdout_raw('结束 stdout_raw')
        return cls._bulk_real_stdout()

    @classmethod
    def start_bulk_stdout(cls):
        def _bulk_stdout():
            while 1:
                cls._bulk_real_stdout()
                time.sleep(0.1)

        if not cls._has_start_bulk_stdout:
            cls._has_start_bulk_write = True
            threading.Thread(target=_bulk_stdout, daemon=True).start()

    @classmethod
    def patch_print(cls):
        """
        Python有几个namespace，分别是

        locals

        globals

        builtin

        其中定义在函数内声明的变量属于locals，而模块内定义的函数属于globals。


        https://codeday.me/bug/20180929/266673.html   python – 为什么__builtins__既是模块又是dict

        :return:
        """
        try:
            __builtins__.print = cls.print
        except AttributeError:
            """
            <class 'AttributeError'>
            'dict' object has no attribute 'print'
            """
            # noinspection PyUnresolvedReferences
            __builtins__['print'] = cls.print
        # traceback.print_exception = print_exception  # file类型为 <_io.StringIO object at 0x00000264F2F065E8> 单独判断，解决了，不要加这个。

OsStream = Stream


if os.name == 'nt':  # windows io性能差
    OsStream = BulkStream
    BulkStream.start_bulk_stdout()
    BulkStream.patch_print()
    atexit.register(BulkStream._when_exit)
