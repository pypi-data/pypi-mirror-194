import multiprocessing as mp

from talkkeeper import talkkeeper as tk
from talkkeeper.packages.index import Index


class Uploader:
    def __init__(self, path):
        self.path = path
        self.index = Index()

    def ignore_exception(exceptions):
        def wrap(func):
            def _wrap(self, *args, **kwargs):
                try:
                    return func(self, *args, **kwargs)
                except exceptions:
                    ...

            return _wrap

        return wrap

    def read(self, path):
        for position in path.iterdir():
            if position.is_file():
                self.push(position.absolute())

            elif position.is_dir():
                self.read(position.absolute())

    @ignore_exception(PermissionError)
    def scan(self, single=True):
        if not self.path:
            return

        elif self.path.is_file():
            self.push(self.path)

        if self.path.is_dir():
            return self.read(self.path)

            # with mp.Pool(mp.cpu_count()) as p:
            #     self.read(self.path, pool=p)
            #     p.close()
            #     p.join()

    @ignore_exception(tk.UnacceptedFormat)
    def push(self, path):
        _tk = tk.Talkkeeper(path)
        self.index.push(_tk)
        print(_tk)

    @property
    def cursor(self):
        # Токен загрузки
        ...

    def upload(self):
        # Отправить мета информацию, создать/получить курсор загрузки
        # Отправка блоков в загрузку по поличеству ядер - 1
        ...
