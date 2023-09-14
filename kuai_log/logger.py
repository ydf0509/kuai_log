import json
import typing
import copy
import datetime
# from tzlocal import get_localzone
import os
import socket
import sys
import threading
import traceback
from enum import Enum
import logging

from kuai_log._datetime import aware_now
from kuai_log.stream import OsStream
from kuai_log.rotate_file_writter import OsFileWritter


class FormatterFieldEnum(Enum):
    host = 'host'

    asctime = 'asctime'
    name = 'name'
    levelname = 'levelname'
    message = 'message'

    process = 'process'
    thread = 'thread'

    pathname = 'pathname'
    filename = 'filename'
    lineno = 'lineno'
    funcName = 'funcName'
    # click_line = 'click_line'


logger_name__logger_obj_map = {}  # type: typing.Dict[str,KuaiLogger]


# noinspection PyPep8
class KuaiLogger:
    """
    不要手动调用这个类,使用get_logger函数就行了.
    """

    # 获取当前时区
    # current_timezone = get_localzone().zone
    host = socket.gethostname()

    def __init__(self, name, level=logging.DEBUG,
                 is_add_stream_handler=True, is_add_file_handler=False, is_add_json_file_handler=False,
                 log_path=None, json_log_path=None, log_filename=None,
                 max_bytes=1000 * 1000 * 1000, back_count=10,
                 formatter_template='{asctime} - {host} - "{pathname}:{lineno}" - {funcName} - {name} - {levelname} - {message}', ):

        self.name = name
        self.level = level

        self._is_add_stream_handler = is_add_stream_handler
        self._is_add_file_handler = is_add_file_handler
        self._is_add_json_file_handler = is_add_json_file_handler

        self._log_path = log_path
        self._log_filename = log_filename

        if self._is_add_file_handler:
            self._fw = OsFileWritter(log_filename, log_path, max_bytes=max_bytes, back_count=back_count)
        if self._is_add_json_file_handler:
            self._fw_json = OsFileWritter(log_filename, json_log_path, max_bytes=max_bytes, back_count=back_count)

        self._formatter_template = formatter_template
        self._need_fields = self._parse_need_filed()
        # print(self._need_fields)

    def setLevel(self, level):
        """
        Set the specified level on the underlying logger.
        """
        self.level = level

    def _parse_need_filed(self):
        need_fields = set()
        for field in FormatterFieldEnum:
            if '{' + field.value + '}' in self._formatter_template:
                need_fields.add(field.value)
        return need_fields

    def _build_format_kwargs(self, level, msg, stacklevel):
        format_kwargs = {}
        if FormatterFieldEnum.name.value in self._need_fields:
            format_kwargs[FormatterFieldEnum.name.value] = self.name
        if FormatterFieldEnum.levelname.value in self._need_fields:
            format_kwargs[FormatterFieldEnum.levelname.value] = logging._levelToName[level]  # noqa
        if FormatterFieldEnum.message.value in self._need_fields:
            format_kwargs[FormatterFieldEnum.message.value] = msg

        if (
                FormatterFieldEnum.pathname.value in self._need_fields or
                FormatterFieldEnum.filename.value in self._need_fields or
                FormatterFieldEnum.funcName.value in self._need_fields):
            fra = sys._getframe(stacklevel)  # noqa
            lineno = fra.f_lineno
            pathname = fra.f_code.co_filename  # type :str
            filename = pathname.split('/')[-1].split('\\')[-1]
            # noinspection PyPep8Naming
            funcName = fra.f_code.co_name
            if FormatterFieldEnum.pathname.value in self._need_fields:
                format_kwargs[FormatterFieldEnum.pathname.value] = pathname
            if FormatterFieldEnum.filename.value in self._need_fields:
                format_kwargs[FormatterFieldEnum.filename.value] = filename
            if FormatterFieldEnum.lineno.value in self._need_fields:
                format_kwargs[FormatterFieldEnum.lineno.value] = lineno
            if FormatterFieldEnum.funcName.value in self._need_fields:
                format_kwargs[FormatterFieldEnum.funcName.value] = funcName

        if f'{FormatterFieldEnum.process.value}' in self._need_fields:
            format_kwargs[FormatterFieldEnum.process.value] = os.getgid()
        if f'{FormatterFieldEnum.thread.value}' in self._need_fields:
            format_kwargs[FormatterFieldEnum.thread.value] = threading.get_ident()
        if FormatterFieldEnum.asctime.value in self._need_fields:
            # format_kwargs[FormatterFieldEnum.asctime.value] = datetime.datetime.now().strftime(
            #     f"%Y-%m-%d %H:%M:%S.%f {self.current_timezone}")
            format_kwargs[FormatterFieldEnum.asctime.value] = aware_now()
        if FormatterFieldEnum.host.value in self._need_fields:
            format_kwargs[FormatterFieldEnum.host.value] = self.host
        return format_kwargs

    def _log(self, level, msg, args=None, exc_info=None, extra=None, stack_info=False, stacklevel=3):
        # def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):

        if self.level > level:
            return

        format_kwargs = self._build_format_kwargs(level, msg, stacklevel)
        # print(self._formatter_template)
        # print(format_kwargs)
        format_kwargs_json = {}
        if self._is_add_json_file_handler:
            format_kwargs_json = copy.copy(format_kwargs)
            format_kwargs_json['msg'] = {}
            if isinstance(msg, dict):
                format_kwargs_json['msg'].update(msg)
                format_kwargs_json['message'] = ''
            if extra:
                format_kwargs_json['msg'].update(extra)
            if exc_info:
                format_kwargs_json['msg'].update({'traceback': traceback.format_exc()})
        if extra:
            format_kwargs.update(extra)
        msg_format = self._formatter_template.format(**format_kwargs)
        if exc_info:
            msg_format += f'\n {traceback.format_exc()}'
        msg_color = self._add_color(msg_format, level)
        # print(msg_format)
        # print(msg)
        if self._is_add_stream_handler:
            OsStream.stdout(msg_color)
        if self._is_add_file_handler:
            self._fw.write_2_file(msg_format)
        if self._is_add_json_file_handler:
            self._fw_json.write_2_file(json.dumps(format_kwargs_json, ensure_ascii=False))

    @staticmethod
    def _add_color(complete_msg, record_level):
        if record_level == logging.DEBUG:
            # msg_color = ('\033[0;32m%s\033[0m' % msg)  # 绿色
            # print(msg1)
            msg_color = f'\033[0;32m{complete_msg}\033[0m'  # 绿色
        elif record_level == logging.INFO:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.bule, msg))  # 青蓝色 36    96
            msg_color = f'\033[0;36m{complete_msg}\033[0m'
        elif record_level == logging.WARNING:
            # msg_color = ('\033[%s;%sm%s\033[0m' % (self._display_method, self.yellow, msg))
            msg_color = f'\033[0;33m{complete_msg}\033[0m'
        elif record_level == logging.ERROR:
            # msg_color = ('\033[%s;35m%s\033[0m' % (self._display_method, msg))  # 紫红色
            msg_color = f'\033[0;35m{complete_msg}\033[0m'
        elif record_level == logging.CRITICAL:
            # msg_color = ('\033[%s;31m%s\033[0m' % (self._display_method, msg))  # 血红色
            msg_color = f'\033[0;31m{complete_msg}\033[0m'
        else:
            msg_color = f'{complete_msg}'
        return msg_color

    def debug(self, msg, *args, **kwargs):
        self._log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._log(logging.ERROR, msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self._log(logging.ERROR, msg, *args, **kwargs, exc_info=True)

    def critical(self, msg, *args, **kwargs):
        self._log(logging.CRITICAL, msg, *args, **kwargs)


# noinspection PyPep8
def get_logger(name, level=logging.DEBUG,
               is_add_stream_handler=True, is_add_file_handler=False, is_add_json_file_handler=False,
               log_path=None, json_log_path=None, log_filename=None,
               max_bytes=1000 * 1000 * 1000, back_count=10,
               formatter_template='{asctime} - {host} - "{pathname}:{lineno}" - {funcName} - {name} - {levelname} - {message}'):
    local_params = copy.copy(locals())
    if name in logger_name__logger_obj_map:
        print(f'已存在该命名空间 {name} 日志')
        logger = logger_name__logger_obj_map[name]
        logger.level = level
    else:
        logger = KuaiLogger(**local_params)
        logger_name__logger_obj_map[name] = logger
    return logger


if __name__ == '__main__':
    pass
