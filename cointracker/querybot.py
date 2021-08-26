import praw
import wallet
import sanitize
from datetime import datetime, timezone
import connect

def get_comments(reddit, subreddit, submission_num):
    """
    returns a list of comment objects using the Reddit API

    Args:
        reddit (obj) - PRAW reddit instance
        subreddit (str) - name of subreddit to return comments from
        submission_num (int) - number of submission posts to return comments from in subreddit (sorted by 'Hot')

    Returns:
        A list of comment objects 
    """
    comments = []
    submissions = []

    # creates a list of all comment objects for every submission returned from the API call
    for submission in reddit.subreddit(subreddit).hot(limit = submission_num):
        submissions.append(submission)
        submission.comments.replace_more(limit=None) # flattens comment tree
        for comment in submission.comments.list():
            comments.append(comment)
    
    return comments, submissions

def prepare_comment(comment, sanitized_text, coin_matches=None):
    comment_map = {
        'id':comment.id, 
        'time':datetime.fromtimestamp(comment.created_utc),
        'parent':comment.parent_id,
        'score':comment.score,
        'body': sanitized_text,
        'pulled':datetime.utcnow(),
        'post':comment.link_id,
        'author':comment.author.id,
        'coin': coin_matches,
    }
    return comment_map

def prepare_subreddit(comment):
    subreddit_map = {
        'subreddit_id': comment.subreddit_id,
        'subreddit_name:': comment.subreddit.display_name
    }
    return subreddit_map

def prepare_author(comment):
    author_map = {
        'author_id':comment.author.id,
        'author_name':comment.redditor.name
    }
    return author_map

def prepare_submission(comment, sanitized_text, coin_matches=None):
    submission_map = {
        'id':submission.id,
        'time':datetime.fromtimestamp(submission.created_utc),
        'name':submission.title,
        'author':comment.author.id,
        'body':sanitized_text,
        'coin': coin_matches,
        'subreddit_id': submission.subreddit.id 
    }
    return submission_map

if __name__ == '__main__':
    reddit = praw.Reddit('coinbot', user_agent = 'cryptoscraper bot')  # praw.ini for 'coinbot' initialization parameters
    coin_wallet = wallet.Wallet(1000)
    comment_list, submission_list = get_comments(reddit, 'MUD', 1)

    for submission in submission_list:
        sanitized_submission = sanitize.sanitize_text(submission.selftext)
        submission_coins = list(coin_wallet.match_coins(sanitized_submission))
        prepared_submission = prepare_submission(submission, sanitized_submission, submission_coins)

    for comment in comment_list:
        sanitized_comment = sanitize.sanitize_text(comment.body)
        mentioned_coins = list(coin_wallet.match_coins(sanitized_comment))
        prepared_comment = prepare_comment(comment, sanitized_comment, mentioned_coins)
        # connect.insert_subreddit(comment.subreddit_id, comment.subreddit.display_name)
        # connect.insert_row(prepared_comment, {'subreddit_id':'test_id3', 'subreddit_name':'ymp4life'})

