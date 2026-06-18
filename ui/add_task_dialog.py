from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout
)


class AddTaskDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Task")
        self.resize(400, 150)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Task Title"))

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter your task...")
        layout.addWidget(self.title_input)

        buttons = QHBoxLayout()

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        buttons.addWidget(self.save_button)
        buttons.addWidget(self.cancel_button)

        layout.addLayout(buttons)