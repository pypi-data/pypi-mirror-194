import multiprocessing
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

    @classmethod
    @property
    def queue(cls):
        ctx = mp.get_context("tk_scan")
        if not ctx:
            mp.set_start_method("tk_scan")
            return mp.Queue()
        else:
            return ctx.Queue()

    @classmethod
    def read(cls, path, pool=None):
        for position in path.iterdir():
            if position.is_file():
                cls(position).scan(single=not bool(pool))

            elif position.is_dir():
                if pool:
                    pool.apply_async(
                        cls(position.absolute()).read, (path,), {"pool": pool}
                    )
                else:
                    cls(position).scan(single=True)

    @ignore_exception(PermissionError)
    def scan(self, single=False):
        if not self.path:
            return

        elif self.path.is_file():
            if single:
                self.push(self.path)
            else:
                self.queue.put(self.path)
            return

        if self.path.is_dir():
            if single:
                self.read(self.path)
            else:
                with mp.Pool(multiprocessing.cpu_count()) as p:
                    self.read(self.path, pool=p)
                    p.close()
                    p.join()

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
