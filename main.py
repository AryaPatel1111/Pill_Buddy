from PyQt5 import QtWidgets
from login import LoginWindow
from mainwindow import MainWindow
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)

    login_dialog = LoginWindow()
    if login_dialog.exec_() == QtWidgets.QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
