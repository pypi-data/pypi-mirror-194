#!/usr/bin/python3
class BufferBytes_(object):
    """
        The byte-buffered queue, suitable for multithreaded operations and use, is a basic buffered queue
        His basic functions are divided into: queue,push, pop, query, persist, get, persist_put, BufferSpace,
        GetBufferSpace, QueryBufferSpace, detailed features, see details
        author：ios_shogun-AtomicJun
        date:2023-2-24
        self:IOS_SHOGUN_studio
    """

    def __init__(self, **data: bytes | int | None) -> None:
        """
            Create a blocking byte buffer, you can give him the initial item,
            you can also define its size, which defaults to infinity
        """

    pass

    def queue(self, ts: int, **data: bytes | None) -> None:
        """
            Cache queue, tuple storage, you can set his response time in milliseconds
            Of course you can set this as None, which is the default
        """

    pass

    def push(self, **data: bytes, ) -> None:
        """
            Push into the cache queue, just divided into it, in the form of a dictionary
        """

    pass

    def pop(self) -> bytes | None:
        """
            The first data of the buffer is removed from the header and the data is returned
        """

    pass

    def query(self) -> str:
        """
            The status of the query buffer, generally divided into, is empty or full |
            with a persistent license
        """

    pass

    def persist(self, path: str) -> bool:
        """
            To persist all buffer data, you need to provide all the storage methods
        """

    pass

    def get(self, index: int | str) -> bytes | None:
        """
            More dictionaries or indexes fetch objects into buffers
        """

    pass

    def persist_put(self, index: int | str, path: str) -> bool:
        """
            Persist individual buffer objects based on dictionaries or indexes
        """

    pass

    def BufferSpace(self, index: int) -> None:
        """
            Manually changing the buffer space at a later stage cannot be smaller
            than the current space
        """

    pass

    def GetBufferSpace(self) -> int:
        """
            Gets the space used by the current buffer
        """

    pass

    def QueryBufferSpace(self) -> int | None:
        """
            Query the remaining buffer space, expressed as the maximum space used in infinite mode
        """

    pass

    def clearBuffered(self) -> None:
        """
            Empty all queues for the buffer
        """

    pass

    def clearIndex(self) -> None:
        """
            Empty all index for the buffer
        """

    pass

    def ExportData(self) -> list[bytes] | None:
        """
            Export all bytes of data
        """

    pass

    def ClearExportData(self) -> list[bytes] | None:
        """
            Export all bytes of data and clear all data
        """

    pass

    def ReentrancyMode(self, mode: int, accessibility: int = -1) -> None:
        """
            [Please refer to it BOUNDLESS|LIMITED]
        """
    pass

    def __Del(self, target: dict | list, key: str) -> None:
        """
            :param target: target dict
            :param key: index key
            :return: None
            The intrinsic function is mainly used as a delete
        """
    pass

    def opencv(self):
        """
        Gets a view object that summarizes the buffer
        :return:Gets a view object that summarizes the buffer
        """
        return self.__repr__()
    pass


pass
