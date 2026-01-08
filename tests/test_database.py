import sqlite3
import pytest
from taskmaster.database import add_task, all_tasks, get_task_id, update_task, search_tasks, delete_tasks, filter_tasks

DB_TEST = "test_taskmaster.db"

def setup_module(module):
    with sqlite3.connect(DB_TEST) as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS tasks")
        cur.execute("""
        CREATE TABLE tasks (
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
        sample_tasks = [
            ("Task A", "First task", "todo", "high", "work,urgent"),
            ("Task B", "Second task", "in_progress", "medium", "home"),
            ("Task C", "Another urgent task", "done", "low", "work,fun"),
        ]
        for t in sample_tasks:
            cur.execute(
                "INSERT INTO tasks (title, description, status, priority, tags) VALUES (?, ?, ?, ?, ?)",
                t
            )

def test_add_task():
    add_task(DB_TEST, "Test Task", description="Testing insert", status="todo", priority="high", tags="test", due_date="2026-01-10")
    with sqlite3.connect(DB_TEST) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM tasks WHERE title = ?", ("Test Task",))
        row = cur.fetchone()
    assert row is not None
    assert row[1] == "Test Task"
    assert row[3] == "todo"
    assert row[4] == "high"

def test_all_tasks():
    rows = all_tasks(DB_TEST)
    assert isinstance(rows, list)
    assert len(rows) > 0
    assert rows[0][1] == "Task A"
    assert rows[0][4] == "high"

def test_get_task():
    item = get_task_id(DB_TEST, 1)
    assert isinstance(item, tuple)
    assert len(item) > 0
    assert item[0] == 1

def test_update_task():
    test_update = update_task(DB_TEST, 1, title="testing if it works")
    assert test_update is True
    with sqlite3.connect(DB_TEST) as con:
        cur = con.cursor()
        cur.execute("SELECT title FROM tasks WHERE id = 1")
        row = cur.fetchone()
    assert row is not None
    assert row[0] == "testing if it works"

def test_search_tasks_found():
    results = search_tasks(DB_TEST, "urgent")
    assert isinstance(results, list)

    titles = [r[1] for r in results]  # index 1 = title
    assert "Task C" in titles

    # Optionally, check that only Task C is returned
    assert len(results) == 1


def test_search_tasks_not_found():
    results = search_tasks(DB_TEST, "nonexistent")
    assert results == []

def test_delete_tasks_existing():
    deleted = delete_tasks(DB_TEST, 2)
    assert deleted is True
    with sqlite3.connect(DB_TEST) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM tasks WHERE id = 2")
        assert cur.fetchone() is None

def test_delete_tasks_nonexistent():
    deleted = delete_tasks(DB_TEST, 999)
    assert deleted is False

def test_filter_tasks_status():
    results = filter_tasks(DB_TEST, status="todo")
    assert all(r[3] == "todo" for r in results)

def test_filter_tasks_priority():
    results = filter_tasks(DB_TEST, priority="low")
    assert all(r[4] == "low" for r in results)

def test_filter_tasks_tags_single():
    results = filter_tasks(DB_TEST, tags=["urgent"])
    assert all("urgent" in r[5] for r in results)

def test_filter_tasks_tags_multiple():
    results = filter_tasks(DB_TEST, tags=["urgent", "fun"])
    for r in results:
        assert any(tag in r[5] for tag in ["urgent", "fun"])

def test_filter_tasks_combined():
    results = filter_tasks(DB_TEST, status="done", priority="low", tags=["fun"])
    assert len(results) == 1
    assert results[0][1] == "Task C"
