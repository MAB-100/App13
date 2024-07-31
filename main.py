from PyQt6.QtGui import QAction, QIcon # Import the QAction and QIcon classes
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
     QLineEdit, QMainWindow, QPushButton, QGridLayout, \
     QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, \
     QComboBox

import sys
import sqlite3



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stdent Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name","Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)

        self.setCentralWidget(self.table)

        

    def load_data(self):
        conn = sqlite3.connect("database.db")
        # cursor = conn.cursor()
        data = conn.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.table.insertRow(row_index)
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        conn.close()
    
    def insert(self):
        insert_dialog = InsertDialog()
        insert_dialog.exec()
        



class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        #Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        #Add course combobox widget
        self.course_combobox = QComboBox()
        course = ["Biological Science", "Computer Science", "Physical Science", "Social Science"]
        self.course_combobox.addItems(course)
        layout.addWidget(self.course_combobox)

        #Add student mobile widget
        self.student_mobile = QLineEdit()
        self.student_mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.student_mobile)

        #Add submit button widget
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.save)
        layout.addWidget(submit_button)

        self.setLayout(layout)
        
    def save(self):
        name = self.student_name.text()
        course = self.course_combobox.itemText(self.course_combobox.currentIndex())
        mobile = self.student_mobile.text()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        conn.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, mobile))
        conn.commit()
        conn.close()




app = QApplication(sys.argv)
student_registration = MainWindow()
student_registration.show()
student_registration.load_data()
sys.exit(app.exec())
