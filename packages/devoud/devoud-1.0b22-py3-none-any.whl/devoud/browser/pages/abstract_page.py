from devoud.browser.pages import *
from devoud.browser.web.view import BrowserWebView


class AbstractPage(QWidget):
    def __init__(self, parent, url=None, title=None, page_history=None, page_history_position=-1,
                 save_page_history=True):
        super().__init__(parent)
        self.setObjectName('abstract_page')
        self.tab_widget = parent
        self.FS = self.window().FS
        self.settings = self.window().settings
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.layout().addWidget(self.progress_bar, 0, 0)

        self.view_spliter = QSplitter(Qt.Vertical)
        self.layout().addWidget(self.view_spliter, 1, 0)
        self.popup_link = None

        self.url = url
        self.title = title
        self.view = None

        if page_history is None:
            page_history = []
        self.page_history = page_history
        self.page_history_position = page_history_position
        self.save_page_history = save_page_history

    def data(self) -> dict:
        return {'url': self.url,
                'title': self.title,
                'type': url_type(self.url)}

    def create_web_view(self):
        if self.view is not None:
            self.view.deleteLater()
        self.view = BrowserWebView(self)
        self.view.titleChanged.connect(self.update_title)
        self.view.page().urlChanged.connect(self.url_changed)
        self.view.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.view.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.view.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, self.settings.get('javascript'))
        if self.settings.get('adblock'):
            self.view.page().profile().setUrlRequestInterceptor(self.window().interceptor)
        if not self.settings.get('cookies'):
            self.view.page().profile().setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        self.view.page().profile().downloadRequested.connect(lambda req: self.window().download_manager.download_requested(req))
        self.view.setAttribute(Qt.WA_DeleteOnClose)
        self.view.loadStarted.connect(self.loadStartedHandler)
        self.view.loadProgress.connect(self.loadProgressHandler)
        self.view.loadFinished.connect(self.loadFinishedHandler)
        self.view_spliter.addWidget(self.view)
        self.popup_link = self.PopupLink(self)
        self.view.page().linkHovered.connect(self.popup_link.show_link)

    def create_embedded_view(self, url='devoud://void'):
        print(f'[Страница]: Открытие встроенной страницы ({url})')
        if self.view is not None:
            self.view.deleteLater()
        self.view = embedded_pages.get(url, NotFoundPage)(self)
        self.add_to_page_history(url)
        self.update_title(self.view.title)
        self.save_page_history = True
        self.window().history.append(self.data())
        self.view.setAttribute(Qt.WA_DeleteOnClose)  # ?
        self.view_spliter.addWidget(self.view)

    def load(self, url: str = None, allow_search=False):
        if url is None:
            if self.url is not None:
                url = self.url
            else:
                url = VoidPage.url

        url = redirects.get(url, url)  # если редирект не найден, то значение остается
        self.url = url

        if is_url(url):
            # если это ссылка, то блокируем поиск
            allow_search = False

        formatted_url = QUrl.fromUserInput(url).toString()
        if url_type(url) is BrowserWebView:
            self.create_web_view()
            if allow_search:
                # при разрешении вставляем текст в поисковый движок
                self.save_page_history = True
                self.view.load(f'{self.window().current_search_engine()["query"]}{url}')
            else:
                self.view.load(formatted_url)
        else:
            self.create_embedded_view(url)
        self.update_title(self.view.title)
        self.window().address_panel.update_navigation_buttons()

    def add_to_page_history(self, url):
        if self.save_page_history:
            if self.page_history_position != len(self.page_history)-1:
                del self.page_history[self.page_history_position+1:]
            self.page_history_position += 1
            self.page_history.append(url)
        self.window().address_panel.update_navigation_buttons()

    def stop(self):
        self.view.stop()

    def reload(self):
        self.save_page_history = False
        self.view.reload()
        self.url_changed(self.url)

    def back(self):
        self.save_page_history = False
        self.page_history_position -= 1
        self.load(self.page_history[self.page_history_position])

    def forward(self):
        self.save_page_history = False
        self.page_history_position += 1
        self.load(self.page_history[self.page_history_position])

    def can_back(self):
        return len(self.page_history) > 1 and self.page_history_position != 0

    def can_forward(self):
        return len(self.page_history) > 1 and self.page_history_position != len(self.page_history) - 1

    @Slot(str)
    def url_changed(self, url):
        if isinstance(url, QUrl):
            url = url.toString()
        self.url = url
        if self.tab_widget.currentWidget() == self:
            self.window().address_line_edit.setText(url)
            self.window().address_line_edit.setCursorPosition(0)
            self.window().address_panel.update_bookmark_button(url)
        self.add_to_page_history(url)

    @Slot(str)
    def update_title(self, title=None):
        if title is not None:
            self.title = title
        index = self.tab_widget.indexOf(self)
        self.tab_widget.setTabText(index, self.title)
        self.tab_widget.setTabToolTip(index, self.title)
        if self.tab_widget.currentIndex() == index:
            self.window().set_title(self.title)

    def is_loading(self):
        return False if self.view is None else self.view.is_loading()

    @Slot()
    def loadStartedHandler(self):
        if self.isVisible():
            self.window().address_panel.show_update_button(False)
        print(f"[Страница]: Начата загрузка страницы ({self.url})")

    @Slot(int)
    def loadProgressHandler(self, progress):
        if self.isVisible():
            self.window().address_panel.show_update_button(False)
        self.progress_bar.setValue(progress)
        print(f"[Страница]: {progress}% ({self.url})")

    @Slot()
    def loadFinishedHandler(self):
        self.save_page_history = True
        self.window().history.append(self.data())
        if self.isVisible():
            self.window().address_panel.show_update_button(True)
        self.progress_bar.setValue(0)
        print(f"[Страница]: Страница загружена ({self.url})")

    class PopupLink(QLabel):
        def __init__(self, parent):
            super().__init__(parent)
            self.setObjectName('popup_link')
            self.setMinimumWidth(0)
            self.setMaximumWidth(16777215)
            self.parent().layout().addWidget(self, 1, 0, 1, 2, Qt.AlignLeft | Qt.AlignBottom)
            self._left_align = True

        @Slot(str)
        def show_link(self, url):
            self.setText(url)
            self.setHidden(url == '')

        def enterEvent(self, event):
            if self._left_align:
                self.parent().layout().addWidget(self, 1, 0, 1, 2, Qt.AlignRight | Qt.AlignBottom)
                self._left_align = False
                self.setStyleSheet('border-top-right-radius: 0px; border-top-left-radius: 6px')
            else:
                self.parent().layout().addWidget(self, 1, 0, 1, 2, Qt.AlignLeft | Qt.AlignBottom)
                self._left_align = True
                self.setStyleSheet('border-top-right-radius: 6px; border-top-left-radius: 0px')
