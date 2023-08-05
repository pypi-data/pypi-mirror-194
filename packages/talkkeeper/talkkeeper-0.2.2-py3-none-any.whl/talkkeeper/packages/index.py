import datetime
import sqlite3
import sys
from pathlib import Path

from pydantic.dataclasses import dataclass

from talkkeeper.core.settings import settings


class Index:
    TABLE = "_index"
    # Файловая система
    # Метаинформация файлов
    # Информация о загрузках

    def __init__(self):
        self._connect = None

    @property
    def index(self):
        return self.fetch_index()

    @property
    def connect(self):
        if not self._connect:
            self._connect = sqlite3.connect(
                settings.INDEX_PATH,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                isolation_level="",
            )
            self._connect.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE}{IndexField.schema()}"
            )
        return self._connect

    def __getitem__(self, tk):
        return self.index[tk.md5]

    def __contains__(self, tk):
        return bool(self[tk])

    def __len__(self):
        return self.count

    def __enter__(self):
        return self

    def __exit__(self):
        self.connect.close()
        self._connect = None

    def fetch_index(self):
        # Информация о всех файлах в базе
        with self.connect:
            res = self.connect.execute(f"SELECT * FROM {self.TABLE}")
            data = res.fetchall()
        return data

    def push(self, tk):
        with self.connect:
            self.connect.execute(
                f"INSERT OR REPLACE INTO {self.TABLE} VALUES (:path, :md5, :created_at)",
                (
                    {
                        "path": str(tk.source.absolute().resolve()),
                        "md5": tk.md5,
                        "created_at": datetime.datetime.now(),
                    }
                ),
            )

    def get_md5(self, tk):
        with self.connect:
            res = self.connect.execute(
                f"SELECT md5 FROM {self.TABLE} WHERE path = ?", (str(tk.source),)
            )
            res = res.fetchone()
            return res[0] if res else None

    @property
    def count(self):
        with self.connect:
            res = self.connect.execute(f"SELECT count(path) FROM {self.TABLE}")
            res = res.fetchone()
            return res[0] if res else None

    def update(self, *args, **kwargs):
        ...

    def remove(self, tk):
        with self.connect:
            self.connect.execute(
                f"DELETE FROM {self.TABLE} WHERE path = ?", (str(tk.source),)
            )


@dataclass
class IndexField:
    md5: str
    path: Path
    format: str
    name: str
    size: int
    date: datetime.datetime

    @classmethod
    def table_params(cls):
        return """(
            path TEXT primary key,
            md5 TEXT,
            created_at timestamp
        )"""

    @classmethod
    def schema(cls):
        return "(path, md5, created_at)"


def debug(unraisable):
    print(f"{unraisable.exc_value!r} in callback {unraisable.object.__name__}")
    print(f"Error message: {unraisable.err_msg}")


sqlite3.enable_callback_tracebacks(True)
sys.unraisablehook = debug
sqlite3.register_converter(
    "date", lambda val: datetime.date.fromisoformat(val.decode())
)
sqlite3.register_converter(
    "datetime", lambda val: datetime.datetime.fromisoformat(val.decode())
)
sqlite3.register_converter(
    "timestamp", lambda val: datetime.datetime.fromtimestamp(int(val))
)
sqlite3.register_converter("Path", lambda val: Path(val.decode()))
sqlite3.register_adapter(datetime.date, lambda val: val.isoformat())
sqlite3.register_adapter(datetime.datetime, lambda val: val.isoformat())
sqlite3.register_adapter(datetime.datetime, lambda val: int(val.timestamp()))
sqlite3.register_adapter(Path, lambda val: str(val.resolve()))
