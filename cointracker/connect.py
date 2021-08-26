import psycopg2
from config.config import config

def insert_row(comment_dict, subreddit_dict):
    """
    connect to the database server and inserts prepared comment as row in comments table for db
    Args:
        comment_dict (dictionary): a map of comment metadata to store as a row in the database
    
    Returns:
        a string confirming successful upload into db
    """
    def commit_row(table_name, query, data):
        """
        executes SQL query and commits it to database

        Args:
            table_name (str) - name of table row to be inserted in
            query (str) - SQL query to be executed by db
            data (dict) - map of columns to data values
        """
        cursor.execute(query, data)
        connection.commit()
        count = cursor.rowcount
        print(count, f'row inserted successfully into {table_name} table')

    try:
        db_params = config('postgresql')  # stored in database.ini file

        print("Connecting to the database...")
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        subreddit_query = """
            INSERT INTO subreddits (subreddit_id, subreddit_name)
            VALUES (%(subreddit_id)s, %(subreddit_name)s)
            ON CONFLICT (subreddit_id)
            DO NOTHING;
            """

        comment_query = """
            INSERT INTO comments (comment_id, comment_time, parent_id, score, body, pulled_at, post_id, author_id, coin_id)
            VALUES (%(id)s, %(time)s, %(parent)s, %(score)s, %(body)s, %(pulled)s, %(post)s, %(author)s, %(coin)s);
            """
        
        commit_row('subreddits', subreddit_query, comment_dict)

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into comments table", error)

    finally:
        # closes connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    