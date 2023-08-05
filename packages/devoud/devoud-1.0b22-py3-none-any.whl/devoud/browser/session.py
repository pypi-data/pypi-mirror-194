from devoud.browser import *
from devoud.browser.pages.abstract_page import AbstractPage
from devoud.browser.pages.control_page import ControlPage


class Session:
    filename = 'session.json'

    def __init__(self, parent):
        self.parent = parent
        self.FS = parent.FS
        self._dict = {}
        self._objects = []
        if self.parent.settings.get('restoreSession') and not self.parent.private_mode:
            with Path(self.FS.user_dir(), self.filename).open() as session_file:
                try:
                    self._dict = json.load(session_file)
                except Exception as error:
                    print(
                        f'[Вкладки]: Произошла ошибка при чтении {self.filename}, ошибка: {error}')
                    self.restore_file()

    def session(self) -> dict:
        return self._dict

    def use(self, session: dict):
        if session is not None:
            self._dict = session

    def objects_list(self) -> list:
        return self._objects

    def urls(self) -> list:
        return list(map(lambda page: page.url, self._objects))

    def add_page(self, page: AbstractPage):
        self._objects.append(page)

    def remove_page(self, page: AbstractPage):
        self._objects.remove(page)

    def clear_objects(self):
        for page in self._objects:
            if page.view is not None:
                page.view.deleteLater()
            page.deleteLater()
        self._objects.clear()

    def update_control_pages(self):
        for page in self._objects:
            if isinstance(page.view, ControlPage):
                page.reload()

    def restore(self):
        if self._dict:
            try:
                self.parent.tab_widget.currentChanged.disconnect()
                for key, data in self._dict.items():
                    if key.isdigit():
                        self.parent.tab_widget.create_tab(url=data['url'],
                                                          title=data['title'],
                                                          page_history=data['pages'],
                                                          page_history_position=data['pages_position'],
                                                          save_page_history=False,
                                                          switch=False,
                                                          load=False)
                self.parent.tab_widget.setCurrentIndex(self._dict['lastPage'])
                self.parent.tab_widget.current().load()
                self.parent.tab_widget.currentChanged.connect(self.parent.tab_widget.tab_changed)
                print('[Вкладки]: Предыдущая сессия восстановлена')
            except Exception as error:
                print(f'[Вкладки]: Не удалось восстановить прошлую сессию, ошибка {error}')
                self.parent.load_home_page()
        else:
            self.parent.load_home_page()

    def save(self):
        if self.parent.settings.get('restoreSession') and not self.parent.private_mode:
            self._dict = {}
            for tab_index in range(self.parent.tab_widget.count()):
                page = self.parent.tab_widget.widget(tab_index)
                self._dict[str(tab_index)] = {
                    'url': page.url,
                    'title': page.title,
                    'pages': page.page_history,
                    'pages_position': page.page_history_position
                }
            self._dict['lastPage'] = self.parent.tab_widget.currentIndex()
            with Path(self.parent.FS.user_dir(), self.filename).open('w') as session_file:
                try:
                    json.dump(self._dict, session_file, sort_keys=True, indent=4, ensure_ascii=False)
                except Exception as error:
                    print(f'[Вкладки]: Произошла ошибка при записи данных в {self.filename}, ошибка {error}')
                else:
                    return print('[Вкладки]: Текущая сессия сохранена')
        print('[Вкладки]: Текущая сессия не сохранена')

    def restore_file(self):
        print('[Вкладки]: Идёт восстановление файла сессии')
        self._dict = {}
        with Path(self.FS.user_dir(), self.filename).open('w') as session_file:
            json.dump(self._dict, session_file, indent=4, ensure_ascii=False)
