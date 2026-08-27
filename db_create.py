import sqlite3

create_users_table = """
CREATE TABLE IF NOT EXISTS users_data (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    lvl_1 FLOAT NOT NULL,
    lvl_2 FLOAT NOT NULL,
    lvl_3 FLOAT NOT NULL
);"""

with sqlite3.connect('game_data.db') as conn:
    cursor = conn.cursor()
    cursor.execute(create_users_table)
    conn.commit()