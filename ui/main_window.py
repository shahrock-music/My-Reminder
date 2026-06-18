from PySide6.QtCore import Qt
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
    QLineEdit,
    QComboBox
)

from ui.add_task_dialog import AddTaskDialog
from database.database import Database


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = Database()

        self.setWindowTitle("My Reminder")
        self.resize(1000, 700)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        title = QLabel("📋 My Reminder")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
        """)

        layout.addWidget(title)

        # Search + Filter

        top_bar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search tasks..."
        )

        self.search_input.textChanged.connect(
            self.load_tasks
        )

        self.priority_filter = QComboBox()
        self.priority_filter.addItems(
            [
                "All",
                "High",
                "Medium",
                "Low"
            ]
        )

        self.priority_filter.currentTextChanged.connect(
            self.load_tasks
        )

        top_bar.addWidget(self.search_input)
        top_bar.addWidget(self.priority_filter)

        layout.addLayout(top_bar)

        # Task List

        self.task_list = QListWidget()

        self.task_list.itemDoubleClicked.connect(
            self.edit_task
        )

        layout.addWidget(self.task_list)

        # Buttons

        buttons = QHBoxLayout()

        self.add_button = QPushButton("➕ Add")
        self.edit_button = QPushButton("✏ Edit")
        self.complete_button = QPushButton("✔ Complete")
        self.delete_button = QPushButton("🗑 Delete")

        self.add_button.clicked.connect(
            self.open_add_task
        )

        self.edit_button.clicked.connect(
            self.edit_task
        )

        self.complete_button.clicked.connect(
            self.complete_task
        )

        self.delete_button.clicked.connect(
            self.delete_task
        )

        buttons.addWidget(self.add_button)
        buttons.addWidget(self.edit_button)
        buttons.addWidget(self.complete_button)
        buttons.addWidget(self.delete_button)

        layout.addLayout(buttons)

        self.load_tasks()

    def load_tasks(self):
        self.task_list.clear()

        search_text = (
            self.search_input.text().strip()
        )

        priority_filter = (
            self.priority_filter.currentText()
        )

        tasks = self.db.get_tasks(
            search_text,
            priority_filter
        )

        for (
            task_id,
            title,
            description,
            priority,
            completed
        ) in tasks:

            status = "✔" if completed else "○"

            text = (
                f"{status} "
                f"[{priority}] "
                f"{title}"
            )

            item = QListWidgetItem(text)

            item.setToolTip(
                description
                if description
                else "No description"
            )

            if priority == "High":
                item.setForeground(Qt.red)

            elif priority == "Medium":
                item.setForeground(Qt.darkYellow)

            elif priority == "Low":
                item.setForeground(Qt.darkGreen)

            item.setData(
                1,
                {
                    "id": task_id,
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "completed": completed
                }
            )

            self.task_list.addItem(item)

    def open_add_task(self):
        dialog = AddTaskDialog()

        if dialog.exec():

            title = (
                dialog.title_input.text().strip()
            )

            description = (
                dialog.description_input
                .toPlainText()
                .strip()
            )

            priority = (
                dialog.priority_input
                .currentText()
            )

            if not title:

                QMessageBox.warning(
                    self,
                    "Warning",
                    "Title is required."
                )

                return

            self.db.add_task(
                title,
                description,
                priority
            )

            self.load_tasks()

    def edit_task(self):
        item = self.task_list.currentItem()

        if item is None:

            QMessageBox.warning(
                self,
                "Warning",
                "Select a task."
            )

            return

        data = item.data(1)

        dialog = AddTaskDialog(
            title=data["title"],
            description=data["description"],
            priority=data["priority"]
        )

        if dialog.exec():

            title = (
                dialog.title_input.text().strip()
            )

            description = (
                dialog.description_input
                .toPlainText()
                .strip()
            )

            priority = (
                dialog.priority_input
                .currentText()
            )

            self.db.update_task(
                data["id"],
                title,
                description,
                priority
            )

            self.load_tasks()

    def complete_task(self):
        item = self.task_list.currentItem()

        if item is None:

            QMessageBox.warning(
                self,
                "Warning",
                "Select a task."
            )

            return

        data = item.data(1)

        new_state = (
            0 if data["completed"]
            else 1
        )

        self.db.complete_task(
            data["id"],
            new_state
        )

        self.load_tasks()

    def delete_task(self):
        item = self.task_list.currentItem()

        if item is None:

            QMessageBox.warning(
                self,
                "Warning",
                "Select a task."
            )

            return

        reply = QMessageBox.question(
            self,
            "Delete Task",
            "Are you sure you want to delete this task?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        data = item.data(1)

        self.db.delete_task(
            data["id"]
        )

        self.load_tasks()
