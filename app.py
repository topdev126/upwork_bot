import sys
from PyQt5.QtWidgets import QApplication

from main import *

def window():
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec_())
if __name__ == '__main__':  
    window()
