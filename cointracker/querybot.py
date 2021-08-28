import praw
import wallet
import sanitize
from datetime import datetime
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
    """returns map of comment metadata"""
    comment_map = {
        'id':comment.id, 
        'time':datetime.fromtimestamp(comment.created_utc),
        'parent':comment.parent_id,
        'score':comment.score,
        'body':sanitized_text,
        'pulled':datetime.utcnow(),
        'post':comment.submission.id,
        'author':comment.author.id,
        'coin':coin_matches,
    }
    return comment_map

def prepare_subreddit(comment):
    """returns map of subreddit metadata"""
    subreddit_map = {
        'subreddit_id':comment.subreddit.id,
        'subreddit_name':comment.subreddit.display_name
    }
    return subreddit_map

def prepare_author(comment):
    """returns map of author metadata"""
    author_map = {
        'author_id':comment.author.id,
        'author_name':comment.author.name
    }
    return author_map

def prepare_submission(comment, sanitized_text, coin_matches=None):
    """returns map of submission metadata"""
    submission_map = {
        'id':submission.id,
        'time':datetime.fromtimestamp(submission.created_utc),
        'name':submission.title,
        'author':comment.author.id,
        'body':sanitized_text,
        'coin':coin_matches,
        'subreddit_id':submission.subreddit.id 
    }
    return submission_map

if __name__ == '__main__':
    reddit = praw.Reddit('coinbot', user_agent = 'cryptoscraper bot')  # praw.ini for 'coinbot' initialization parameters
    coin_wallet = wallet.Wallet(1000)
    comment_list, submission_list = get_comments(reddit, 'MUD', 1)

    new_subreddits = []
    new_authors = []
    new_posts = []
    new_comments = []

    # prepares and inserts data from every submission returned from api call into the db
    for submission in submission_list:
        
        # skips over deleted submission
        if submission.author is None: continue

        sanitized_submission = sanitize.sanitize_text(submission.selftext)
        submission_coins = list(coin_wallet.match_coins(sanitized_submission))
        
        new_subreddits.append(prepare_subreddit(submission))
        new_authors.append(prepare_author(submission))
        new_posts.append(prepare_submission(submission, sanitized_submission, submission_coins))

    # prepares and inserts data from every comment returned from api call into the db
    for comment in comment_list:

        # skips over deleted comments
        if comment.author is None: continue

        sanitized_comment = sanitize.sanitize_text(comment.body)
        mentioned_coins = list(coin_wallet.match_coins(sanitized_comment))
        new_authors.append(prepare_author(comment))
        new_comments.append(prepare_comment(comment, sanitized_comment, mentioned_coins))
        
            
    connect.insert_row('subreddits', new_subreddits)
    connect.insert_row('authors', new_authors)
    connect.insert_row('submissions', new_posts)
    connect.insert_row('comments', new_comments)

