from devoud.browser import *
from devoud.browser.widgets.container import ContainerWidget


class ContainerListWidget(ContainerWidget):
    def __init__(self, parent, title):
        super().__init__(parent, title)
        self.clean_button = QPushButton(self, icon=QIcon('custom:clean(container_title_btn).svg'), text='Очистить всё')
        self.clean_button.setFixedSize(120, 22)
        self.clean_button.setObjectName('container_title_button')
        self.clean_button.clicked.connect(self.remove_all)
        self.title_layout.addWidget(self.clean_button)

        self.clean_select_button = QPushButton(self, text='Удалить выбранное')
        self.clean_select_button.setFixedSize(140, 22)
        self.clean_select_button.setObjectName('container_title_button')
        self.clean_select_button.setHidden(True)
        self.clean_select_button.clicked.connect(self.remove_current)
        self.title_layout.addWidget(self.clean_select_button)

        self.list = QListWidget(self)
        self.list.itemClicked.connect(lambda: self.clean_select_button.setHidden(False))
        self.list.itemDoubleClicked.connect(self.open_item)
        self.content_layout.addWidget(self.list)

        self.empty_info_label = QLabel()
        self.empty_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(self.empty_info_label, 0, 0)
        self.list.model().rowsInserted.connect(self.show_empty_list_info)
        self.list.model().rowsRemoved.connect(self.show_empty_list_info)

        self.update_all()

    def show_empty_list_info(self):
        ...

    def update_all(self):
        self.list.clear()
        self.show_empty_list_info()
        ...

    def add(self):
        ...

    def remove(self):
        ...

    def remove_all(self):
        if QMessageBox.question(self, 'Подтверждение операции', 'Очистить список?') == QMessageBox.Yes:
            self.list.clear()
            self.show_empty_list_info()
            return True

    def remove_current(self):
        ...

    def open_item(self):
        ...
