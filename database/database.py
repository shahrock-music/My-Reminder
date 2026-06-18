import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("reminder.db")
        self.cursor = self.conn.cursor()

        self.create_table()
        self.migrate_database()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            priority TEXT DEFAULT 'Medium',
            completed INTEGER DEFAULT 0
        )
        """)
        self.conn.commit()

    def migrate_database(self):
        self.cursor.execute("PRAGMA table_info(tasks)")
        columns = [column[1] for column in self.cursor.fetchall()]

        if "description" not in columns:
            self.cursor.execute(
                "ALTER TABLE tasks ADD COLUMN description TEXT DEFAULT ''"
            )

        if "priority" not in columns:
            self.cursor.execute(
                "ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'Medium'"
            )

        if "completed" not in columns:
            self.cursor.execute(
                "ALTER TABLE tasks ADD COLUMN completed INTEGER DEFAULT 0"
            )

        self.conn.commit()

    def add_task(self, title, description="", priority="Medium"):
        self.cursor.execute(
            """
            INSERT INTO tasks(
                title,
                description,
                priority
            )
            VALUES (?, ?, ?)
            """,
            (
                title,
                description,
                priority
            )
        )

        self.conn.commit()

    def get_tasks(
        self,
        search_text="",
        priority_filter="All"
    ):
        query = """
        SELECT
            id,
            title,
            description,
            priority,
            completed
        FROM tasks
        WHERE 1=1
        """

        params = []

        if search_text:
            query += """
            AND (
                title LIKE ?
                OR description LIKE ?
            )
            """

            params.extend([
                f"%{search_text}%",
                f"%{search_text}%"
            ])

        if priority_filter != "All":
            query += " AND priority = ? "
            params.append(priority_filter)

        query += " ORDER BY id DESC "

        self.cursor.execute(query, params)

        return self.cursor.fetchall()

    def update_task(
        self,
        task_id,
        title,
        description,
        priority
    ):
        self.cursor.execute(
            """
            UPDATE tasks
            SET
                title=?,
                description=?,
                priority=?
            WHERE id=?
            """,
            (
                title,
                description,
                priority,
                task_id
            )
        )

        self.conn.commit()

    def complete_task(
        self,
        task_id,
        completed=1
    ):
        self.cursor.execute(
            """
            UPDATE tasks
            SET completed=?
            WHERE id=?
            """,
            (
                completed,
                task_id
            )
        )

        self.conn.commit()

    def delete_task(self, task_id):
        self.cursor.execute(
            "DELETE FROM tasks WHERE id=?",
            (task_id,)
        )

        self.conn.commit()

    def close(self):
        self.conn.close()
