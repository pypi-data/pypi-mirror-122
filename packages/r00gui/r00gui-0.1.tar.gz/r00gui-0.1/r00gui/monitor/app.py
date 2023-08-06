import sys
from PySide6.QtWidgets import QMainWindow, QApplication
from r00gui.monitor.interface import Ui_MainWindow

class Moninor(QMainWindow):
    def __init__(self, parent=None):
        super(Moninor, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QApplication()
    moninor = Moninor()
    moninor.show()
    sys.exit(app.exec())