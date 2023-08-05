import os
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings

BASEPATH = Path(os.path.dirname(os.path.realpath(__file__))).parent


class CoreSettings(BaseSettings):
    INDEX_PATH: Optional[Path] = BASEPATH / "index.db"


class S3Settings(BaseSettings):
    ENDPOINT_URL: str = "https://storage.yandexcloud.net"
    BUCKET_NAME: str = "talkkeeper"
    ACCESS_KEY: str
    SECRET_KEY: str


settings = CoreSettings()
