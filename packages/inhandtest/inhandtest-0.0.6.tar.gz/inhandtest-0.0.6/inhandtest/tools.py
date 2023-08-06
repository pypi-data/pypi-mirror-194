# -*- coding: utf-8 -*-
# @Time    : 2023/1/31 16:42:40
# @Author  : Pane Li
# @File    : tools.py
"""
tools

"""
import logging
import time
import datetime
import pytz


def loop_inspector(flag='status', timeout=90, interval=5, assertion=True):
    """装饰器，期望接收函数返回的值为True，如果为False时进行轮询，直至超时失败，如果正确就退出

    :param flag:  功能名称，用以输出日志，如果不填  默认为’状态’二字
    :param timeout:  循环检测超时时间
    :param interval:  循环检测时间间隔
    :param assertion: 默认期望断言，如果为False时 返回值
    :return:  assertion为False时，返回函数的值
    """

    def timeout_(func):
        def inspector(*args, **kwargs):
            for i in range(0, timeout + 1, interval):
                result = func(*args, **kwargs)
                if not result:
                    logging.info(f'{flag} assert failure, wait for {interval}s inspection')
                    time.sleep(interval)
                    continue
                else:
                    logging.info(f'{flag} assert normal')
                    return result
            else:
                if assertion:
                    raise AssertionError(f'{flag} assert timeout failure')

        return inspector

    return timeout_


def dict_merge(*dicts):
    """合并多个字典

    :param dicts:
    :return:
    """
    result = {}
    for dict_ in dicts:
        if dict_ is not None:
            result.update(dict_)
    return result


def dict_flatten(in_dict, separator=":", dict_out=None, parent_key=None):
    """ 平铺字典

    :param in_dict: 输入的字典
    :param separator: 连接符号
    :param dict_out:
    :param parent_key:
    :return: dict
    """
    if dict_out is None:
        dict_out = {}

    for k, v in in_dict.items():
        k = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            dict_flatten(in_dict=v, dict_out=dict_out, parent_key=k)
            continue

        dict_out[k] = v

    return dict_out


def timezone_change(time_str, src_timezone, dst_timezone=None, time_format=None):
    """
    将任一时区的时间转换成指定时区的时间
    如果没有指定目的时区，则默认转换成当地时区  时区参考https://www.beijing-time.org/shiqu/

    :param time_str:
    :param src_timezone: 要转换的源时区，如"Asia/Shanghai" 即东八区， 'Europe/London' 零时区  'Canada/Eastern' 西五区 UTC-5
    :param dst_timezone: 要转换的目的时区，如"Asia/Shanghai", 如果没有指定目的时区，则默认转换成当地时区
    :param time_format: 默认格式"%Y-%m-%d %H:%M:%S"
    :return: str, 字符串时间格式
    """
    if not time_format:
        time_format = "%Y-%m-%d %H:%M:%S"

    # 将字符串时间格式转换成datetime形式
    old_dt = datetime.datetime.strptime(time_str, time_format)

    # 将源时区的datetime形式转换成GMT时区(UTC+0)的datetime形式
    dt = pytz.timezone(src_timezone).localize(old_dt)
    utc_dt = pytz.utc.normalize(dt.astimezone(pytz.utc))

    # 将GMT时区的datetime形式转换成指定的目的时区的datetime形式
    if dst_timezone:
        _timezone = pytz.timezone(dst_timezone)
        new_dt = _timezone.normalize(utc_dt.astimezone(_timezone))
    else:
        # 未指定目的时间，默认转换成当地时区
        new_dt = utc_dt.astimezone()
    # 转换成字符串时间格式
    return new_dt.strftime(time_format)


if __name__ == '__main__':
    import sys
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO,
                        stream=sys.stdout)
    print(timezone_change('2022-02-18 13:39:32', 'Canada/Eastern', 'Asia/Shanghai'))
    # print(dict_merge({"a": 1}, {"a": 2}, None))
    # print(dict_flatten({'key': {'key1': 'value1'}, 'key2': [0, 1]}))
