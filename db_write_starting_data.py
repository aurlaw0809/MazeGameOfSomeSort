import sqlite3

conn = sqlite3.connect('game_data.db')
cursor = conn.cursor()

user_data = [('starchy', 30, 50, 70),
         ('gunther', 35, 48, 76),
         ('simon', 28, 60, 80),
        ]

paramterised_insert_query1 = """
    INSERT INTO users_data (user_name, lvl_1, lvl_2, lvl_3)
    VALUES (?, ?, ?, ?);"""

cursor.executemany(paramterised_insert_query1, user_data)
conn.commit()
