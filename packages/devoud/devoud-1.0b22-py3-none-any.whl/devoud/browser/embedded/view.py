from devoud.browser import *


class EmbeddedView(QWidget):
    title = "'Embedded Page'"
    url = None

    def __init__(self, parent, *args):
        super().__init__(parent)
        self.setObjectName('embedded_view')
        self.embedded = True
        self.parent = parent

    def load(self, url):
        self.parent.load(url)

    def stop(self):
        ...

    def reload(self):
        self.parent.load(self.url)

    def forward(self):
        ...

    def back(self):
        ...

    def is_loading(self):
        return False
