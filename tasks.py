from db import db

def task_get() -> list[dict]:
    with db() as conn:
        rows = conn.execute("SELECT id, title FROM tasks ORDER BY id").fetchall()
    return [
        {"id": row["id"], "position": i, "title": row["title"]}
        for i, row in enumerate(rows, start=1)
    ]


def task_add(title: str) -> dict:
    with db() as conn:
        cursor = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        task_id = cursor.lastrowid
        count = conn.execute("SELECT COUNT(*) AS c FROM tasks").fetchone()["c"]
    return {"id": task_id, "position": count, "title": title}


def task_update_by_position(position: int, new_title: str) -> dict | None:
    with db() as conn:
        row = conn.execute(
            "SELECT id FROM tasks ORDER BY id LIMIT 1 OFFSET ?",
            (position - 1,),
        ).fetchone()
        if row is None:
            return None
        task_id = row["id"]
        conn.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_title, task_id))
    return {"id": task_id, "position": position, "title": new_title}

 
def task_delete_by_position(position: int) -> bool:
    with db() as conn:
        row = conn.execute(
            "SELECT id FROM tasks ORDER BY id LIMIT 1 OFFSET ?", 
            (position - 1,),
        ).fetchone()
        if row is None:
            return False
        conn.execute("DELETE FROM tasks WHERE id = ?", (row["id"],))
    return True