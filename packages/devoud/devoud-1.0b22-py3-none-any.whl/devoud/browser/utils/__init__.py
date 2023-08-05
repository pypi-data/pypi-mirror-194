# Based on https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PySide6
from devoud.browser import *

if platform == "win32":
    from ctypes.wintypes import MSG
    import win32con
    from .win32_utils import WindowsMoveResize as MoveResize
elif platform == "darwin":
    from .mac_utils import MacMoveResize as MoveResize
else:
    from .linux_utils import LinuxMoveResize as MoveResize


def move_window(window, globalPos):
    MoveResize.startSystemMove(window, globalPos)


def resize_window(window, globalPos, edges):
    MoveResize.starSystemResize(window, globalPos, edges)
