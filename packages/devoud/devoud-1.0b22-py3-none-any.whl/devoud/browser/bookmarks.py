from devoud.browser import *


class Bookmarks(QObject):
    filename = 'bookmarks.json'
    changed = Signal(str, str)
    add = Signal(str, str)
    remove = Signal(str, str)

    def __init__(self, parent):
        super().__init__(parent)
        self._dict = {}
        if not parent.private_mode:
            with Path(self.parent().FS.user_dir(), self.filename).open() as bookmarks_file:
                try:
                    self._dict = json.load(bookmarks_file)
                except json.decoder.JSONDecodeError:
                    print(f'[Закладки]: Произошла ошибка при чтении {self.filename}, ошибка: {json.decoder.JSONDecodeError}')
                    self.remove_all()

    def dict(self) -> dict:
        return self._dict

    def exist(self, url: str) -> bool:
        return url in self._dict

    def append(self, data: dict) -> None:
        """{'url': 'ссылка',
        'title': 'заголовок'}"""
        url = data['url']
        title = data.get('title', 'Без названия')
        if self.exist(url):
            self.remove_(url)
        else:
            self._dict[url] = {'title': title}
            print(f'[Закладки]: Добавлена закладка ({url})')
            self.add.emit(url, title)
        if not self.parent().private_mode:
            with Path(self.parent().FS.user_dir(), self.filename).open('w') as bookmarks_file:
                json.dump(self._dict, bookmarks_file, indent=4, ensure_ascii=False)
        self.changed.emit(url, title)

    def remove_(self, url: str) -> None:
        with Path(self.parent().FS.user_dir(), self.filename).open('w') as bookmarks_file:
            title = self._dict[url]['title']
            del self._dict[url]
            print(f'[Закладки]: Удалена закладка ({url})')
            if not self.parent().private_mode:
                json.dump(self._dict, bookmarks_file, indent=4, ensure_ascii=False)
            self.remove.emit(url, title)
            self.changed.emit(url, title)

    def remove_all(self) -> None:
        self._dict = {}
        with Path(self.parent().FS.user_dir(), self.filename).open('w') as bookmarks_file:
            json.dump(self._dict, bookmarks_file, indent=4, ensure_ascii=False)
        print(f'[Закладки]: Все закладки удалены')
