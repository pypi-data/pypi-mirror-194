#!/usr/bin/python3
import os
import sys
import time
import inspect
from threading import RLock
import threading
from typing import Iterable

from IOS_SHOGUN import BufferBytes, consoles
import enum


class console_colors:
    """
        "console_color" class:reset all colors with colors.reset; two
        subclasses foreground for foreground
        and background for background; use as colors.subclass.colorname.
        i.e. colors.foreground.red or colors.background.green also, the generic bold, disable,
        underline, reverse, strike through,
        and invisible work with the main class i.e. colors.bold
        author：ios_shogun-AtomicJun
        date:2023-2-24
        self:IOS_SHOGUN_studio
    """
    re = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    under_line = '\033[04m'
    reverse = '\033[07m'
    de_line = '\033[09m'
    invisible = '\033[08m'

    class foreground:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightGrey = '\033[37m'
        darkGrey = '\033[90m'
        lightRed = '\033[91m'
        lightGreen = '\033[92m'
        yellow = '\033[93m'
        lightBlue = '\033[94m'
        pink = '\033[95m'
        lightCyan = '\033[96m'
        end = '\033[0m'
        pass

    class background:
        yellow = '\033[93m'
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightGrey = '\033[47m'
        pass

    pass


class bufferError(BaseException, object):
    def __init__(self, *value) -> None:
        self.value = value
        pass

    def add__(self, *value) -> None:
        for value_ in value:
            if value_ is str and value_ != '':
                self.value.__add__(value_)
        pass

    @classmethod
    def build(cls, *value):
        return cls(value)
        pass

    def __str__(self):
        return repr(f"Buffer error!:->{self.value}-TIME{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        pass


pass


@enum.unique
class BufferState(enum.Enum):
    empty: str = 'empty'
    Full: str = 'Full'
    boundless: str = 'boundless'
    remainder: str = 'remainder'
    limited: str = 'limited'


class BufferByte(BufferBytes.BufferBytes_):
    """
    The byte-buffered queue, suitable for multithreaded operations and use, is a basic buffered queue
    His basic functions are divided into: queue,push, pop, query, persist, get, persist_put, BufferSpace,
    GetBufferSpace, QueryBufferSpace, detailed features, see details
    author：ios_shogun-AtomicJun
    date:2023-2-24
    self:IOS_SHOGUN_studio
    """
    BOUNDLESS: int = 1 << 3
    LIMITED: int = 2 << 3

    def __init__(self, **data: bytes | int | None):
        """
        Create a blocking byte buffer, you can give him the initial item,
        you can also define its size, which defaults to infinity
        """
        self.__BufferLock: RLock = RLock()
        self.__SpaceRemaining: int = -1
        self.__ByteQuery: list[bytes] = []
        self.__Index: dict[str, int] = {}
        self.__allState__ = ['empty', 'Full', 'boundless', 'remainder', 'limited']
        self.__state: str = self.__allState__[2]
        self.__state_Space: str = self.__allState__[0]

        super().__init__(**data)
        self.__slots__ = ['Injection_NET']
        try:
            if data['data'] is not None:
                try:
                    self.__BufferLock.acquire()
                    if isinstance(data['data'], int):
                        if data['data'] > 0:
                            self.__state = self.__allState__[4]
                            self.__SpaceRemaining = data['data']
                        elif data['data'] <= 0:
                            raise bufferError("data size <= 0 try again setting.")
                    elif len(data) > 0 and isinstance(data, dict):
                        for dataKey, DataValue in data:
                            if isinstance(DataValue, bytes) and len(DataValue) > 0:
                                self.__ByteQuery.append(DataValue)
                                self.__Index.setdefault(f'{dataKey}', len(self.__ByteQuery) - 1)
                            else:
                                raise bufferError("The key value is not a byte array.")
                    else:
                        raise bufferError("data size <=0 or data not is dict.")
                finally:
                    self.__BufferLock.release()
            else:
                self.__ShortCheck(len(self.__ByteQuery))
                self.__state = self.__allState__[2]
        except Exception:
            raise bufferError("If you can't find the standard definition, use None or data=100!]")

    pass

    def Sample_Push(self, data: bytes) -> None:
        """
        Push into the cache queue, just divided into it, in the form of a dictionary
        And into a dictionary form - current length + list index
        """
        if isinstance(data, bytes):
            if isinstance(self.__state, str) and self.__state.__eq__(self.__allState__[2]):
                try:
                    self.__BufferLock.acquire()
                    if len(data) > 0:
                        self.__ByteQuery.append(data)
                        length_ = len(self.__ByteQuery)
                        self.__Index.setdefault(f'{length_ }', length_ - 1)
                    else:
                        raise bufferError("The key value is not a byte array.")
                finally:
                    self.__BufferLock.release()
            elif (isinstance(self.__state, str) and self.__state.__eq__(self.__allState__[4])
                  and self.__state != self.__allState__[2]) or (self.__state_Space.__eq__(self.__allState__[3])
                                                                or self.__state_Space.__eq__(self.__allState__[0])):
                if len(data) > 0 and (len(self.__ByteQuery) <= self.__SpaceRemaining):
                    try:
                        self.__BufferLock.acquire()
                        self.__state_Space = self.__allState__[3]
                        if len(data) > 0:
                            if len(self.__ByteQuery) <= self.__SpaceRemaining:
                                self.__ByteQuery.append(data)
                                length_ = len(self.__ByteQuery)
                                self.__Index.setdefault(f'{length_}', length_ - 1)
                            else:
                                self.__ShortCheck(len(self.__ByteQuery))
                                raise bufferError("The buffer block is full.")
                        else:
                            raise bufferError("The key value is not a byte array.")
                    finally:
                        self.__BufferLock.release()
                    self.__ShortCheck(len(self.__ByteQuery))
        pass

    def push(self, **data: bytes) -> None:
        """
        Push into the cache queue, just divided into it, in the form of a dictionary
        """
        if isinstance(data, dict):
            if isinstance(self.__state, str) and self.__state.__eq__(self.__allState__[2]):
                try:
                    self.__BufferLock.acquire()
                    for dataKey, DataValue in data.items():
                        if isinstance(DataValue, bytes) and len(DataValue) > 0:
                            self.__ByteQuery.append(DataValue)
                            self.__Index.setdefault(f'{dataKey}', len(self.__ByteQuery) - 1)
                        else:
                            raise bufferError("The key value is not a byte array.")
                finally:
                    self.__BufferLock.release()
            elif (isinstance(self.__state, str) and self.__state.__eq__(self.__allState__[4])
                  and self.__state != self.__allState__[2]) or (self.__state_Space.__eq__(self.__allState__[3])
                                                                or self.__state_Space.__eq__(self.__allState__[0])):
                if len(data) > 0 and (len(self.__ByteQuery) <= self.__SpaceRemaining):
                    try:
                        self.__BufferLock.acquire()
                        self.__state_Space = self.__allState__[3]
                        for dataKey, DataValue in data.items():
                            if isinstance(DataValue, bytes) and len(DataValue) > 0:
                                if len(self.__ByteQuery) <= self.__SpaceRemaining:
                                    self.__ByteQuery.append(DataValue)
                                    self.__Index.setdefault(f'{dataKey}', len(self.__ByteQuery) - 1)
                                else:
                                    self.__ShortCheck(len(self.__ByteQuery))
                                    raise bufferError("The buffer block is full.")
                            else:
                                raise bufferError("The key value is not a byte array.")
                    finally:
                        self.__BufferLock.release()
                    self.__ShortCheck(len(self.__ByteQuery))
        pass

    def Push(self, data: list[bytes]) -> None:
        """
        Pushed into the cache queue in the form of a list, just divided into cache queues,
        and IL turned into a dictionary in the form - current length + list index
        """
        if isinstance(data, list):
            if isinstance(self.__state, str) and self.__state.__eq__(self.__allState__[2]):
                try:
                    self.__BufferLock.acquire()
                    for DataValue in data:
                        if isinstance(DataValue, bytes) and len(DataValue) > 0:
                            self.__ByteQuery.append(DataValue)
                            length_ = len(self.__ByteQuery)
                            self.__Index.setdefault(f'{(length_ + 1)}', length_ - 1)
                        else:
                            raise bufferError("The key value is not a byte array.")
                finally:
                    self.__BufferLock.release()
            elif (isinstance(self.__state, str) and self.__state.__eq__(self.__allState__[4])
                  and self.__state != self.__allState__[2]) or (self.__state_Space.__eq__(self.__allState__[3])
                                                                or self.__state_Space.__eq__(self.__allState__[0])):
                if len(data) > 0 and (len(self.__ByteQuery) <= self.__SpaceRemaining):
                    try:
                        self.__BufferLock.acquire()
                        self.__state_Space = self.__allState__[3]
                        for DataValue in data:
                            if isinstance(DataValue, bytes) and len(DataValue) > 0:
                                if len(self.__ByteQuery) <= self.__SpaceRemaining:
                                    self.__ByteQuery.append(DataValue)
                                    length_ = len(self.__ByteQuery)
                                    self.__Index.setdefault(f'{(length_ + 1)}', length_ - 1)
                                else:
                                    self.__ShortCheck(len(self.__ByteQuery))
                                    raise bufferError("The buffer block is full.")
                            else:
                                raise bufferError("The key value is not a byte array.")
                    finally:
                        self.__BufferLock.release()
                    self.__ShortCheck(len(self.__ByteQuery))
        pass

    def __Del(self, target: dict | list, key: str) -> None:
        target.pop(key)

    def clearBuffered(self) -> None:
        """
            Empty all queues for the buffer
        """
        try:
            self.__BufferLock.acquire()
            self.__ByteQuery.clear()
            self.clearIndex()
            self.__state_Space = self.__allState__[0]
        finally:
            self.__BufferLock.release()

    def clearIndex(self) -> None:
        """
            Empty all index for the buffer
        """
        try:
            self.__BufferLock.acquire()
            self.__Index.clear()
        finally:
            self.__BufferLock.release()

    def pop(self) -> bytes | None:
        """
            The first data of the buffer is removed from the header and the data is returned
        """
        if self.__state_Space != self.__allState__[0]:
            return None
        elif self.__state_Space.__eq__(self.__allState__[1]) or \
                self.__state_Space.__eq__(self.__allState__[3]):
            self.__BufferLock.acquire()
            data_buffer: bytes = self.__ByteQuery[0]
            index_key: str = list(self.__Index.keys())[0]
            self.__Del(self.__ByteQuery, index_key)
            self.__Del(self.__Index, index_key)
            self.__BufferLock.release()
            return data_buffer
        pass

    def __ShortCheck(self, en: int) -> None:
        if self.__state.__eq__(self.__allState__[4]):
            if en > 0:
                if en < self.__SpaceRemaining:
                    self.__state_Space = self.__allState__[3]
                elif en == self.__SpaceRemaining:
                    self.__state_Space = self.__allState__[1]
            elif en <= 0:
                self.__state_Space = self.__allState__[0]
        else:
            if en > 0:
                self.__state_Space = self.__allState__[3]
            elif en <= 0:
                self.__state_Space = self.__allState__[0]
                if len(self.__Index) != 0:
                    self.clearIndex()

    pass

    def query(self) -> str:
        """
            The status of the query buffer, generally divided into, is empty or full |
            with a persistent license
        """
        self.__ShortCheck(len(self.__ByteQuery))
        if self.__state.__eq__(self.__allState__[4]):
            return self.__state_Space
        else:
            return self.__state_Space

    pass

    def get(self, index: int | str) -> bytes | None:
        """
            More dictionaries or indexes fetch objects into buffers
        """
        self.__ShortCheck(len(self.__ByteQuery))
        if self.query().__eq__(self.__allState__[0]):
            return None
        else:
            if isinstance(index, int):
                if len(self.__ByteQuery) >= index > 0:
                    return self.__ByteQuery[index - 1]
                else:
                    return None
            else:
                index_ = self.__Index.get(index)
                return self.__ByteQuery[index_-1]

    pass

    def QueryBufferSpace(self) -> int | None:
        """
            Query the remaining buffer space, expressed as the maximum space used in infinite mode
        """
        QueryLen = len(self.__ByteQuery)
        self.__ShortCheck(QueryLen)
        if self.__state.__eq__(self.__allState__[2]):
            return None
        else:
            return self.__SpaceRemaining - QueryLen

    pass

    def __updateMax(self, AC: int) -> None:
        self.__SpaceRemaining = AC

    pass

    def GetBufferSpace(self) -> int:
        """
            Gets the space used by the current buffer
        """
        self.__ShortCheck(len(self.__ByteQuery))
        if self.__state.__eq__(self.__allState__[2]):
            if self.query().__eq__(self.__allState__[0]):
                return 0
            else:
                return len(self.__ByteQuery)
        else:
            if self.query().__eq__(self.__allState__[0]):
                return 0
            elif self.query().__eq__(self.__allState__[1]):
                return self.__SpaceRemaining
            else:
                return len(self.__ByteQuery)

    pass

    def BufferSpace(self, index: int) -> None:
        """
            Manually changing the buffer space at a later stage cannot be smaller
            than the current space
        """
        self.__ShortCheck(len(self.__ByteQuery))
        if self.__state.__eq__(self.__allState__[4]):
            if index > len(self.__ByteQuery):

                self.__updateMax(index)
            else:
                raise bufferError('The maximum queue to be modified is less than the current queue.')
        else:
            raise bufferError('It is currently in infinite mode.')

    pass

    def persist(self, path: str) -> bool:
        """
            To persist all buffer data, you need to provide all the storage methods
        """
        self.__ShortCheck(len(self.__ByteQuery))
        if self.__state_Space.__eq__(self.__allState__[3]) \
                or self.__state_Space.__eq__(self.__allState__[1]):
            try:
                self.__BufferLock.acquire()
                with open(path, 'ab+') as dataPoint:
                    datas_persist = self.__ByteQuery.copy()
                    for dataInfo in datas_persist:
                        dataPoint.write(dataInfo)
                self.__BufferLock.release()
            except OSError as os_:
                self.__BufferLock.release()
                assert bufferError(f'->TypeError:OSError:import->{os_}')
                return False
            return True
        else:
            return False

    pass

    def ExportData(self) -> list[bytes] | None:
        """
            Export all data
        """
        self.__ShortCheck(len(self.__ByteQuery))
        if self.__state_Space.__eq__(self.__allState__[3]) \
                or self.__state_Space.__eq__(self.__allState__[1]):
            return self.__ByteQuery.copy()
        else:
            return None

    pass

    def persist_put(self, index: int | str, path: str) -> bool:
        """
            Persist individual buffer objects based on dictionaries or indexes
        """
        try:
            dataSet: bytes | None = self.get(index)
            if dataSet is not None:
                self.__BufferLock.acquire()
                with open(path, 'ab+') as dataPoint:
                    datas_persist = self.__ByteQuery.copy()
                    for dataInfo in datas_persist:
                        dataPoint.write(dataInfo)
                self.__BufferLock.release()
        except OSError as os_:
            self.__BufferLock.release()
            assert bufferError(f'->TypeError:OSError:import->{os_}')
            return False
        return True

    pass

    def ClearExportData(self) -> list[bytes] | None:
        """
            Export all bytes of data and clear all data
        """
        self.__ShortCheck(len(self.__ByteQuery))
        if self.__state_Space.__eq__(self.__allState__[3]) \
                or self.__state_Space.__eq__(self.__allState__[1]):
            datas: list[bytes] = self.__ByteQuery.copy()
            self.clearBuffered()
            return datas
        else:
            return None

    pass

    def ReentrancyMode(self, mode: int, accessibility: int = -1) -> None:
        """
            [Please refer to it BOUNDLESS|LIMITED]
        """
        self.__BufferLock.acquire()
        if self.__state.__eq__(self.__allState__[2]):
            self.__SpaceRemaining = accessibility
            if accessibility != -1:
                if mode.__eq__(self.LIMITED):
                    if accessibility > len(self.__ByteQuery):
                        self.__updateMax(accessibility)
                        self.__state = self.__allState__[4]
                else:
                    self.__BufferLock.release()
                    raise bufferError('The maximum queue to be modified is less than the current queue.')
            else:
                self.__BufferLock.release()
                raise bufferError('When turning finite in infinite mode, you need to set a finite boundary.')
        else:
            self.__state = self.__allState__[2]
            self.__updateMax(-1)
        self.__BufferLock.release()

    pass

    def __repr__(self):
        self.__ShortCheck(len(self.__ByteQuery))
        return f'bufferByte[mode state:{self.__state},space state:{self.__state_Space}' \
               f',maxSpace:{self.__SpaceRemaining},available:{self.QueryBufferSpace()}]'

    pass

    def opencv(self):
        """
        Gets a view object that summarizes the buffer
        :return:Gets a view object that summarizes the buffer
        """
        return self.__repr__()

    pass

    def __dir__(self) -> Iterable[str]:
        return Iterable.__iter__(['__state:mode', '__state_Space:space state', 'BOUNDLESS:static mode',
                                  'LIMITED:static mode', 'push', 'clearBuffered', 'clearIndex', 'pop',
                                  'query', 'get', 'QueryBufferSpace', 'BufferSpace', 'persist', 'ExportData',
                                  'ClearExportData', 'ReentrancyMode'
                                  ])

    pass

    def __del__(self):
        self.clearBuffered()
        try:
            self.__BufferLock.release()
        except RuntimeError:
            pass

    pass


pass


def success(text: str = "") -> None:
    if text != "":
        print(console_colors.background.black, "", console_colors.foreground.lightGreen, str(text))
    else:
        print(console_colors.background.black, str("\n"), console_colors.foreground.lightGreen, str(text))
    pass


def error(text: str = "") -> None:
    if text != "":
        print(console_colors.background.black, "", console_colors.foreground.lightRed, str(text))
    else:
        print(console_colors.background.black, str("\n"), console_colors.foreground.lightRed, str(text))
    pass


def ware(text: str = "") -> None:
    if text != "":
        print(console_colors.background.black, "", console_colors.foreground.yellow, str(text))
    else:
        print(console_colors.background.black, str("\n"), console_colors.foreground.yellow, str(text))
    pass


def log(text: str = "") -> None:
    if text != "":
        print(console_colors.foreground.end, "", console_colors.foreground.end, str(text))
    else:
        print(console_colors.foreground.end, str("\n"), console_colors.foreground.end, str(text))
    pass


def info(text: str = "", K: bool = False) -> None:
    if text != "":
        if K is False:
            print(console_colors.background.black, "", console_colors.foreground.lightBlue, str(text))
        elif K is True:
            print(console_colors.background.black, "", console_colors.foreground.lightBlue, str(text))
    else:
        print(console_colors.background.black, str("\n"), console_colors.foreground.lightBlue, str(text))
    pass


class console(consoles.console_):
    """
        The 'console' micro-logging system carries its own 'BufferByte' when using the console,
        which can be used for multithreaded operation processing, which is divided into 5 levels - error,
        warning, message. Debugging, correct, each level has a different effect,
        of course you can go through the 'disposition' configuration of it,
        Export can drive IO logs Of course, you can also configure the log name,
        and whether it is continuous,Configure via 'Continuity'
        In a continuous state, each 'debug...' debug will drive the IO log generation and
        the emptying of 'bufferByte', 'bufferByte' it is in unlimited mode - you can set the same log path,
        I have introduced simple information, please go down for information
        author：ios_shogun-AtomicJun
        date:2023-2-24
        self:IOS_SHOGUN_studio
    """
    ERROR = 40
    WARN = 30
    INFO = 20
    DEBUG = 10
    SUCCESS = 0
    __all__ = ['log', 'ware', 'error', 'success', 'info', 'console', 'consoles', 'bufferError', 'BufferState',
               'BufferByte', 'BufferBytes', 'console_colors']

    def __init__(self) -> None:
        self.__Lock: RLock = RLock()
        self.__name: str = str(f'{os.getpid()}-Log')
        self.__time = None
        self.__filename = None
        self.__pathname = None
        self.__levelName = None
        self.__functionName = None
        self.__processName = None
        self.__ThreadID = None
        self.__LineID = None
        self.__disposition: str = 'time-LineID-levelName'
        self.__bufferedLog: BufferByte = BufferByte(data=None)
        self.__path: str = f'./{self.__name}'
        self._Level = {
            'SUCCESS': self.SUCCESS,
            'DEBUG': self.DEBUG,
            'INFO': self.INFO,
            'WARN': self.WARN,
            'ERROR': self.ERROR,
        }
        self.__Continuity: bool = False
        super().__init__()
        self.__slots__ = ['InjectionConsole_NET']
        pass

    def log(self, text: str, **attract) -> None:
        """
        Vernacular information: We display this log message in plain bold
        """
        if text != "":
            print(console_colors.foreground.end, "", console_colors.foreground.end, str(text))
            Specific: list[str] = [f'__{Data}' for Data in self.__decompose()]
            if '__functionName' in Specific:
                self.__functionName: str = inspect.getmodule(inspect.stack()[2][0]).f_code.co_name
            elif '__LineID' in Specific:
                self.__LineID: str = f"invoke:{inspect.stack()[1][0].f_lineno}:Code:{inspect.stack()[0][0].f_lineno}"
            self.__onCreate(Specific, self.DEBUG)
            self.__push("shogun-model", **attract)
        else:
            print(console_colors.foreground.end, str("\n"), console_colors.foreground.end, str(text))

    pass

    def __decompose(self) -> list[str]:
        return self.__disposition.split('-')

    def __push(self, exegesis: str, **attract) -> None:
        Data_info_: list[bytes] = [bytes(f'{self[f"__{name}"]}', 'utf-8') for name in self.__decompose()]
        if list(attract.values())[0] is not None:
            for attract_key, attract_value in attract:
                Data_info_.append(bytes(f'{attract_key}->{attract}', 'utf-8'))
        Data_info_.append(bytes(f"\t\r\n{exegesis}+\n", 'utf-8'))
        if self.__Continuity is False:
            self.__bufferedLog.Push(Data_info_)
        else:
            self.__bufferedLog.Push(Data_info_)
            self.Export()
        pass

    def __getitem__(self, msg):
        match msg:
            case '__name':
                return self.__name
            case '__time':
                return self.__time
            case '__filename':
                return self.__filename
            case '__pathname':
                return self.__pathname
            case '__levelName':
                return self.__levelName
            case '__functionName':
                return self.__functionName
            case '__processName':
                return self.__processName
            case '__ThreadID':
                return self.__ThreadID
            case '__LineID':
                return self.__LineID
            case '__disposition':
                return self.__disposition
            case '__bufferedLog':
                return self.__bufferedLog
            case '__path':
                return self.__path
        pass

    def ware(self, text: str, **attract) -> None:
        """
        Warning: We use yellow to indicate this information log
        """
        if text != "":
            print(console_colors.background.black, "", console_colors.foreground.yellow, str(text))
            Specific: list[str] = [f'__{Data}' for Data in self.__decompose()]
            if '__functionName' in Specific:
                self.__functionName: str = inspect.getmodule(inspect.stack()[2][0]).f_code.co_name
            elif '__LineID' in Specific:
                self.__LineID: str = f"invoke:{inspect.stack()[1][0].f_lineno}:Code:{inspect.stack()[0][0].f_lineno}"
            self.__onCreate(Specific, self.WARN)
            self.__push("shogun-model", **attract)
        else:
            print(console_colors.background.black, str("\n"), console_colors.foreground.yellow, str(text))

    pass

    def error(self, text: str, **attract) -> None:
        """
        The error message, which we indicate in red, is this log
        """
        if text != "":
            print(console_colors.background.black, "", console_colors.foreground.lightRed, str(text))
            Specific: list[str] = [f'__{Data}' for Data in self.__decompose()]
            if '__functionName' in Specific:
                self.__functionName: str = inspect.getmodule(inspect.stack()[2][0]).f_code.co_name
            elif '__LineID' in Specific:
                self.__LineID: str = f"invoke:{inspect.stack()[1][0].f_lineno}:Code:{inspect.stack()[0][0].f_lineno}"
            self.__onCreate(Specific, self.ERROR)
            self.__push("shogun-model", **attract)
        else:
            print(console_colors.background.black, str("\n"), console_colors.foreground.lightRed, str(text))

    pass

    def __onCreate(self, decompose: list[str], level: int) -> None:
        for data in decompose:
            if data.__eq__('__time'):
                self.__time: str = " " + time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + " "
            elif data.__eq__('__filename'):
                self.__filename: str = " " + os.path.basename(sys.argv[0]) + " "
            elif data.__eq__('__pathname'):
                self.__pathname: str = " " + os.getcwd() + " "
            elif data.__eq__('__levelName'):
                self.__levelName: str = " " + list(self._Level)[int(level / 10)] + " "
            elif data.__eq__('__processName'):
                self.__processName: str = " " + str(os.path.abspath(__file__)) + " "
            elif data.__eq__('__ThreadID'):
                self.__ThreadID: str = " " + str(threading.current_thread().ident) + " "
            elif data.__eq__('__disposition'):
                self.__disposition: str = 'time-processName-pathname-LineID-levelName'
            elif data.__eq__('__path'):
                self.__path: str = f'./{self.__name}.txt'

    pass

    def success(self, text: str, **attract) -> None:
        """
        The correct information, which we indicate in green, is this log
        """
        if text != "":
            print(console_colors.background.black, "", console_colors.foreground.lightGreen, str(text))
            Specific: list[str] = [f'__{Data}' for Data in self.__decompose()]
            if '__functionName' in Specific:
                self.__functionName: str = inspect.getmodule(inspect.stack()[2][0]).f_code.co_name
            elif '__LineID' in Specific:
                self.__LineID: str = f"invoke:{inspect.stack()[1][0].f_lineno}:Code:{inspect.stack()[0][0].f_lineno}"
            self.__onCreate(Specific, self.SUCCESS)
            self.__push("shogun-model", **attract)
        else:
            print(console_colors.background.black, str("\n"), console_colors.foreground.lightGreen, str(text))

    pass

    def info(self, text: str, K: bool, **attract) -> None:
        """
        This is general information, and we use black to represent this log
        """
        if text != "":
            if K is False:
                print(console_colors.background.black, "", console_colors.foreground.lightBlue, str(text))
            elif K is True:
                print(console_colors.background.black, "", console_colors.foreground.lightBlue, str(text))
            Specific: list[str] = self.__decompose()
            if '__functionName' in Specific:
                self.__functionName: str = inspect.getmodule(inspect.stack()[2][0]).f_code.co_name
            elif '__LineID' in Specific:
                self.__LineID: str = f"invoke:{inspect.stack()[1][0].f_lineno}:Code:{inspect.stack()[0][0].f_lineno}"
            self.__onCreate(Specific, self.INFO)
            self.__push("[LogName-shogun-model]", **attract)
        else:
            print(console_colors.background.black, str("\n"), console_colors.foreground.lightBlue, str(text))

    pass

    def logName(self, Info: str) -> None:
        if Info != '':
            self.__Lock.acquire()
            self.__name = Info
            self.__Lock.release()
        else:
            assert AttributeError('Configuration information cannot be empty')

    pass

    def disposition(self, path: str, Info: str) -> None:
        if Info != '':
            self.__Lock.acquire()
            self.__disposition = Info
            self.__path = path
            self.__Lock.release()
        else:
            assert AttributeError('Configuration information cannot be empty')

    pass

    def Export(self) -> bool:
        if self.__bufferedLog.query() == BufferState.empty:
            return False
        else:
            try:
                self.__Lock.acquire()
                self.__onCreate(['__path'], -1)
                self.__bufferedLog.persist(self.__path)
            except OSError:
                self.__Lock.release()
                return False
        pass

    def Continuity(self, Continuity: bool) -> None:
        try:
            self.__Lock.acquire()
            self.__Continuity = Continuity
        finally:
            self.__Lock.release()
        pass

    def __repr__(self):
        return f'shogun-console-model:[disposition:{self.__disposition},buffered:{self.__bufferedLog}]'
        pass

    def __dir__(self) -> Iterable[str]:
        return Iterable.__iter__(['SUCCESS', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'Continuity', 'Export', 'disposition',
                                  'logName'])
        pass


pass
