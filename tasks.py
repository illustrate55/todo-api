from db import db

def task_get() -> list[dict]:
    with db() as conn:
        rows = conn.execute(
            "SELECT id, title, done FROM tasks ORDER BY id"
        ).fetchall()
    return [
        {"id": row["id"], "position": i, "title": row["title"], "done": row["done"]}
        for i, row in enumerate(rows, start=1)
    ]


def task_add(title: str) -> dict:
    with db() as conn:
        row = conn.execute(
            "INSERT INTO tasks (title) VALUES (%s) RETURNING id, done", 
            (title,)
        ).fetchone()
        task_id = row["id"]
        count = conn.execute("SELECT COUNT(*) AS c FROM tasks").fetchone()["c"]
    return {
        "id": task_id, 
        "position": count, 
        "title": title,
        "done": row["done"]
    }


def task_update_by_position(position: int, new_title: str) -> dict | None:
    with db() as conn:
        row = conn.execute(
            "SELECT id, done FROM tasks ORDER BY id LIMIT 1 OFFSET %s",
            (position - 1,),
        ).fetchone()
        if row is None:
            return None
        conn.execute(
            "UPDATE tasks SET title = %s WHERE id = %s", 
            (new_title, row["id"]),
        )
    return {
        "id": row["id"], 
        "position": position, 
        "title": new_title,
        "done": row["done"],
    }


def task_set_done_by_position(position: int, done: bool) -> dict | None:
    with db() as conn:
        row = conn.execute(
            "SELECT id, title FROM tasks ORDER BY id LIMIT 1 OFFSET %s",
            (position - 1,),
        ).fetchone()
        if row is None:
            return None
        conn.execute(
            "UPDATE tasks SET done = %s WHERE id = %s",
            (done, row["id"]),
        )
    return {
        "id": row["id"],
        "position": position,
        "title": row["title"],
        "done": done,
    }

 
def task_delete_by_position(position: int) -> bool:
    with db() as conn:
        row = conn.execute(
            "SELECT id FROM tasks ORDER BY id LIMIT 1 OFFSET %s", 
            (position - 1,),
        ).fetchone()
        if row is None:
            return False
        conn.execute("DELETE FROM tasks WHERE id = %s", (row["id"],))
    return True