import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("reminder.db")
        self.cursor = self.conn.cursor()

        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def add_task(self, title):
        self.cursor.execute(
            "INSERT INTO tasks(title) VALUES(?)",
            (title,)
        )
        self.conn.commit()

    def get_tasks(self):
        self.cursor.execute(
            "SELECT id, title FROM tasks ORDER BY id DESC"
        )
        return self.cursor.fetchall()

    def delete_task(self, task_id):
        self.cursor.execute(
            "DELETE FROM tasks WHERE id=?",
            (task_id,)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()