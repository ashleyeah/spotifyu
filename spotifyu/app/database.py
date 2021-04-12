"""Defines all the functions related to the database"""
from app import db

def fetch_todo() -> dict:
    """Reads all tasks listed in the todo table
    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from SongsSmall;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[1], #task
            "release_date": result[2] #status
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
    query = 'UPDATE SongsSmall SET name = "{}" where song_id = "{}";'.format(text, task_id)
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


def insert_new_task(text: str) ->  None:
    """Insert new task to todo table.
    Args:
        text (str): Song name. Looks up the song name from SongsOld table, and
        gets the value of the attributes.
    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    separateVar = 'Select * from SongsOld where name = "{}" LIMIT 1;'.format(text)
    query_song_data = conn.execute(separateVar).fetchall()
    
    
    query = 'Insert Into SongsSmall (song_id, name, release_date) VALUES ("{}", "{}", "{}");'.format(
        query_song_data[0][0], query_song_data[0][1], query_song_data[0][2])
    conn.execute(query)
    
    
    conn.close()

    #return task_id


def remove_task_by_id(task_id: str) -> None:
    """ remove entries based on song ID """
    conn = db.connect()
    query = 'Delete From SongsSmall where song_id="{}";'.format(task_id) #task_id = song_id, also note- quotes around {}
    conn.execute(query)
    conn.close()

def advanced_query() -> dict:
    conn = db.connect()
    query_results = conn.execute("(SELECT COUNT(*) as freq, name FROM Albums GROUP BY name ORDER BY freq DESC LIMIT 7) UNION(SELECT COUNT(*) as freq, name FROM Songs GROUP BY name ORDER BY freq DESC LIMIT 8) ORDER BY freq DESC;").fetchall()
    todo_list = []
    for i in range(len(query_results)):
        query1 = 'Insert Into SongsSmall (song_id, name, release_date) VALUES ("{}", "{}", "1900-01-01");'.format(
            query_results[i][0], query_results[i][1])
        conn.execute(query1)
    conn.close()


    return todo_list