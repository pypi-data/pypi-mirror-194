import devoud
from devoud.browser.download_manager import *
from devoud.browser.embedded.view import EmbeddedView
from devoud.browser.web.search_engines import search_engines
from devoud.browser.widgets.container import ContainerWidget
from devoud.browser.widgets.container_list_widget import ContainerListWidget
from devoud.browser.widgets.line_edit import LineEdit


class ControlPage(EmbeddedView):
    title = 'Панель управления'
    url = 'devoud://control'
    section_tags = {'devoud://control#settings': 0,
                    'devoud://control#history': 1,
                    'devoud://control#bookmarks': 2,
                    'devoud://control#downloads': 3}

    def __init__(self, parent):
        super().__init__(parent)
        self.FS = parent.window().FS
        self.settings = parent.settings
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 5)
        self.main_layout.setSpacing(0)

        self.sections_panel = self.SectionsPanel(self)

        self.stacked_widget = QStackedWidget(self)  # всё что справа от панели вкладок
        self.stacked_widget.setObjectName('stacked_widget')
        self.sections_panel.setCurrentRow(self.section_tags.get(self.parent.url, 0))
        self.sections_panel.currentRowChanged.connect(self.section_changed)
        self.main_layout.addWidget(self.stacked_widget)

        self.settings_section = self.Section(self.stacked_widget, 'custom:settings.svg')
        self.history_section = self.Section(self.stacked_widget, 'custom:history.svg')
        self.bookmarks_section = self.Section(self.stacked_widget, 'custom:bookmark_empty(sections).svg')
        self.downloads_section = self.Section(self.stacked_widget, 'custom:downloads.svg')

        # Виджет "О программе"
        self.about_widget = ContainerWidget(self, 'О программе')
        self.settings_section.add_widget(self.about_widget)
        self.browser_icon = QLabel(self.about_widget)
        self.browser_icon.setPixmap(QPixmap('icons:devoud.svg'))
        self.browser_icon.mousePressEvent = lambda e: self.browser_icon.setPixmap(QPixmap('icons:warning.svg'))
        self.browser_icon.setFixedSize(QSize(85, 85))
        self.browser_icon.setScaledContents(True)
        self.about_widget.content_layout.addWidget(self.browser_icon, 0, 0)
        self.about_widget.content_layout.addWidget(QLabel(self.about_widget,
                                                          text=f'{devoud.__name__} {devoud.__version__} '
                                                               f'({"Pyinstaller" if IS_PYINSTALLER else "PyPi"})'
                                                               f'\nРазработал OneEyedDancer\nс '
                                                               f'использованием PySide6 под лицензией GPL3'), 0, 1)
        self.create_shortcut_button = QPushButton(self.about_widget, text='Создать ярлык')
        self.create_shortcut_button.setFixedSize(110, 22)
        self.create_shortcut_button.setObjectName('container_title_button')
        self.create_shortcut_button.clicked.connect(self.create_shortcut)
        self.about_widget.title_layout.addWidget(self.create_shortcut_button)
        self.project_site_button = QPushButton(self.about_widget, text='Страница проекта')
        self.project_site_button.setFixedSize(130, 22)
        self.project_site_button.setObjectName('container_title_button')
        self.project_site_button.clicked.connect(
            lambda: self.window().tab_widget.create_tab('https://codeberg.org/OneEyedDancer/Devoud', end=False))
        self.about_widget.title_layout.addWidget(self.project_site_button)

        # Виджет настроек
        self.settings_widget = ContainerWidget(self, 'Настройки')
        self.user_dir_button = QPushButton(self.settings_widget, icon=QIcon('custom:folder.svg'))
        self.user_dir_button.setFixedSize(30, 22)
        self.user_dir_button.setObjectName('container_title_button')
        self.user_dir_button.setToolTip('Открыть каталог с пользовательскими данными')
        self.user_dir_button.clicked.connect(lambda: self.window().FS.open_in_file_manager(self.window().FS.user_dir()))
        self.settings_widget.title_layout.addWidget(self.user_dir_button)
        self.settings_section.add_widget(self.settings_widget)

        # Кнопка перезапуска
        self.restart_button = QPushButton(self.settings_widget, icon=QIcon('custom:restart.svg'), text='Перезапустить')
        self.restart_button.setFixedSize(140, 22)
        self.restart_button.setObjectName('container_title_button')
        self.restart_button.setToolTip('Для применения настроек требуется перезапуск')
        self.restart_button.setHidden(True)
        self.restart_button.clicked.connect(self.window().restart)
        self.settings_widget.title_layout.addWidget(self.restart_button)

        self.history_checkbox = self.SettingsCheckBox(parent=self,
                                                      text='Сохранять историю',
                                                      option='saveHistory',
                                                      command=self.history_checkbox_command,
                                                      command_exec='before',
                                                      tooltip='При выключении удаляет историю',
                                                      block=self.window().private_mode)
        self.settings_widget.content_layout.addWidget(self.history_checkbox, 0, 0)
        self.restore_tabs_checkbox = self.SettingsCheckBox(parent=self,
                                                           text='Восстанавливать вкладки',
                                                           option='restoreSession',
                                                           tooltip='Восстанавливает последнюю сессию браузера',
                                                           block=self.window().private_mode)
        self.settings_widget.content_layout.addWidget(self.restore_tabs_checkbox, 1, 0)
        self.adblock_checkbox = self.SettingsCheckBox(parent=self,
                                                      text='Блокировщик рекламы',
                                                      option='adblock',
                                                      restart=True)
        self.settings_widget.content_layout.addWidget(self.adblock_checkbox, 2, 0)
        self.cookie_checkbox = self.SettingsCheckBox(parent=self,
                                                     text='Хранить Cookie',
                                                     option='cookies',
                                                     tooltip='При отключении Cookie-файлы больше не будут храниться на диске',
                                                     command=self.cookie_checkbox_command,
                                                     command_exec='before',
                                                     restart=True,
                                                     block=self.window().private_mode)
        self.settings_widget.content_layout.addWidget(self.cookie_checkbox, 3, 0)
        self.javascript_checkbox = self.SettingsCheckBox(parent=self,
                                                         text='JavaScript',
                                                         option='javascript',
                                                         restart=True)
        self.settings_widget.content_layout.addWidget(self.javascript_checkbox, 4, 0)
        self.systemframe_checkbox = self.SettingsCheckBox(parent=self,
                                                          text='Системная рамка окна',
                                                          option='systemWindowFrame',
                                                          restart=True)
        self.settings_widget.content_layout.addWidget(self.systemframe_checkbox, 5, 0)

        self.home_lineedit = LineEdit(self)
        self.home_lineedit.setFixedSize(QSize(215, 24))
        self.home_lineedit.setFocusPolicy(Qt.ClickFocus)
        self.home_lineedit.textEdited.connect(lambda: self.settings.set('homePage', self.home_lineedit.text()))
        self.home_lineedit.setText(self.settings.get('homePage'))
        self.settings_widget.content_layout.addWidget(self.home_lineedit, 6, 0)
        self.settings_widget.content_layout.addWidget(QLabel(self.settings_widget, text='Домашняя страница'), 6, 1)

        self.new_page_box = QComboBox(self.settings_widget)
        [self.new_page_box.addItem(title) for title in ['Заставка с часами', 'Поисковик', 'Домашняя страница']]
        self.new_page_box.setFixedSize(QSize(215, 24))
        self.new_page_box.setFocusPolicy(Qt.ClickFocus)
        self.new_page_box.setCurrentText(self.settings.get('newPage')['title'])
        self.new_page_box.currentIndexChanged.connect(self.change_new_page)
        self.settings_widget.content_layout.addWidget(self.new_page_box, 7, 0)
        self.settings_widget.content_layout.addWidget(QLabel("Новая страница"), 7, 1)

        self.search_box = QComboBox(self.settings_widget)
        [self.search_box.addItem(QIcon(search_engines[title]['icon']), title) for title in search_engines.keys()]
        self.search_box.setFixedSize(QSize(215, 24))
        self.search_box.setFocusPolicy(Qt.ClickFocus)
        self.search_box.setCurrentText(self.settings.get('searchEngine'))
        self.search_box.currentIndexChanged.connect(self.change_default_search)
        self.settings_widget.content_layout.addWidget(self.search_box, 8, 0)
        self.settings_widget.content_layout.addWidget(QLabel('Поисковая система по умолчанию'), 8, 1)

        self.tab_bar_position_box = QComboBox(self.settings_widget)
        self.tab_bar_position_box.addItem('Снизу')
        self.tab_bar_position_box.addItem('Сверху')
        self.tab_bar_position_box.setCurrentText(self.settings.get('TabBarPosition'))
        self.tab_bar_position_box.setFixedSize(QSize(215, 24))
        self.tab_bar_position_box.setFocusPolicy(Qt.ClickFocus)
        self.settings_widget.content_layout.addWidget(self.tab_bar_position_box, 9, 0)
        self.tab_bar_position_box.currentIndexChanged.connect(
            lambda: self.change_tab_bar_position(self.tab_bar_position_box.currentText()))
        self.settings_widget.content_layout.addWidget(QLabel("Положение панели вкладок"), 9, 1)

        # Виджет тем
        self.themes_widget = ContainerWidget(self, 'Темы')
        self.settings_section.add_widget(self.themes_widget)
        self.themes_buttons_list = []
        self.create_themes_buttons()
        self.themes_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.themes_widget.content_layout.addItem(self.themes_spacer, 0, 5)

        # Settings section spacer
        self.settings_section.add_spacer(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # История и закладки
        self.history_list = self.HistoryListWidget(self)
        self.history_section.add_widget(self.history_list)
        self.window().history.add.connect(self.history_list.add)
        self.window().history.remove.connect(self.history_list.remove)
        self.bookmarks_list = self.BookmarksListWidget(self)
        self.bookmarks_section.add_widget(self.bookmarks_list)
        self.window().bookmarks.add.connect(self.bookmarks_list.add)
        self.window().bookmarks.remove.connect(self.bookmarks_list.remove)

        # Загрузки
        self.downloads_widget = ContainerWidget(self, 'Загрузки')
        self.downloads_widget_list = QWidget(self)
        self.downloads_widget_list.setLayout(QVBoxLayout())
        self.downloads_widget_list.layout().setContentsMargins(0, 0, 0, 0)
        self.downloads_widget.content_layout.addWidget(self.downloads_widget_list)
        self.downloads_widget.content_layout.setSpacing(0)
        self.downloads_section.add_widget(self.downloads_widget)
        self.downloads_widget.content_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.remove_all_downloads_button = QPushButton(self.downloads_widget,
                                                       icon=QIcon('custom:clean(container_title_btn).svg'),
                                                       text='Очистить всё')
        self.remove_all_downloads_button.setFixedSize(120, 22)
        self.remove_all_downloads_button.setObjectName('container_title_button')
        self.remove_all_downloads_button.clicked.connect(self.remove_all_download_item_widgets)
        self.downloads_widget.title_layout.addWidget(self.remove_all_downloads_button)
        downloads_history = self.window().download_manager.history()
        downloads = self.window().download_manager.list()
        for item in downloads + downloads_history:
            self.add_download_item_widget(item)
        self.window().download_manager.list().add.connect(self.add_download_item_widget)
        self.window().download_manager.history_item_delete.connect(self.remove_download_item_widget)
        self.sections_panel.setCurrentRow(self.section_tags.get(self.parent.url, 0))

    def deleteLater(self) -> None:
        self.window().download_manager.list().add.disconnect(self.add_download_item_widget)
        self.window().download_manager.history_item_delete.disconnect(self.remove_download_item_widget)
        self.window().history.add.disconnect(self.history_list.add)
        self.window().history.remove.disconnect(self.history_list.remove)
        self.window().bookmarks.add.disconnect(self.bookmarks_list.add)
        self.window().bookmarks.remove.disconnect(self.bookmarks_list.remove)
        super().deleteLater()

    @Slot(DownloadItem)
    def add_download_item_widget(self, item):
        downloads_item = self.DownloadsItemWidget(self, item)
        self.downloads_widget_list.layout().addWidget(downloads_item)

    @Slot(str)
    def remove_download_item_widget(self, name):
        for widget in self.downloads_widget_list.findChildren(self.DownloadsItemWidget):
            if widget.name == name:
                return widget.deleteLater()

    def remove_all_download_item_widgets(self):
        if QMessageBox.question(self.parent, 'Подтверждение операции',
                                'Очистить список загруженных файлов?') == QMessageBox.Yes:
            for widget in self.downloads_widget_list.findChildren(self.DownloadsItemWidget):
                widget.deleteLater()

    @Slot(int)
    def section_changed(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.parent.url = {value: key for key, value in self.section_tags.items()}.get(index, 0)
        self.window().address_line_edit.setText(self.parent.url)
        self.window().address_line_edit.setCursorPosition(0)
        self.window().address_panel.update_bookmark_button(self.parent.url)

    def create_themes_buttons(self):
        for path, dirs, files in os.walk(rpath("ui/themes")):
            for count, filename in enumerate(files):
                with open(f"{path}/{filename}", 'r') as theme_file:
                    data = json.load(theme_file)
                    btn = QPushButton(self)
                    btn.setFixedSize(20, 20)
                    btn.setObjectName(filename.rpartition('.')[0])
                    btn.setStyleSheet(f"""
                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                            stop:0 {data['tab_widget']['select_bg']}, 
                            stop:1 {data['tab_widget']['bg']});
                            border-radius: 10px;
                            border: 0;""")
                    btn.clicked.connect(self.apply_theme)
                    self.themes_buttons_list.append(btn)
                    self.themes_widget.content_layout.addWidget(btn, 0, count)

        self.set_select_icon(self.settings.get('theme'))

    def set_select_icon(self, select_theme=None):
        if select_theme is None:
            select_theme = self.FS.default_settings['theme']
        for button in self.themes_buttons_list:
            if button.objectName() == select_theme:
                button.setIcon(QIcon('custom:select.svg'))
            else:
                button.setIcon(QIcon('custom:void.png'))

    def apply_theme(self):
        selected_theme = self.sender().objectName()
        self.settings.set('theme', selected_theme)
        self.window().change_style()
        self.set_select_icon(selected_theme)
        self.window().session.update_control_pages()
        print('[Стили]: Применена тема', selected_theme)

    def change_default_search(self):
        current = self.search_box.currentText()
        self.settings.set('searchEngine', current)
        self.window().address_panel.search_box.setCurrentText(self.settings.get('searchEngine'))
        if self.settings.get('newPage')['title'] == 'Поисковик':
            self.settings.set('newPage', {'title': 'Поисковик', 'site': search_engines[current]['site']})

    def change_new_page(self):
        new_page_dict = {'Заставка с часами': 'https://web.tabliss.io/',
                         'Поисковик': search_engines[self.settings.get('searchEngine')]['site'],
                         'Домашняя страница': self.settings.get('homePage')}
        title = self.new_page_box.currentText()
        self.settings.set('newPage', {'title': title, 'site': new_page_dict[title]})

    def change_tab_bar_position(self, position):
        self.settings.set('TabBarPosition', position)
        self.window().tab_widget.set_tab_bar_position(position)

    def create_shortcut(self):
        if QMessageBox.question(self.parent, 'Подтверждение операции',
                                'Пересоздать ярлык запуска программы в системе?') == QMessageBox.Yes:
            self.FS.create_launch_shortcut()

    def history_checkbox_command(self):
        if self.history_checkbox.isChecked():
            if QMessageBox.question(self.parent, 'Подтверждение операции',
                                    'Это действие удалит всю вашу историю. Продолжить?') == QMessageBox.Yes:
                self.window().history.remove_all()
                self.history_list.list.clear()
                self.history_list.empty_info_label.setText('История отключена в настройках')
                self.history_list.empty_info_label.show()
                return True
            else:
                return False
        self.history_list.empty_info_label.setText('Список истории пуст')
        self.history_list.empty_info_label.show()
        return True

    def cookie_checkbox_command(self):
        if self.cookie_checkbox.isChecked():
            if QMessageBox.question(self.parent, 'Подтверждение операции',
                                    'Это действие удалит все текущие Cookie-файлы. Продолжить?') == QMessageBox.Yes:
                self.window().profile.cookieStore().deleteAllCookies()
                print('[Веб-Профиль]: Все cookie удалены')
                return True
            else:
                return False
        return True

    class SectionsPanel(QListWidget):
        def __init__(self, parent):
            super().__init__(parent)
            self.setObjectName('sections_panel')
            self.setIconSize(QSize(25, 25))
            self.setFrameShape(QListWidget.NoFrame)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            parent.layout().addWidget(self)

        def add(self, icon):
            item = QListWidgetItem(icon, "", self)
            item.setSizeHint(QSize(16777215, 40))

    class Section(QWidget):
        def __init__(self, parent, icon: str):
            super().__init__(parent)
            self.setLayout(QVBoxLayout())
            self.layout().setContentsMargins(10, 0, 10, 0)

            self.scroll_area = QScrollArea(self)
            self.layout().addWidget(self.scroll_area)
            self.scroll_area.setWidgetResizable(True)
            self.scroll_content = QWidget()
            self.scroll_content_layout = QVBoxLayout()
            self.scroll_content_layout.setContentsMargins(0, 0, 0, 0)
            self.scroll_content.setLayout(self.scroll_content_layout)
            self.scroll_area.setWidget(self.scroll_content)

            parent.layout().addWidget(self)

            self.icon = QIcon(icon)
            parent.parent().sections_panel.add(self.icon)

        def add_widget(self, widget):
            self.scroll_content_layout.addWidget(widget)

        def add_spacer(self, spacer):
            self.scroll_content_layout.addItem(spacer)

    class DownloadsItemWidget(QWidget):
        # FIXME: Исправить удаление
        def __init__(self, parent, item: DownloadItem):
            super().__init__(parent)
            self.parent = parent
            self.window = parent.window()
            self.item = item
            self.name = item.name
            self.size = item.size
            self.date = item.date
            self.source = item.source
            self.location = item.location
            self.request = item.request
            if self.item.request is not None:
                self.request.isFinishedChanged.connect(self.download_finished)
                self.request.receivedBytesChanged.connect(self.update_bar)
                self.request.totalBytesChanged.connect(self.update_info)

            self.setObjectName('downloads_item')
            self.setLayout(QVBoxLayout())
            self.layout().setContentsMargins(0, 0, 0, 0)

            self.widget = QWidget(self)
            self.layout().addWidget(self.widget)
            self.widget.setLayout(QVBoxLayout())
            self.widget.layout().setSpacing(0)

            self.name_label = QLabel(self.name)
            self.name_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.name_label.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred))
            self.widget.layout().addWidget(self.name_label)

            self.info_widget = QWidget(self.widget)
            self.info_widget.setObjectName('downloads_item_info')
            self.info_widget.setLayout(QHBoxLayout())
            self.widget.layout().addWidget(self.info_widget)
            self.info_widget.layout().setContentsMargins(0, 4, 0, 4)

            self.info_label = QLabel(
                f'Размер: {self.window.FS.human_bytes(self.size)}\nДата: {self.date}\nИсточник: {self.source}')
            self.info_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.info_label.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred))
            self.info_widget.layout().addWidget(self.info_label)

            self.actions_widget = QWidget(self.widget)
            self.actions_widget.setObjectName('downloads_item_actions')
            self.actions_widget.setLayout(QHBoxLayout())
            self.widget.layout().addWidget(self.actions_widget)
            self.actions_widget.layout().setContentsMargins(0, 0, 0, 0)

            self.open_file_button = QPushButton(self.actions_widget)
            self.open_file_button.clicked.connect(
                lambda: self.window.FS.open_in_file_manager(Path(self.location).parent))
            self.open_file_button.setFixedWidth(25)
            self.open_file_button.setObjectName('downloads_item_open')
            self.actions_widget.layout().addWidget(self.open_file_button)

            self.delete_item_button = QPushButton(self.actions_widget)
            self.delete_item_button.clicked.connect(self.deleteLater)
            self.delete_item_button.setFixedWidth(25)
            self.delete_item_button.setObjectName('downloads_item_delete')
            self.delete_item_button.setToolTip('Удаляется только элемент списка, а не сам файл')
            self.actions_widget.layout().addWidget(self.delete_item_button)

            self.state_label = QLabel('Загружен')
            self.actions_widget.layout().addWidget(self.state_label)

            if self.item.request is not None:
                self.progress_bar = QProgressBar(self)
                self.progress_bar.setValue(0)
                self.progress_bar.setFixedHeight(23)
                self.actions_widget.layout().addWidget(self.progress_bar)
                self.state_label.hide()

        def deleteLater(self):
            if self.item.request is not None:
                self.window.download_manager.list().remove(self.item)
            else:
                self.window.download_manager.history().remove(self.item)
            self.window.download_manager.history_item_delete.emit(self.name)
            self.window.download_manager.save_download_history()
            super().deleteLater()

        def update_bar(self):
            if self.size > 0:
                percent = int(self.request.receivedBytes() * 100 / self.size)
                self.progress_bar.setValue(percent)

        def update_info(self):
            self.size = self.request.totalBytes()
            self.info_label.setText(
                f'Размер: {self.window.FS.human_bytes(self.size)}\nДата: {self.date}\nИсточник: {self.source}')

        def download_finished(self):
            self.item.request = None
            self.progress_bar.hide()
            self.state_label.setText('Загружен')
            self.state_label.show()

    class SettingsCheckBox(QCheckBox):
        def __init__(self, parent, text, option, command=None, command_exec='after', restart: bool = False,
                     tooltip=None, block=False):
            super().__init__(parent)
            self.setText(text)
            self.setMinimumSize(QSize(0, 25))
            self.setChecked(parent.settings.get(option))
            self.parent = parent
            self.option = option
            self.restart = restart
            self.command = command
            self.command_exec = command_exec
            self.clicked.connect(self.checked)
            self.setDisabled(block)
            if tooltip is not None:
                self.setToolTip(tooltip)

        def checked(self):
            if self.command is not None:
                if self.command_exec == 'after':
                    self.parent.settings.set(self.option)
                    self.setChecked(self.parent.settings.get(self.option))
                    if self.restart:
                        self.parent.restart_button.show()
                    self.command()
                else:
                    self.setChecked(self.parent.settings.get(self.option))
                    if self.command():
                        self.parent.settings.set(self.option)
                        self.setChecked(self.parent.settings.get(self.option))
                        if self.restart:
                            self.parent.restart_button.show()
            else:
                self.parent.settings.set(self.option)
                self.setChecked(self.parent.settings.get(self.option))
                if self.restart:
                    self.parent.restart_button.show()

    class BookmarksListWidget(ContainerListWidget):
        def __init__(self, parent, title='Закладки'):
            super().__init__(parent, title)

        def show_empty_list_info(self):
            if self.list.count() == 0:
                text = 'Нет сохраненных закладок'
                self.empty_info_label.show()
            else:
                text = ''
                self.empty_info_label.hide()
            self.empty_info_label.setText(text)

        def update_all(self):
            super().update_all()
            self.list.addItems(
                [f'{data["title"]} [{url}]' for url, data in self.window().bookmarks.dict().items()][::-1])

        @Slot(str, str)
        def add(self, url, title):
            self.list.insertItem(0, QListWidgetItem(f'{title} [{url}]'))

        @Slot(str, str)
        def remove(self, url, title):
            self.list.takeItem(self.list.row(self.list.findItems(f'{title} [{url}]', Qt.MatchContains)[0]))

        def remove_all(self):
            if super().remove_all():
                self.window().bookmarks.remove_all()
                self.window().address_panel.update_bookmark_button('')

        def remove_current(self):
            self.window().bookmarks.remove.disconnect(self.remove)
            self.window().bookmarks.remove_(self.list.currentItem().text().split("[")[-1].split("]")[0])
            self.window().bookmarks.remove.connect(self.remove)
            self.list.takeItem(self.list.currentRow())

        def open_item(self):
            url = self.list.currentItem().text().split("[")[-1].split("]")[0]
            self.window().tab_widget.create_tab(url, end=False)

    class HistoryListWidget(ContainerListWidget):
        def __init__(self, parent, title='История'):
            super().__init__(parent, title)

        def show_empty_list_info(self):
            if self.window().private_mode:
                text = 'Включен приватный режим'
                self.empty_info_label.show()
            elif not self.window().settings.get('saveHistory'):
                text = 'История отключена в настройках'
                self.empty_info_label.show()
            elif self.list.count() == 0:
                text = 'Список истории пуст'
                self.empty_info_label.show()
            else:
                text = ''
                self.empty_info_label.hide()
            self.empty_info_label.setText(text)

        def update_all(self):
            super().update_all()
            self.list.addItems([f"{item[2]}     {item[0]} [{item[1]}]" for item in self.window().history.list()])
            self.show_empty_list_info()

        @Slot(str, str, str)
        def add(self, title, url, time):
            self.list.insertItem(0, QListWidgetItem(f'{time}     {title} [{url}]'))

        @Slot(list)
        def remove(self, rows):
            for row in rows:
                self.list.takeItem(row)

        def remove_all(self):
            if super().remove_all():
                self.window().history.remove.disconnect(self.remove)
                self.window().history.remove_all()
                self.window().history.remove.connect(self.remove)

        def remove_current(self):
            self.window().history.remove.disconnect(self.remove)
            self.window().history.remove_([self.list.currentRow()])
            self.window().history.remove.connect(self.remove)
            self.list.takeItem(self.list.currentRow())

        def open_item(self):
            url = self.list.currentItem().text().split("[")[-1].split("]")[0]
            self.window().tab_widget.create_tab(url, end=False)
