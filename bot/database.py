import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

def create_table():
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task_name TEXT,
            task_description TEXT,
            task_status TEXT
            )
            ''')

    conn.commit()

def add_task():
    cursor.execute('''
        INSERT INTO tasks (task_name, task_description, task_status)
        VALUES (?, ?, ?)
    ''', ('Task 1', 'Do task 1', 'incomplete'))

    conn.commit()

create_table()
add_task()

# cursor.execute('SELECT * FROM tasks')
# rows = cursor.fetchall()
#
# for row in rows:
#     print(row)

conn.close()