import win32api
import win32con
import win32gui


class WindowsMoveResize:

    @staticmethod
    def startSystemMove(window, globalPos):
        win32gui.ReleaseCapture()
        win32api.SendMessage(
            int(window.winId()),
            win32con.WM_SYSCOMMAND,
            win32con.SC_MOVE | win32con.HTCAPTION,
            0
        )

    @classmethod
    def starSystemResize(cls, window, globalPos, edges):
        pass
