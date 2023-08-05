# Based on https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PySide6
from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication


class LinuxMoveResize:

    @classmethod
    def startSystemMove(cls, window, globalPos):
        window.windowHandle().startSystemMove()
        event = QMouseEvent(QEvent.MouseButtonRelease, QPoint(-1, -1),
                            Qt.LeftButton, Qt.NoButton, Qt.NoModifier)
        QApplication.instance().postEvent(window.windowHandle(), event)

    @classmethod
    def starSystemResize(cls, window, globalPos, edges):
        if not edges:
            return

        window.windowHandle().startSystemResize(edges)
