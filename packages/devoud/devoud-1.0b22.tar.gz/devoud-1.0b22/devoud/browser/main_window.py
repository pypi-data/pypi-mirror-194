from devoud.browser.styles.theme import Theme
from devoud.browser.web.adblocker.ad_blocker import AdBlocker, RequestInterceptor
from devoud.browser.web.search_engines import search_engines
from devoud.browser.widgets.address_panel import AddressPanel
from devoud.browser.filesystem import FileSystem
from devoud.browser.widgets.find_on_page import FindWidget
from devoud.browser.download_manager import DownloadManager
from devoud.browser.widgets.tab_widget import BrowserTabWidget
from devoud.browser.widgets.title_bar import CustomTitleBar
from devoud.browser.widgets.size_grip import SizeGrip
from devoud.browser.utils import *
from devoud.browser.settings import Settings
from devoud.browser.bookmarks import Bookmarks
from devoud.browser.history import History
from devoud.browser.session import Session
import devoud


class BrowserWindow(QMainWindow):
    def __init__(self, private_mode: bool = False, session=None, settings: dict = None):
        super().__init__()
        self.private_mode = private_mode
        self.FS = FileSystem()
        self.settings = Settings(self)
        self.settings.use(settings)
        self.session = Session(self)
        self.session.use(session)
        self.history = History(self)
        self.bookmarks = Bookmarks(self)
        self.download_manager = DownloadManager(self)
        self.theme = Theme(self)

        self.setWindowIcon(QIcon(self.theme.app_icons.get(platform, 'icons:devoud.png')))
        self.setWindowTitle(__name__)
        self.setMinimumSize(QSize(400, 300))
        size = self.screen().availableGeometry()
        self.resize(size.width() * 2 / 3, size.height() * 2 / 3)

        # профиль для веб-страниц
        self.profile = None
        if not private_mode:
            self.profile = QWebEngineProfile('DevoudProfile')
            self.profile.setCachePath(f'{self.FS.user_dir()}/cache')
            self.profile.setPersistentStoragePath(f'{self.FS.user_dir()}/web_profile')
        else:
            print(f'[{devoud.__name__}]: Включен приватный режим, настройки не сохраняются')
            self.settings.set('saveHistory', False)
            self.settings.set('restoreSession', False)
            self.settings.set('cookies', False)

        # блокировщик рекламы
        self.ad_blocker = AdBlocker(self)
        if self.ad_blocker.is_enable():
            self.ad_blocker.add_rules()
            self.interceptor = RequestInterceptor(self.ad_blocker.rules)

        # шрифт
        QFontDatabase.addApplicationFont(rpath('ui/fonts/ClearSans-Medium.ttf'))
        self.setFont(QFont('Clear Sans Medium'))

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.window_layout = QGridLayout(self.central_widget)
        self.window_layout.setSpacing(0)
        self.window_layout.setContentsMargins(0, 0, 0, 0)

        # всё кроме size grip
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName('main_frame')

        # тени для окна с кастомной рамкой ломают рендер веб-страниц
        # self.window_shadow = QGraphicsDropShadowEffect(self)
        # self.window_shadow.setBlurRadius(17)
        # self.window_shadow.setXOffset(0)
        # self.window_shadow.setYOffset(0)
        # self.window_shadow.setColor(QColor(0, 0, 0, 150))
        # self.main_frame.setGraphicsEffect(self.window_shadow)

        self.window_layout.addWidget(self.main_frame, 1, 1)
        self.main_layout = QGridLayout(self.main_frame)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # выбор рамки окна
        self.title_bar = None
        if not self.settings.get('systemWindowFrame'):
            self.title_bar = CustomTitleBar(self)
            self.main_layout.addWidget(self.title_bar, 0, 0)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.enable_rounded_corners()

            # для растяжения окна с кастомной рамкой
            if platform != 'win32':
                self.window_layout.addWidget(SizeGrip(side='right'), 1, 2)
                self.window_layout.addWidget(SizeGrip(side='left'), 1, 0)
                self.window_layout.addWidget(SizeGrip(side='top'), 0, 1)
                self.window_layout.addWidget(SizeGrip(side='bottom'), 2, 1)
                self.window_layout.addWidget(SizeGrip(side='top-right'), 0, 2)
                self.window_layout.addWidget(SizeGrip(side='top-left'), 0, 0)
                self.window_layout.addWidget(SizeGrip(side='bottom-right'), 2, 2)
                self.window_layout.addWidget(SizeGrip(side='bottom-left'), 2, 0)
            else:
                self.nativeEvent = self.native_event

            self.changeEvent = self.change_event

        # адресная панель
        self.address_panel = AddressPanel(self)
        self.main_layout.addWidget(self.address_panel, 1, 0, 1, 1)
        self.address_line_edit = self.address_panel.address_line_edit
        self.add_tab_button = self.address_panel.add_tab_button

        # виджет вкладок
        self.main_layout.addWidget(self.tab_widget, 3, 0)
        self.tab_widget.set_tab_bar_position()

        # комбинации клавиш
        QShortcut(QKeySequence("Ctrl+Q"), self).activated.connect(self.close)
        QShortcut(QKeySequence("F5"), self).activated.connect(self.update_page)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self.show_find_on_page)
        QShortcut(QKeySequence("Alt+H"), self).activated.connect(lambda: self.load_home_page(new_tab=False))
        QShortcut(QKeySequence("Ctrl+T"), self).activated.connect(
            lambda: self.tab_widget.create_tab(self.settings.get('newPage')['site']))
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(
            lambda: self.bookmarks.append(self.tab_widget.current().data()))
        QShortcut(QKeySequence("Ctrl+Shift+O"), self).activated.connect(
            lambda: self.tab_widget.create_tab('devoud://control#bookmarks'))
        QShortcut(QKeySequence("Ctrl+H"), self).activated.connect(
            lambda: self.tab_widget.create_tab('devoud://control#history'))
        QShortcut(QKeySequence("Ctrl+J"), self).activated.connect(
            lambda: self.tab_widget.create_tab('devoud://control#downloads'))
        QShortcut(QKeySequence("Ctrl+W"), self).activated.connect(
            lambda: self.tab_widget.close_tab(self.tab_widget.currentIndex()))
        QShortcut(QKeySequence("Alt+Left"), self).activated.connect(self.back_page)
        QShortcut(QKeySequence("Alt+Right"), self).activated.connect(self.forward_page)

        self.session.restore()

    def native_event(self, type_, message):
        """Для растяжения без рамочного окна в windows-системах
        Based on https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PySide6"""
        msg = MSG.from_address(message.__int__())
        if not msg.hWnd:
            return super().nativeEvent(type_, message)

        if msg.message == win32con.WM_NCHITTEST:
            pos = QCursor.pos()
            xPos = pos.x() - self.x()
            yPos = pos.y() - self.y()
            w, h = self.width(), self.height()
            lx = xPos < SizeGrip.WIDTH
            rx = xPos > w - SizeGrip.WIDTH
            ty = yPos < SizeGrip.WIDTH
            by = yPos > h - SizeGrip.WIDTH
            if lx and ty:
                return True, win32con.HTTOPLEFT
            elif rx and by:
                return True, win32con.HTBOTTOMRIGHT
            elif rx and ty:
                return True, win32con.HTTOPRIGHT
            elif lx and by:
                return True, win32con.HTBOTTOMLEFT
            elif ty:
                return True, win32con.HTTOP
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT
        elif msg.message == win32con.WM_NCCALCSIZE:
            result = 0 if not msg.wParam else win32con.WVR_REDRAW  # исправляет мерцания при раскрытии окна
            return True, result

        return super().nativeEvent(type_, message)

    def change_event(self, event):
        if event.type() == QEvent.WindowStateChange:
            is_maximized = self.isMaximized()
            self.enable_rounded_corners(not is_maximized)
            for grip in self.findChildren(SizeGrip):
                grip.setHidden(is_maximized)

    def current_search_engine(self):
        return search_engines[self.address_panel.search_box.currentText()]

    def change_style(self, name=None):
        self.theme = Theme(self, name)
        self.setStyleSheet(self.theme.style())
        self.address_line_edit.findChild(QToolButton).setIcon(QIcon('custom:close(address_line_frame).svg'))

    def enable_rounded_corners(self, rounded: bool = True):
        self.main_frame.setStyleSheet(Template("""
                #main_frame { 
                    border-radius: $radius;
                }""").substitute(radius='12px' if rounded else '0px'))

    def show_find_on_page(self):
        page = self.tab_widget.current()
        page_find_widget = page.findChild(FindWidget)
        if page_find_widget:
            if not page_find_widget.isHidden():
                page_find_widget.hide_find()
            else:
                page_find_widget.show()
                page_find_widget.find_focus()
                page_find_widget.find_text()
        elif not page.view.embedded:
            find_widget = FindWidget(page)
            page.layout().addWidget(find_widget)
            find_widget.show()
            find_widget.find_focus()

    def load_home_page(self, new_tab=True):
        if new_tab:
            self.tab_widget.create_tab()
        self.tab_widget.current().load(self.settings.get('homePage'))

    def set_title(self, text):
        self.setWindowTitle(f"{'[Приватный режим]' if self.private_mode else ''} {text} – {devoud.__name__} {devoud.__version__}")
        if self.title_bar is not None:
            self.title_bar.label.setText(f"{'[Приватный режим]' if self.private_mode else ''} {text} – {devoud.__name__} {devoud.__version__}")

    def back_page(self):
        self.tab_widget.current().back()

    def forward_page(self):
        self.tab_widget.current().forward()

    def stop_load_page(self):
        self.tab_widget.current().stop()

    def update_page(self):
        self.tab_widget.current().reload()

    @staticmethod
    def create_new_window(private_mode=False, session=None, settings=None):
        window = BrowserWindow(private_mode=private_mode, session=session, settings=settings)
        window.show()
        window.change_style()

    def closeEvent(self, event):
        self.session.save()
        self.session.clear_objects()
        super().closeEvent(event)

    def restart(self):
        self.session.save()
        self.close()
        self.create_new_window(self.private_mode, self.session.session(), self.settings.settings())
        self.deleteLater()

    @cached_property
    def tab_widget(self):
        return BrowserTabWidget()
