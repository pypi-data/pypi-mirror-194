from devoud.browser import *
from devoud.browser.pages.abstract_page import AbstractPage


class BrowserTabWidget(QTabWidget):
    count_changed = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName('tab_widget')
        self.maximum_tabs = 150
        self.setTabBar(self.TabBar(self))
        self.setTabsClosable(True)
        self.setElideMode(Qt.ElideRight)
        self.tabCloseRequested.connect(self.close_tab)
        self.tabBar().mousePressSignal.connect(self.close_tab)
        self.currentChanged.connect(self.tab_changed)

        # кнопка создания новой вкладки
        self.add_tab_button = QPushButton(self)
        self.add_tab_button.setObjectName('add_tab_button')
        self.add_tab_button.setFixedSize(40, 40)
        self.add_tab_button.setIconSize(QSize(25, 19))
        self.add_tab_button.setToolTip('Создать новую вкладку (Ctrl + T)')
        self.add_tab_button.clicked.connect(lambda: self.create_tab(self.window().settings.get('newPage')['site']))
        self.setCornerWidget(self.add_tab_button, Qt.Corner.TopLeftCorner)

        self.count_changed.connect(self.toggle_tab_bar)

    def toggle_tab_bar(self):
        if self.count() == 1:
            self.tabBar().hide()
            self.window().add_tab_button.show()
            self.window().address_panel.setFixedHeight(45)
            self.add_tab_button.hide()
        elif self.count() == 2:
            self.window().add_tab_button.hide()
            if self.window().settings.get('TabBarPosition') == 'Снизу':
                self.window().address_panel.setFixedHeight(45)
            else:
                self.window().address_panel.setFixedHeight(40)
            self.add_tab_button.show()
            self.tabBar().show()

    def set_tab_bar_position(self, position=None):
        if position is None:
            position = self.window().settings.get('TabBarPosition')
        if position == 'Сверху':
            self.setTabPosition(QTabWidget.North)
            self.add_tab_button.setStyleSheet('#add_tab_button {margin-bottom: 8px;}')
            self.window().address_panel.setFixedHeight(40)
        else:
            self.window().address_panel.setFixedHeight(45)
            self.setTabPosition(QTabWidget.South)
            self.add_tab_button.setStyleSheet('#add_tab_button {margin-top: 8px;}')

    def create_tab(self, url=None, title=None, page_history: list = None, page_history_position=-1, save_page_history=True, switch=True, end=True, load=True):
        if self.count() >= self.maximum_tabs:
            print('[Вкладки]: Достигнуто максимальное количество вкладок')
            self.add_tab_button.setDisabled(True)
            return False
        else:
            self.add_tab_button.setDisabled(False)
        if url is None and load is True:
            url = self.window().settings.get('newPage')['site']
        if title is None:
            title = url
        page = AbstractPage(self, url=url, title=title,
                            page_history=page_history, page_history_position=page_history_position,
                            save_page_history=save_page_history)
        if end:
            self.addTab(page, page.title)
        else:
            self.insertTab(self.currentIndex()+1, page, page.title)
        index = self.indexOf(page)
        if switch:
            self.setCurrentIndex(index)
        elif load:
            page.load(url)
        self.setTabToolTip(index, page.title)
        self.window().session.add_page(page)
        self.tabBar().findChild(QAbstractButton).setToolTip('Закрыть вкладку (Ctrl + W)')
        self.count_changed.emit()
        return page.view  # для запросов на новую вкладку

    @Slot()
    def tab_changed(self):
        page = self.current()
        if page is not None:
            if page.view is None:
                page.load()
            self.window().address_line_edit.setText(self.current().url)
            self.window().address_line_edit.setCursorPosition(0)
            self.window().address_line_edit.clearFocus()
            self.window().set_title(self.current().title)
            self.window().address_panel.show_update_button(not self.current().is_loading())
            self.window().address_panel.update_bookmark_button(self.current().url)
            self.window().address_panel.update_navigation_buttons()

    def close_tab(self, index):
        page = self.widget(index)
        if self.count() <= 1:  # если одна вкладка, то открывать сайт с заставкой
            page.load(self.window().settings.get('newPage')['site'])
            return
        if page.view is not None:
            page.view.deleteLater()
        page.deleteLater()
        self.window().session.remove_page(page)
        self.removeTab(index)
        self.count_changed.emit()

    def current(self) -> AbstractPage:
        return self.currentWidget()

    class TabBar(QTabBar):
        mousePressSignal = Signal(int)

        def __init__(self, parent):
            super().__init__(parent)
            self.setMovable(True)

        def mousePressEvent(self, event):
            if event.button() == Qt.LeftButton:
                super().mousePressEvent(event)
            elif event.button() == Qt.MiddleButton:
                position = self.tabAt(event.position().toPoint())
                self.mousePressSignal.emit(position)
