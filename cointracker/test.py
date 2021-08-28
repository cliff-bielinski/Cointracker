from pmaw import PushshiftAPI
from datetime import datetime, timedelta
import sanitize


def get_post_ids():
    time = int((datetime.today() - timedelta(days=10)).timestamp())

    api = PushshiftAPI()
    posts = api.search_submissions(q='daily', subreddit='cryptocurrency',stickied=True, after=time)
    post_list = [(
        post['id'], post['title'], 
        post['author_fullname'], 
        sanitize.sanitize_text(post['selftext']),
        post['subreddit_id'],
        datetime.fromtimestamp(post['created_utc'])) 
        for post in posts]
    return post_list
