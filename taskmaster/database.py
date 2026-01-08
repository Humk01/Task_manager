import sqlite3


db = "taskmaster.db"
with sqlite3.connect(db) as con:
    cur = con.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL DEFAULT 'todo',
        priority TEXT NOT NULL DEFAULT 'medium',
        tags TEXT,
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        due_date TEXT,
        completed_at TEXT
    )
    """)

# Function to add a task
def add_task(db, title, description=None, status='todo', priority='medium', tags=None, due_date=None):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO tasks (title, description, status, priority, tags, due_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, status, priority, tags, due_date))
        

def all_tasks(db):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM tasks")
        return cur.fetchall()
    
def get_task_id(db, id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM tasks WHERE id = ?", (id,))
        return cur.fetchone()
    
def update_task(
    db,
    task_id,
    title=None,
    status=None,
    priority=None,
    due_date=None
):
    fields = []
    values = []

    if title is not None:
        fields.append("title = ?")
        values.append(title)

    if status is not None:
        fields.append("status = ?")
        values.append(status)

    if priority is not None:
        fields.append("priority = ?")
        values.append(priority)

    if due_date is not None:
        fields.append("due_date = ?")
        values.append(due_date)

    if not fields:
        return False  # nothing to update

    values.append(task_id)

    sql = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"

    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(sql, values)
        return cur.rowcount > 0
    

def search_tasks(db, keyword):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        search_term = f"%{keyword}%"  # sql wildcard term
        cur.execute("""
            SELECT * FROM tasks 
            WHERE title LIKE ? OR description LIKE ?
            ORDER BY created_at DESC
        """, (search_term, search_term))
        return cur.fetchall()
    
def delete_tasks(db, id):
    """
    Permanently delete tasks from the database
    :param db: database file path
    :param id: int
    :returns: True if a file was deleted
    """

    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute("""
            DELETE FROM tasks WHERE id = ?
            """, (id,))
        return cur.rowcount > 0
    

def filter_tasks(db, status=None, priority=None, tags=None):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        query = "SELECT * FROM tasks WHERE TRUE"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        if tags:
            tag_conditions = " OR ".join(["tags LIKE ?" for _ in tags])
            query += f" AND ({tag_conditions})"
            params.extend([f"%{tag}%" for tag in tags])
        query += " ORDER BY created_at DESC"
        cur.execute(query, params)
        return cur.fetchall()

