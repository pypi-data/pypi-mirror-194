import hashlib
import io
import sqlite3


class Talkkeeper:
    ACCEPTED_FORMATS = [".wav", ".webm"]

    def __init__(self, source):
        if source.suffix not in Talkkeeper.ACCEPTED_FORMATS:
            raise UnacceptedFormat(source)
        self.source = source
        self._content = None

    @property
    def content(self):
        if not self._content:
            if not self.source.exists():
                raise ReadError(self.source)
            self._content = io.BytesIO(open(self.source, "rb").read()).getvalue()
        return self._content

    @property
    def buffer(self):
        return io.BufferedReader(io.BytesIO(self.content))

    @property
    def md5(self):
        return hashlib.md5(self.buffer.read()).hexdigest()

    def __hash__(self):
        return hash(self.md5)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.md5 == other.md5
        return NotImplemented

    @property
    def map(self):
        # Получение индекса файла
        ...

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return self.md5

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.source.resolve()}"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.source.resolve()}"


class BaseTKException(Exception):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f"{self.__class__.__name__}: {self.path}"


class UnacceptedFormat(BaseTKException):
    ...


class ReadError(BaseTKException):
    ...
