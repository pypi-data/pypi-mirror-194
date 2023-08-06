import asyncio
import json
import os
import sys
import time
from datetime import datetime as Datetime
from datetime import timezone
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

import nest_asyncio
import pyperclip
import typer
from colorama import Fore

from beni import bcolor, bexecute, bfile, bpath

_app = typer.Typer()


def main():
    nest_asyncio.apply()
    _app()


def exit(errorMsg: str):
    print(errorMsg)
    sys.exit(errorMsg and 1 or 0)


# ------------------------------------------------------------------------


@_app.command('time')
def showtime(
    value: str = typer.Argument('', help='时间戳（支持整形和浮点型）或日期（格式: 2021-11-23）', show_default=False, metavar='[Timestamp or Date]'),
    value2: str = typer.Argument('', help='时间（格式: 09:20:20），只有第一个参数为日期才有意义', show_default=False, metavar='[Time]')
):
    '''
    格式化时间戳

    beni showtime

    beni showtime 1632412740

    beni showtime 1632412740.1234

    beni showtime 2021-9-23

    beni showtime 2021-9-23 09:47:00
    '''

    timestamp: float | None = None
    if not value:
        timestamp = time.time()
    else:
        try:
            timestamp = float(value)
        except:
            try:
                if value2:
                    timestamp = Datetime.strptime(f'{value} {value2}', '%Y-%m-%d %H:%M:%S').timestamp()
                else:
                    timestamp = Datetime.strptime(f'{value}', '%Y-%m-%d').timestamp()
            except:
                pass

    if timestamp is None:
        color = typer.colors.BRIGHT_RED
        typer.secho('参数无效', fg=color)
        typer.secho('\n可使用格式: ', fg=color)
        msgAry = str(showtime.__doc__).strip().replace('\n\n', '\n').split('\n')[1:]
        msgAry = [x.strip() for x in msgAry]
        typer.secho('\n'.join(msgAry), fg=color)
        raise typer.Abort()

    print()
    print(timestamp)
    print()
    localtime = time.localtime(timestamp)
    tzname = time.tzname[(time.daylight and localtime.tm_isdst) and 1 or 0]
    bcolor.printx(time.strftime('%Y-%m-%d %H:%M:%S %z', localtime), tzname, colorList=[Fore.YELLOW])
    print()

    # pytz版本，留作参考别删除
    # tzNameList = [
    #     'Asia/Tokyo',
    #     'Asia/Kolkata',
    #     'Europe/London',
    #     'America/New_York',
    #     'America/Chicago',
    #     'America/Los_Angeles',
    # ]
    # for tzName in tzNameList:
    #     tz = pytz.timezone(tzName)
    #     print(Datetime.fromtimestamp(timestamp, tz).strftime(fmt), tzName)

    datetime_utc = Datetime.fromtimestamp(timestamp, tz=timezone.utc)
    tzname_list = [
        'Australia/Sydney',
        'Asia/Tokyo',
        'Asia/Kolkata',
        'Africa/Cairo',
        'Europe/London',
        'America/Sao_Paulo',
        'America/New_York',
        'America/Chicago',
        'America/Los_Angeles',
    ]
    for tzname in tzname_list:
        datetime_tz = datetime_utc.astimezone(ZoneInfo(tzname))
        dstStr = ''
        dst = datetime_tz.dst()
        if dst:
            dstStr = f'(DST+{dst})'
        print(f'{datetime_tz} {tzname} {dstStr}')

    print()

# ------------------------------------------------------------------------


@_app.command()
def format_json_file(file_path: str, encoding: str = 'utf8'):
    '''格式化 JSON 文件'''
    file = bpath.get(file_path)
    content = file.read_text(encoding=encoding)
    data = json.loads(content)
    file.write_text(json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True), encoding=encoding)


# ------------------------------------------------------------------------


