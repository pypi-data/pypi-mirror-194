# Based on https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PySide6
from devoud.browser.utils import *


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("title_bar")

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(6)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self)
        self.label.setObjectName("title_bar_label")
        self.layout.addWidget(self.label)

        self.window_buttons_widget = QWidget(self)
        self.window_buttons_widget.setFixedWidth(80)
        self.window_buttons_widget.setObjectName("title_bar_buttons")
        self.window_buttons_layout = QHBoxLayout(self.window_buttons_widget)
        self.window_buttons_layout.setContentsMargins(0, 5, 0, 0)

        self.minimize_button = QPushButton(self)
        self.minimize_button.setObjectName("minimize_button")
        self.minimize_button.setFixedSize(QSize(23, 23))
        self.minimize_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.minimize_button.setFlat(True)
        self.minimize_button.clicked.connect(self.window().showMinimized)
        self.window_buttons_layout.addWidget(self.minimize_button)

        self.maximize_button = QPushButton(self)
        self.maximize_button.setObjectName("maximize_button")
        self.maximize_button.setFixedSize(QSize(23, 23))
        self.maximize_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.maximize_button.setFlat(True)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.window_buttons_layout.addWidget(self.maximize_button)

        self.close_button = QPushButton(self)
        self.close_button.setObjectName("close_button")
        self.close_button.setFixedSize(QSize(23, 23))
        self.close_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_button.setFlat(True)
        self.close_button.clicked.connect(self.window().close)
        self.window_buttons_layout.addWidget(self.close_button)

        self.right_spacer = QSpacerItem(11, 10)

        self.layout.addWidget(self.window_buttons_widget)
        self.layout.addItem(self.right_spacer)

        self.window().installEventFilter(self)

    def mouseDoubleClickEvent(self, event):
        self.toggle_maximize()

    def mouseMoveEvent(self, event):
        move_window(self.window(), event.globalPos())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            move_window(self.window(), event.globalPos())

    def toggle_maximize(self):
        self.window().showNormal() if self.window().isMaximized() else self.window().showMaximized()
