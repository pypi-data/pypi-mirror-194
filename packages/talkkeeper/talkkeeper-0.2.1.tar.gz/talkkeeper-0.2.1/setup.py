# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['talkkeeper',
 'talkkeeper.cli',
 'talkkeeper.core',
 'talkkeeper.handlers',
 'talkkeeper.packages']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.69,<2.0.0',
 'orjson>=3.8.3,<4.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'tinytag>=1.8.1,<2.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['tk = talkkeeper:application']}

setup_kwargs = {
    'name': 'talkkeeper',
    'version': '0.2.1',
    'description': 'Библиотека Python talkkeeper для загрузки в хранилище / предобработки / разметки / ...',
    'long_description': '# Обработчик Media файлов\n\nЗадача: Обработать звук, разложить его на объекты и положить в систему так, чтобы над данными можно было выполнять операции\n\n## Интерфейс Talkkeeper\n-[] Получение meta информации\n-[x] Вычисление хеша\n-[] Базовая аналитика над объектом\n-[] Хранение метрик клиента\n-[] Разбиение объекта на блоки\n-[] Создание карты объекта\n-[] Поддержка интерфейса talkkeeper server\n-[] Поддержка чтения \n-[x] Обход файлов системы\n-[] Загрузка индекса файлов в бд\n  -[] Схема данных в базе\n  -[] Создание таблиц и базы при первом запуске',
    'author': 'Nikolay Baryshnikov',
    'author_email': 'root@k0d.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/p141592',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
