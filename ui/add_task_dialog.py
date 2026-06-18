from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QComboBox
)


class AddTaskDialog(QDialog):
    def __init__(
        self,
        title="",
        description="",
        priority="Medium"
    ):
        super().__init__()

        self.setWindowTitle("Task")
        self.resize(450, 300)

        layout = QVBoxLayout(self)

        # Title

        layout.addWidget(QLabel("Title"))

        self.title_input = QLineEdit()
        self.title_input.setText(title)
        self.title_input.setPlaceholderText(
            "Enter task title..."
        )

        layout.addWidget(self.title_input)

        # Description

        layout.addWidget(QLabel("Description"))

        self.description_input = QTextEdit()
        self.description_input.setPlainText(description)

        layout.addWidget(self.description_input)

        # Priority

        layout.addWidget(QLabel("Priority"))

        self.priority_input = QComboBox()
        self.priority_input.addItems(
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        index = self.priority_input.findText(priority)

        if index >= 0:
            self.priority_input.setCurrentIndex(index)

        layout.addWidget(self.priority_input)

        # Buttons

        buttons = QHBoxLayout()

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        buttons.addWidget(self.save_button)
        buttons.addWidget(self.cancel_button)

        layout.addLayout(buttons)
