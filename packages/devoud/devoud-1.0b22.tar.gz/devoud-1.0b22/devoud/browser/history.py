from devoud.browser import *


class History(QObject):
    filename = 'history.csv'
    changed = Signal(list)
    add = Signal(str, str, str)
    remove = Signal(list)

    def __init__(self, parent):
        super().__init__(parent)
        self._list = []
        if parent.settings.get('saveHistory') and not parent.private_mode:
            with Path(self.parent().FS.user_dir(), self.filename).open(newline='') as history_file:
                try:
                    self._list = list(csv.reader(history_file))
                except Exception as read_error:
                    print(f'[История]: Произошла ошибка при чтении {self.filename}, ошибка: {read_error}')
                    self.remove_all()
                self._list.reverse()

    def list(self) -> list:
        return self._list

    def exist(self, url: str) -> bool:
        return url in self._list

    def append(self, data: dict) -> None:
        if self.parent().settings.get('saveHistory'):
            data = [data['title'], data['url'], datetime.now().strftime("%d-%m-%Y %H:%M")]
            self._list.insert(0, data)
            self.add.emit(data[0], data[1], data[2])
            self.changed.emit(data[0])
            with Path(self.parent().FS.user_dir(), self.filename).open('a', newline='') as history_file:
                writer = csv.writer(history_file)
                writer.writerow(data)

    def remove_(self, rows: list) -> None:
        """Список строк для удаления: [0, 1, 2...]"""
        with Path(self.parent().FS.user_dir(), self.filename).open('w', newline='') as history_file:
            for row in rows:
                del self._list[row]
            writer = csv.writer(history_file)
            writer.writerows(self._list[::-1])
            self.remove.emit(rows)
            self.changed.emit(rows)

    def remove_all(self) -> None:
        with Path(self.parent().FS.user_dir(), self.filename).open('w', newline='') as history_file:
            rows = [i for i in range(len(self._list))]
            self._list = []
            print(f'[История]: История очищена')
            self.remove.emit(rows)
            self.changed.emit(rows)
            history_file.write('')
