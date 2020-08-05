import praw
from config import token, db_file
import sqlite3
from sqlite3 import Error

def db_connection(database_file):
    try:
        connection = sqlite3.connect(database_file)
    except Error as err:        # Error checking here is broken
        print("Cannot connect to database")
        print(err)
        exit(-10)
    return connection
def read_table(conn, sql_table):
    """
    Query all rows in the table
    :param conn: the Connection object
    :param sql_table: the queriable table
    :return:
    """
    cur = conn.cursor()
    query = 'SELECT * FROM {}'.format(sql_table)
    cur.execute(query)
    rows = cur.fetchall()
    matches = [element for tupl in rows for element in tupl]
    return matches
def create_entry(conn, found_data):
    """
    Create a new project into the projects table
    :param conn:
    :param data:
    :return: data
    """
    sql = '''INSERT INTO (p_id,p_title,p_url) VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, found_data)
    conn.commit()
    return cur.lastrowid

# Define Reddit
reddit = praw.Reddit('bot1', config_interpolation="basic")
reddit.read_only = True  # set our reddit instance to read only.. realistically was unnecessary
# Meat and potatoes
database = db_connection(db_file)
try:
    for submission in reddit.subreddit("gundeals").new(limit=300):  # Get the last 1000 from the gun deals subreddit
        #res = set(tuple(map(str, lowerString.split(' '))))
        wants = read_table(database,'seek')
        if any(matches in submission.title.lower() for matches in wants):
            create_entry(database,(submission.id,submission.title,submission.url))
            # Need to clean up the output before going into the database.
except ValueError:
    print("Oh Shit")
