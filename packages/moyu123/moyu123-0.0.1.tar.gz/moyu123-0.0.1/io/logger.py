"""
对 loguru 进行重新封装，防止重复生成日志句柄，但是又不失 loguru 原来的便利性
"""
import sys

from loguru._logger import Core
from loguru._logger import Logger


def get_logger(logfile: str = None, rotation: str = '10M'):
    """
    获取日志记录。
    rotation：日志分割形式，rotation=10M 则按10M分割，rotation=00:00 则每日分割。
    """
    # 日志格式
    _format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
    # 获取日志
    logger = Logger(Core(), None, 0, False, False, False, False, True, None, {})
    # 添加文件输出
    if logfile:
        logger.add(logfile, rotation=rotation, encoding='utf-8', format=_format)
    # 输出到控制台
    logger.add(sys.stdout, format=_format)
    return logger
