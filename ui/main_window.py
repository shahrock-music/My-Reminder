from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QMessageBox,
    QInputDialog
)

from ui.add_task_dialog import AddTaskDialog
from database.database import Database


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = Database()

        self.setWindowTitle("My Reminder")
        self.resize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        title = QLabel("📋 My Reminder")
        layout.addWidget(title)

        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        buttons = QHBoxLayout()

        self.add_button = QPushButton("➕ Add")
        self.delete_button = QPushButton("🗑 Delete")

        self.add_button.clicked.connect(self.open_add_task)
        self.delete_button.clicked.connect(self.delete_task)

        buttons.addWidget(self.add_button)
        buttons.addWidget(self.delete_button)

        layout.addLayout(buttons)

        self.load_tasks()

    def load_tasks(self):
        self.task_list.clear()

        tasks = self.db.get_tasks()

        for task_id, title in tasks:
            item = QListWidgetItem(title)
            item.setData(1, task_id)
            self.task_list.addItem(item)

    def open_add_task(self):
        dialog = AddTaskDialog()

        if dialog.exec():
            title = dialog.title_input.text().strip()

            if title:
                self.db.add_task(title)
                self.load_tasks()

    def delete_task(self):
        item = self.task_list.currentItem()

        if item is None:
            QMessageBox.warning(
                self,
                "Warning",
                "Please select a task."
            )
            return

        task_id = item.data(1)

        self.db.delete_task(task_id)

        self.load_tasks()