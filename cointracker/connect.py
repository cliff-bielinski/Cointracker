import psycopg2
from config.config import config

def insert_row(table_name, data):
    """
    connect to the database server and inserts data as row in table for db
    Args:
        table_name(str): the table having the row of data inserted into
        data (dictionary): a map of data to store as a row in the database
    
    Returns:
        a string confirming successful upload into db
    """
    def commit_row(query):
        """executes SQL query and commits it to database"""
        cursor.execute(query, data)
        connection.commit()
        count = cursor.rowcount
        print(count, f'row inserted successfully into {table_name} table')

    try:
        db_params = config('postgresql')  # stored in database.ini file

        print("Connecting to the database...")
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # SQL query for insertion into subreddits table
        subreddit_query = """
            INSERT INTO subreddits (subreddit_id, subreddit_name)
            VALUES (%(subreddit_id)s, %(subreddit_name)s)
            ON CONFLICT (subreddit_id)
            DO NOTHING;
            """

        # SQL query for insertion into authors table
        author_query = """
            INSERT INTO authors (author_id, author_name)
            VALUES (%(author_id)s, %(author_name)s)
            ON CONFLICT (author_id)
            DO NOTHING;
            """

        # SQL query for insertion into submissions table
        submission_query = """
            INSERT INTO submissions (post_id, post_name, author_id, coin_id, subreddit_id, submission_time)
            VALUES (%(id)s, %(name)s, %(author)s, %(coin)s, %(subreddit_id)s, %(time)s)
            ON CONFLICT (post_id)
            DO NOTHING;
            """
        
        # SQL query for insertion into comments table
        comment_query = """
            INSERT INTO comments (comment_id, comment_time, parent_id, score, body, pulled_at, post_id, author_id, coin_id)
            VALUES (%(id)s, %(time)s, %(parent)s, %(score)s, %(body)s, %(pulled)s, %(post)s, %(author)s, %(coin)s)
            ON CONFLICT (comment_id)
            DO NOTHING;
            """

        if table_name == 'subreddits':
            commit_row(subreddit_query)
        elif table_name == 'authors':
            commit_row(author_query)
        elif table_name == 'submissions':
            commit_row(submission_query)
        elif table_name == 'comments':
            commit_row(comment_query) 

    except (Exception, psycopg2.Error) as error:
        print(f"Failed to insert record into {table_name} table", error)

    finally:
        # closes connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    