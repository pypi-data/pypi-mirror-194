from devoud.browser import *


class DownloadItem(QObject):
    def __init__(self, request: QWebEngineDownloadRequest = None):
        super().__init__()
        self.request = request
        if request is not None:
            self.name = request.downloadFileName()
            self.size = request.totalBytes()
            self.request.totalBytesChanged.connect(self.update_size)
            self.source = request.url().toString()
            self.location = str(Path(request.downloadDirectory(), request.downloadFileName()))
            self.date = datetime.now().strftime("%d/%m/%Y(%H-%M)")

    def update_size(self):
        self.size = self.request.totalBytes()


class ListSignals(QObject):
    add = Signal(DownloadItem)
    delete = Signal(DownloadItem)


class DownloadList(list):
    def __init__(self, manager, *args):
        super().__init__(*args)
        self.manager = manager
        self._proxy = ListSignals()
        self.add = self._proxy.add
        self.delete = self._proxy.delete

    def append(self, item):
        item.request.isFinishedChanged.connect(lambda: self.manager.download_finished(item))
        item.request.accept()
        super().append(item)
        self.add.emit(item)
        print(
            f'[Загрузки]: Файл ({item.request.downloadFileName()})[{item.request.downloadDirectory()}] добавлен в очередь для загрузки')

    def remove(self, item):
        try:
            super().remove(item)
        except ValueError:
            pass
        if item.request is not None:
            item.request.cancel()
            self.delete.emit(item)


class DownloadHistoryProxy(QObject):
    delete = Signal(str)


class DownloadManager(QObject):
    filename = 'downloads.json'

    def __init__(self, browser):
        super().__init__(browser)
        self.browser = browser
        self._download_list = DownloadList(self)
        self._history = self.read_history()
        self._proxy = DownloadHistoryProxy()
        self.history_item_delete = self._proxy.delete

    def list(self) -> DownloadList:
        return self._download_list

    def history(self):
        return self._history

    def save_download_history(self):
        if not self.parent().private_mode:
            with Path(self.browser.FS.user_dir(), self.filename).open('w') as file:
                history_dict = {}
                for item in self.history():
                    history_dict[item.name] = {'size': item.size,
                                               'date': item.date,
                                               'source': item.source,
                                               'location': item.location}
                json.dump(history_dict, file, indent=4, ensure_ascii=False)

    def read_history(self, dictionary=False):
        with Path(self.browser.FS.user_dir(), self.filename).open() as downloads_history_file:
            try:
                downloads_history_dict = json.load(downloads_history_file)
                if not dictionary:
                    downloads_history_list = []
                    for name, info in downloads_history_dict.items():
                        item = DownloadItem()
                        item.name = name
                        item.size = info.get('size', -1)
                        item.date = info.get('date', '01/01/2000(00-00)')
                        item.source = info.get('source', 'Отсутствует')
                        item.location = info.get('location', '')
                        downloads_history_list.append(item)
                    return downloads_history_list
                else:
                    return downloads_history_dict
            except json.decoder.JSONDecodeError:
                return {} if dictionary else []

    def download_requested(self, request: QWebEngineDownloadRequest):
        DownloadMethod.Method(self.parent(), request)
        DownloadMethod.Method = DownloadMethod.Default

    @Slot(DownloadItem)
    def download_finished(self, item):
        print(
            f'[Загрузки]: Файл ({item.request.downloadFileName()})[{item.request.downloadDirectory()}] был загружен')
        state = item.request.state()
        item.request = None
        if state == QWebEngineDownloadRequest.DownloadState.DownloadCompleted:
            notification.notify(
                title='Файл загружен',
                message=item.location,
                app_name='Devoud',
            )
            self._history.append(item)
            self.save_download_history()
        elif state == QWebEngineDownloadRequest.DownloadState.DownloadInterrupted:
            notification.notify(
                title='Ошибка загрузки файла',
                message=item.location,
                app_name='Devoud',
            )
        else:
            notification.notify(
                title='Загрузка файла отменена',
                message=item.location,
                app_name='Devoud',
            )
        self.list().remove(item)


class DownloadMessageBox(QMessageBox):
    def __init__(self, parent, request: QWebEngineDownloadRequest):
        super().__init__(parent)
        self.setWindowTitle('Сохранить в загрузках?')
        self.request = request
        self.setIcon(QMessageBox.Icon.Question)
        self.setText(request.downloadFileName())

        self.save_button = self.addButton('Сохранить', QMessageBox.ButtonRole.YesRole)
        self.save_button.clicked.connect(self.save)

        self.select_button = self.addButton('Выбрать место', QMessageBox.ButtonRole.YesRole)
        self.select_button.clicked.connect(self.select)

        self.cancel_button = self.addButton('Отменить', QMessageBox.ButtonRole.NoRole)
        self.cancel_button.clicked.connect(self.cancel)

        self.exec()

    def save(self):
        download_item = DownloadItem(self.request)
        self.parent().download_manager.list().append(download_item)

    def select(self):
        DownloadMethod.SaveAs(self.parent(), self.request)

    def cancel(self):
        self.request.cancel()
        print('[Загрузки]: Загрузка файла отменена')


class DownloadMethod(QObject):
    @classmethod
    def Default(cls, parent, request: QWebEngineDownloadRequest):
        DownloadMessageBox(parent, request)

    @classmethod
    def SaveAs(cls, parent, request: QWebEngineDownloadRequest):
        path = Path(QFileDialog.getSaveFileName(parent, 'Сохранить файл как', request.downloadFileName())[0])

        if str(path) != '.':
            request.setDownloadFileName(path.name)
            request.setDownloadDirectory(str(path.parent))
            download_item = DownloadItem(request)
            parent.download_manager.list().append(download_item)
        else:
            request.cancel()
            print('[Загрузки]: Загрузка файла отменена')

    Method = Default
