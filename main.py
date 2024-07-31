from PyQt6.QtGui import QAction, QIcon # Import the QAction and QIcon classes
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
     QLineEdit, QMainWindow, QPushButton, QGridLayout, QTableWidget, QTableWidgetItem   
import sys
import sqlite3



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stdent Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name","Course", "Mobile"))

        self.setCentralWidget(self.table)

    def add_student(self):
        pass



app = QApplication(sys.argv)
student_registration = MainWindow()
student_registration.show()
sys.exit(app.exec())
