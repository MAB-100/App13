from PyQt6.QtGui import QAction, QIcon 
from PyQt6.QtWidgets import QApplication, QGridLayout, QLabel, \
     QLineEdit, QMainWindow, QPushButton, QToolBar, \
     QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, \
     QComboBox, QStatusBar, QMessageBox

import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stdent Management System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")


        add_student_action = QAction(QIcon("icons/add.png") ,"Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)


        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name","Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)


        # create and add toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)

        # create and add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # ddetect click on a cell
        self.table.cellClicked.connect(self.cell_click)

    def cell_click(self):
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)

        buttons = self.findChildren(QPushButton)
        if buttons:
            for button in buttons:
                self.status_bar.removeWidget(button)

        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)

    def about(self):
        dialog = AbputDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

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
        self.load_data()

class AbputDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About Student Management System")
        self.setText("This is a simple student management system")
        self.setIcon(QMessageBox.Icon.Information)

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("update Student")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        index = student_registration.table.currentRow()
        self.selected_id = student_registration.table.item(index, 0).text()
        selected_name = student_registration.table.item(index, 1).text()
        selected_course = student_registration.table.item(index, 2).text()
        selected_mobile = student_registration.table.item(index, 3).text()
        #Edit student name widget
        self.student_name = QLineEdit(selected_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        #Add course combobox widget
        self.course_combobox = QComboBox()
        course = ["Biology", "Math", "Physics", "Astronomy"]
        self.course_combobox.addItems(course)
        self.course_combobox.setCurrentText(selected_course)
        layout.addWidget(self.course_combobox)

        #Add student mobile widget
        self.student_mobile = QLineEdit(selected_mobile)
        self.student_mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.student_mobile)

        #Add submit button widget
        submit_button = QPushButton("Update")
        submit_button.clicked.connect(self.update)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def update(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                        (self.student_name.text(), self.course_combobox.itemText(self.course_combobox.currentIndex()), 
                         self.student_mobile.text(), self.selected_id))
        conn.commit()
        cursor.close()
        conn.close()
        student_registration.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("update Student")


        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete this student?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)  
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)

    def delete_student(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        index = student_registration.table.currentRow()
        selected_id = student_registration.table.item(index, 0).text()

        cursor.execute("DELETE FROM students WHERE id = ?", (selected_id,))
        conn.commit()
        cursor.close()
        conn.close()
        student_registration.load_data()
        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Student Management System")
        confirmation_widget.setText("Student deleted successfully")
        confirmation_widget.exec()


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
