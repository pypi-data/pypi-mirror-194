import datetime
import time
from datetime import datetime as Datetime
from datetime import timedelta

from beni import bhttp

_serverDatetime = datetime.datetime.now()
_initTime = time.monotonic()


async def networkTime():
    _, response = await bhttp.get('https://www.baidu.com')
    date_str = response.headers['Date']
    datetime = Datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT') + timedelta(hours=8)
    return datetime


async def initServerDatetime():
    global _serverDatetime, _initTime
    _serverDatetime = await networkTime()
    _initTime = time.monotonic()


def nowDatetime():
    return _serverDatetime + datetime.timedelta(seconds=time.monotonic() - _initTime)


def nowDate():
    return nowDatetime().date()


def nowTime():
    return nowDatetime().time()


def nowTimestamp():
    return nowDatetime().timestamp()


def nowDatetimeStr():
    return nowDatetime().strftime(r'%Y-%m-%d %H:%M:%S')


def nowDateStr():
    return nowDatetime().strftime(r'%Y-%m-%d')


def nowTimeStr():
    return nowDatetime().strftime(r'%H:%M:%S')


def makeDatetime(date_str: str, fmt: str = r'%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(date_str, fmt)


def makeDate(date_str: str, fmt: str = r'%Y-%m-%d'):
    return datetime.datetime.strptime(date_str, fmt).date()


# def tomorrowDatetime():
#     return datetime.datetime.combine(
#         nowDate(),
#         datetime.time(),
#     )


# def foreverDatetime():
#     return datetime.datetime(9999, 1, 1)
