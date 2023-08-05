import datetime
from pathlib import Path
from typing import Optional

import typer

from talkkeeper.packages.index import Index
from talkkeeper.packages.uploader import Uploader

app = typer.Typer()


@app.command()
def scan(path: Optional[Path] = typer.Option(None), single: bool = typer.Option(False)):
    start_time = datetime.datetime.now()
    source_count = len(Index())
    try:
        Uploader(path or Path(".")).scan(single=single)
    finally:
        result_count = len(Index())
        timer = datetime.datetime.now() - start_time
        print(
            f"===\nКоличество файлов в индексе: {result_count}\nЗагружено: {result_count - source_count}\nВремя работы: {timer}"
        )


if __name__ == "__main__":
    app()
