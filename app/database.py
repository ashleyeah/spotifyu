"""Defines all the functions related to the database"""
from app import db
from datetime import date

def fetch_todo() -> dict:
    """Reads all tasks listed in the todo table
    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * From SongsOld LIMIT 30;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[1],
            "release_date": result[2]
        }
        todo_list.append(item)

    return todo_list


def update_task_entry(task_id: str, text: str) -> None:
    """Updates task description based on given `task_id`
    Args:
        task_id (int): Targeted task_id
        text (str): Updated description
    Returns:
        None
    """

    conn = db.connect()
    query = 'UPDATE SongsOld SET name = "{}" where song_id = "{}";'.format(text, task_id)
    conn.execute(query)
    conn.close()


def update_status_entry(task_id: int, text: str) -> None:
    """Updates task status based on given `task_id`
    Args:
        task_id (int): Targeted task_id
        text (str): Updated status
    Returns:
        None
    """

    conn = db.connect()
    query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def insert_new_task(artist_id: str, name: str) ->  None:
    """Insert new task to todo table.
    Args:
        text (str): Song name. Looks up the song name from SongsOld table, and
        gets the value of the attributes.
    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    today = date.today()
    query = 'Insert Ignore Into SongsOld (song_id, name, release_date) VALUES ("{}", "{}", "{}");'.format(
        artist_id, name, today)
    conn.execute(query)
    conn.close()

    return artist_id


def remove_task_by_id(task_id: str) -> None:
    """ remove entries based on song ID """
    conn = db.connect()
    query = 'Delete From SongsOld Where song_id="{}";'.format(task_id) #task_id = song_id, also note- quotes around {}
    conn.execute(query)
    conn.close()

def advanced_query() -> dict:
    conn = db.connect()
    query_results = conn.execute("(SELECT COUNT(*) as freq, name FROM Albums GROUP BY name ORDER BY freq DESC LIMIT 7) UNION(SELECT COUNT(*) as freq, name FROM Songs GROUP BY name ORDER BY freq DESC LIMIT 8) ORDER BY freq DESC;").fetchall()
    query_res = []
    for result in query_results:
        item = {
            "Frequency": result[0],
            "Name": result[1]
        }
        query_res.append(item)
    print(query_res)
    return query_res

def search(name: str) -> dict:
    conn = db.connect()
    sql='SELECT * FROM SongsOld WHERE name LIKE %s'
    args=['%'+name+'%']
    conn.execute(sql,args)
    query_results = conn.execute(sql,args).fetchall()
    search_res = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[1],
            "release_date": result[2]
        }
        search_res.append(item)
    return search_res