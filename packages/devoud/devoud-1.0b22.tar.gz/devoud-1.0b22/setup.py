# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devoud',
 'devoud.browser',
 'devoud.browser.embedded',
 'devoud.browser.pages',
 'devoud.browser.styles',
 'devoud.browser.utils',
 'devoud.browser.web',
 'devoud.browser.web.adblocker',
 'devoud.browser.widgets',
 'devoud.browser.widgets.title_bar']

package_data = \
{'': ['*'],
 'devoud': ['ui/fonts/*', 'ui/icons/*', 'ui/themes/*'],
 'devoud.browser.web.adblocker': ['rules/*']}

install_requires = \
['PySide6==6.4.2',
 'braveblock==0.5.0',
 'plyer==2.1.0',
 'pyshortcuts==1.8.3',
 'requests==2.28.2']

entry_points = \
{'console_scripts': ['devoud = devoud.Devoud:main']}

setup_kwargs = {
    'name': 'devoud',
    'version': '1.0b22',
    'description': 'A simple web browser written in Python using PySide6',
    'long_description': '<h1 align="center">Devoud</h1>\n\n![Скриншот](./screenshot.png)\n![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)\n![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)\n![Arch](https://img.shields.io/badge/Arch%20Linux-1793D1?logo=arch-linux&logoColor=fff&style=for-the-badge)\n![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white)\n![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)\n![Fedora](https://img.shields.io/badge/Fedora-294172?style=for-the-badge&logo=fedora&logoColor=white)\n## О проекте 🎧\nДанный браузер является более легковесным решением в сравнение с другими известными графически-ориентированными аналогами. Не требует повышенных прав для установки. Проект следует своим принципам и идеям при разработке. А также полностью открыт и свободно распространяемый, поэтому каждый может перестроить его под свои нужды. Основывается на движке QtWebEngine, с использованием библиотеки PySide6\n## Установка браузера 💿\n### Требования\n* Для работы программы, требуется установленный [Python](https://www.python.org/), и его пакетный менеджер pip (pip идет вместе с Python, но во время установки Python поставьте галочку "Add Python 3.x to PATH")\n### Установка через pip (рекомендуется)\n* Введите в терминале(cmd, powershell, bash) ```pip install devoud```\n* После установки, запустите его через команду ```devoud```, он произведет начальную настройку, и создаст ярлык запуска в системе\n### Из исходников (другой способ установки)\n* Скачайте архив с этой страницы\n* Распакуйте в любом месте\n* Установите зависимости из файла ```./devoud/requirements.txt```\n* Запустите start.py\n## Обновление 🔧\n* На данный момент обновление доступно через команду ```devoud update```\n## Сборка пакета через [поэзию](https://python-poetry.org/) 📜 (для разработчиков)\n* ```poetry build```\n## Вопросы ❓\n* О всех найденных ошибках и предложениях по улучшению программы сообщайте во вкладке [Задачи](https://codeberg.org/OneEyedDancer/Devoud/issues)\n* Случайно удалили ярлык? Запустите ```devoud shortcut```\n* Все доступные команды для браузера можно узнать через ```devoud help```\n* Будут ли доступны расширения из других браузеров? Пока что маловероятно\n* Как помочь проекту? Вы можете предложить свой вариант решение какой-либо проблемы через [Задачи](https://codeberg.org/OneEyedDancer/Devoud/issues)\n* Могу ли я модифицировать эту программу и выпускать под своим названием? Да, можно, но с соблюдением требований лицензии\n* Передаются ли мои данные? Автор гарантирует, что с его стороны все ваши данные хранятся только на вашем компьютере. Но помните, что мы живем в проклятом мире, а этот браузер основывается на двжике QtWebEngine, а значит этим могут заниматься Qt и Google \n## Лицензия 🄯\n[![GPLv3](https://www.gnu.org/graphics/gplv3-with-text-136x68.png)](https://www.gnu.org/licenses/gpl-3.0)\n',
    'author': 'OneEyedDancer',
    'author_email': 'ooeyd@ya.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/OneEyedDancer/Devoud',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