@_app.command()
def venv(
    packages: list[str] = typer.Argument(None),
    path: Path = typer.Option(None, help="指定路径，默认当前目录"),
    clear: bool = typer.Option(False, help='删除venv目录后重新安装，可以保证环境干净'),
    clear_lock: bool = typer.Option(False, help='删除venv.lock文件和venv目录后重新安装，可以保证环境干净的情况下将包更新'),
    mirror: bool = typer.Option(True, help='使用镜像加速（https://pypi.douban.com/simple）')
):
    '''python 虚拟环境配置'''
    path = path or Path(os.getcwd())
    clear = clear or clear_lock

    async def run():
        venvDir = bpath.get(path, 'venv')
        _assertDirOrNotExists(venvDir)
        if clear:
            bpath.remove(venvDir)
        if not venvDir.exists():
            await bexecute.run(f'python.exe -m venv {venvDir}')
        vevnListFile = bpath.get(path, 'venv.list')
        _assertFileOrNotExists(vevnListFile)
        if not vevnListFile.exists():
            await bfile.writeText(vevnListFile, '')
        venvLockFile = bpath.get(path, 'venv.lock')
        _assertFileOrNotExists(venvLockFile)
        if clear_lock:
            bpath.remove(venvLockFile)
        if packages:
            await tidyVenvFile(vevnListFile, packages)
            await tidyVenvFile(venvLockFile, packages)
        targetFile = venvLockFile if venvLockFile.exists() else vevnListFile
        pip = bpath.get(venvDir, 'Scripts/pip.exe')
        await pipInstall(pip, targetFile)
        await bexecute.run(f'{pip} freeze > {venvLockFile}')

    async def pipInstall(pip: Path, file: Path):

        python = pip.with_name('python.exe')
        assert python.is_file()
        await bexecute.run(f'{python} -m pip install --upgrade pip {"-i https://pypi.douban.com/simple" if mirror else "" }')

        assert pip.is_file()
        cmdAry = [
            f'{pip} install',
        ]
        if mirror:
            cmdAry.insert(0, f'{pip} install -i https://pypi.douban.com/simple')
        lineSet = {x.strip() for x in (await bfile.readText(file)).split('\n')}
        lineSet = set(filter(lambda x: x, lineSet))
        specLineSet = set(filter(lambda x: x.startswith('benimang'), lineSet))
        normalLineSet = lineSet - specLineSet
        async with bpath.useTempFile() as tempFile:
            for targetSet in (specLineSet, normalLineSet):
                await bfile.writeText(tempFile, '\n'.join(targetSet))
                isOk = False
                for cmd in cmdAry:
                    isOk = isOk or not await bexecute.run(f'{cmd} -r {tempFile}')
                assert isOk, '执行失败'

    async def tidyVenvFile(file: Path, addPackages: list[str]):
        addPackageNames = [getPackageName(x) for x in addPackages]
        ary = (await bfile.readText(file)).strip().replace('\r\n', '\n').replace('\r\n', '\n').split('\n')
        ary = list(filter(lambda x: getPackageName(x) not in addPackageNames, ary))
        ary.extend(addPackageNames)
        ary.sort()
        await bfile.writeText(file, '\n'.join(ary).strip())

    def getPackageName(value: str):
        sepList = ['>', '<', '=']
        for sep in sepList:
            if sep in value:
                return value.split(sep)[0]
        return value

    asyncio.run(run())


def _assertFileOrNotExists(file: Path):
    assert file.is_file() or not file.exists(), f'必须是文件 {file=}'


def _assertDirOrNotExists(folder: Path):
    assert folder.is_dir() or not folder.exists(), f'必须是文件 {folder=}'


# ------------------------------------------------------------------------


@_app.command()
def bin(
    name: str = typer.Argument(None, help="如果有多个使用,分割"),
    is_file: bool = typer.Option(False, '--is-file', '-f', help="文件形式指定参数，行为单位"),
    ak: str = typer.Option(..., help="七牛云账号AK"),
    sk: str = typer.Option(..., help="七牛云账号SK"),
    output: Optional[Path] = typer.Option(None, '--output', '-o', help="本地保存路径")
):
    '''从七牛云下载执行文件'''
    from beni.bqiniusdk import QiniuBucket
    try:
        bucketName = 'pytask'
        bucketUrl = 'http://qiniu-cdn.pytask.com'
        if output is None:
            output = Path(os.curdir)
        bucket = QiniuBucket(bucketName, bucketUrl, ak, sk)
        targetList: list[str] = []
        if is_file:
            content = asyncio.run(
                bfile.readText(Path(name))
            )
            targetList.extend(content.replace('\r\n', '\n').split('\n'))
        else:
            targetList.extend(name.strip().split(','))
        for target in targetList:
            file = output.joinpath(target).resolve()
            if file.exists():
                print(f'exists {file}')
            else:
                key = f'bin/{target}.zip'
                bucket.downloadUnzipPrivateFile(key, output)
                bcolor.printGreen(f'added  {file}')
    except Exception as e:
        print(e)


# ------------------------------------------------------------------------


@_app.command()
def proxy(
    port: int = typer.Option(15236, help="代理服务器端口"),
):
    '''生成终端设置代理服务器的命令'''
    msg = '\r\n'.join([
        f'set http_proxy=http://localhost:{port}',
        f'set https_proxy=http://localhost:{port}',
        f'set all_proxy=http://localhost:{port}',
        '',
    ])
    print('\r\n' + msg)
    pyperclip.copy(msg)
    print('已复制')
