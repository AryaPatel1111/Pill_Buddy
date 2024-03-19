from PyQt5 import QtWidgets, uic
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("ui/mainwindow.ui", self)

        # Find the widgets using their object names and connect them
        self.viewReportsButton = self.findChild(QtWidgets.QPushButton, 'viewReportsButton')
        self.viewReportsButton.clicked.connect(self.view_reports)

        self.enterDataButton = self.findChild(QtWidgets.QPushButton, 'enterDataButton')
        self.enterDataButton.clicked.connect(self.enter_data)

        # Repeat for other functionalities

    def view_reports(self):
        # Code to handle viewing reports
        print("View Reports clicked")

    def enter_data(self):
        # Code to handle data entry
        print("Enter Data clicked")

    # Implement other methods for additional buttons

# Below would typically be in your main.py
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
