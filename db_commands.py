import sqlite3

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")

def execute_write_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")


def high_score_order(level):

    level = f'lvl_{level}'

    high_score_order_query = f"""
    SELECT
        user_name,
        {level}
    FROM
        users_data
    WHERE
        {level} != 0
    ORDER BY
        {level} ASC
    """

    with sqlite3.connect("game_data.db") as conn:
        high_scores = execute_read_query(conn, high_score_order_query)

    return high_scores

def is_name_taken(name):

    is_name_taken_query = f"""
    SELECT
        *
    FROM
        users_data
    WHERE
        user_name == '{name}'
    """

    with sqlite3.connect("game_data.db") as conn:
        if len(execute_read_query(conn, is_name_taken_query)) > 0:
            return True
        else:
            return False

def get_high_score(user_name, level):

    level = f'lvl_{level}'

    get_high_score_query = f"""
    SELECT
        {level}
    FROM
        users_data
    WHERE
        user_name == '{user_name}'
    ORDER BY
        {level} ASC
    """

    with sqlite3.connect("game_data.db") as conn:
        high_score = execute_read_query(conn, get_high_score_query)

    return float(str(high_score[0])[1:-2])

def write_high_score(user_name, level, score):

    level = f'lvl_{level}'

    write_high_score_query = f"""
    UPDATE
        users_data
    SET
        {level} = {score}
    WHERE
        user_name == '{user_name}'
    """

    with sqlite3.connect("game_data.db") as conn:
        execute_write_query(conn, write_high_score_query)

def update_high_score(user_name, level, recent_score):

    old_score = get_high_score(user_name, level)

    if old_score == 0 or recent_score < old_score:
        write_high_score(user_name, level, recent_score)

def get_score_ranking(user_name, level):

    high_scores = high_score_order(level)
    ranking = 0
    for i in range(0, len(high_scores)):
        if high_scores[i][0] == user_name:
            ranking = i + 1

    return ranking

def name_entered(user_name):

    #if false returned, name exists, if true returned, new name added to database as name is new

    if is_name_taken(user_name):
        return False
    else:
        return True

def add_name_entered(user_name):

    if not is_name_taken(user_name):
        write_new_name_query = f"""
                         INSERT INTO users_data (user_name, lvl_1, lvl_2, lvl_3)
                         VALUES ('{user_name}', 0, 0, 0);"""
        with sqlite3.connect("game_data.db") as conn:
            execute_write_query(conn, write_new_name_query)

#is_name_taken('starchy')
#get_high_score('starchy', 1)
#write_high_score('starchy', 1, 32.1)
#update_high_score('starchy', 1, 32)
#get_score_ranking('starchy', 1)
#name_entered('marcy')