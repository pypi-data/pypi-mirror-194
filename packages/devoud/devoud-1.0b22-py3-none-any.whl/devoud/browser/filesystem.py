from devoud.browser import *
from devoud.browser.settings import Settings
from devoud.browser.history import History
from devoud.browser.bookmarks import Bookmarks
from devoud.browser.session import Session
from devoud.browser.download_manager import DownloadManager


class FileSystem:
    def __init__(self):
        print('[Файлы]: Инициализация файловой системы')
        self.__root = Path(__file__).parents[1]
        self.__local_user_dir = Path(self.__root, 'user')
        print(f'[Файлы]: Текущая операционная система {platform}')
        self.__user_dir = {'linux': Path(f'{Path.home()}/.local/share/devoud/user'),
                           'darwin': Path(f'{Path.home()}/Library/Application Support'),
                           'win32': Path(f'{Path.home()}/AppData/Roaming/devoud/user')}.get(platform,
                                                                                            self.__local_user_dir)
        print(f'[Файлы]: Рабочий каталог ({Path.cwd()})')
        self.check_program_files()

        # добавить ссылки для ресурсов
        QtCore.QDir.addSearchPath('custom', f'{self.user_dir()}/generated_icons')
        QtCore.QDir.addSearchPath('icons', rpath('ui/icons'))

    def root(self):
        """Возвращает директорию программы"""
        return self.__root

    def user_dir(self):
        """Возвращает путь до каталога с пользовательскими данными"""
        return self.__user_dir

    def check_program_files(self):
        """Проверяет необходимые файлы для работы программы"""
        print(f'[Файлы]: Проверка необходимых файлов')
        if not Path.exists(self.user_dir()):
            print('[Файлы]: Каталог для пользовательских данных не найден, идёт его создание')
            Path.mkdir(self.user_dir(), parents=True, exist_ok=True)
            self.create_launch_shortcut()
        print(f'[Файлы]: Пользовательские данные лежат в ({self.user_dir()})')

        for directory in ('generated_icons', 'web_profile', 'cache'):
            Path(self.user_dir(), directory).mkdir(parents=True, exist_ok=True)

        for user_file in (
                Settings.filename, History.filename, Bookmarks.filename, Session.filename, DownloadManager.filename):
            if not Path.exists(Path(self.user_dir(), user_file)):
                print(f'[Файлы]: Создается отсутствующий файл {user_file}')
                Path(self.user_dir(), user_file).touch()

    @staticmethod
    def create_launch_shortcut():
        """Создает ярлык запуска программы в системе"""
        root = Path(__file__).parents[1]
        icon = {'win32': f'{root}/ui/icons/devoud.ico',
                'darwin': f'{root}/ui/icons/devoud.svg',
                'linux': f'{root}/ui/icons/devoud.svg'}
        make_shortcut(f'{root}/Devoud.py', name='Devoud',
                      description='A simple web browser written in Python using PySide6',
                      icon=icon[platform],
                      terminal=False, desktop=False)
        print(f'[Файлы]: Ярлык для запуска браузера был создан')

    @staticmethod
    def open_in_file_manager(path):
        """Открывает путь через системный файловый менеджер"""
        command = {'win32': ["explorer", path],
                   'darwin': ["open", path],
                   'linux': ["xdg-open", path]}
        subprocess.Popen(command.get(platform, ["xdg-open", path]))

    @staticmethod
    def human_bytes(B):
        """Return the given bytes as a human friendly KB, MB, GB, or TB string."""
        B = float(B)
        KB = float(1024)
        MB = float(KB ** 2)  # 1,048,576
        GB = float(KB ** 3)  # 1,073,741,824
        TB = float(KB ** 4)  # 1,099,511,627,776

        if B < KB:
            return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
        elif KB <= B < MB:
            return '{0:.2f} KB'.format(B / KB)
        elif MB <= B < GB:
            return '{0:.2f} MB'.format(B / MB)
        elif GB <= B < TB:
            return '{0:.2f} GB'.format(B / GB)
        elif TB <= B:
            return '{0:.2f} TB'.format(B / TB)
