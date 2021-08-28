import praw
import wallet
import sanitize
from datetime import datetime, timedelta
from pmaw import PushshiftAPI
import connect

def get_new_posts(query, location, time, sticky=False):
    day_num = int((datetime.today() - timedelta(days=time)).timestamp())

    api = PushshiftAPI()
    posts = api.search_submissions(q=query, subreddit=location, stickied=sticky, after=day_num)
    
    subreddits = []
    post_ids = []
    authors = []
    post_list = []

    for post in posts:
        if not connect.post_exists(post['id']):
            print("Preparing new Post.")
            sanitext = sanitize.sanitize_text(post['selftext'])
            coins = coin_wallet.match_coins(sanitext)
            
            subreddits.append((post['subreddit_id'], post['subreddit']))
            post_ids.append(post['id'])
            authors.append((post['author_fullname'], post['author']))
            post_list.append(
                (post['id'], 
                post['title'], 
                post['author_fullname'], 
                coins,
                post['subreddit_id'],
                datetime.fromtimestamp(post['created_utc']),
                sanitext))
    
    connect.insert_row('subreddits', subreddits)
    connect.insert_row('authors', authors)
    connect.insert_row('submissions', post_list)
    
    return post_ids


def get_comment_ids(post_ids):
    """
    Takes a list of post_ids and returns all comment_ids using Pushshift API

    Args:
        post_ids (list) - list of reddit post_ids
    
    Returns:
        comments (list) - list of comment ids associated with the post_ids
    """
    comments = []
    api = PushshiftAPI()
    print("Obtaining comment IDs")
    for post_id in post_ids:
        comments += api.search_submission_comment_ids(post_id)
    return comments

def get_new_comments(comment_ids):
    authors = []
    comments = []

    for comment_id in comment_ids:
        print("Preparing new Comment.")
        comment = reddit.comment(id=comment_id)
        sanitext = sanitize.sanitize_text(comment.body)
        coins = coin_wallet.match_coins(sanitext)

        authors.append((comment.author.id, comment.author.name))
        comments.append(
            (comment.id,
            datetime.fromtimestamp(comment.created_utc),
            comment.parent_id,
            comment.score,
            sanitext,
            datetime.utcnow(),
            comment.submission.id,
            comment.author.id,
            coins
            )
        )
    
    connect.insert_row('authors', authors)
    connect.insert_row('comments', comments)


if __name__ == '__main__':
    reddit = praw.Reddit('coinbot', user_agent = 'cryptoscraper bot')  # praw.ini for 'coinbot' initialization parameters
    coin_wallet = wallet.Wallet(1000)
    new_post_ids = get_new_posts('daily', 'CryptoCurrency', 2, True)
    comment_ids = get_comment_ids(new_post_ids)
    get_new_comments(comment_ids)