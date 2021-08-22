import praw
import wallet

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

    for submission in reddit.subreddit(subreddit).hot(limit = submission_num):
        submission.comments.replace_more(limit=None) # flattens comment tree without limit
        for comment in submission.comments.list():
            comments.append(comment)
    
    return comments

if __name__ == '__main__':
    reddit = praw.Reddit('coinbot', user_agent = 'cryptoscraper bot')
    coin_wallet = wallet.Wallet(1000)
    comment_list = get_comments(reddit, 'MUD', 1)
    

# for comment in comment_list:
#     print("Time:", comment.created_utc)
#     print("ID:", comment.id)
#     print("Parent_ID:", comment.parent_id)
#     print("Post_ID:", comment.link_id)
#     print("Submission_title:", comment.submission.title)
#     print("Submission Author:", comment.submission.author.id)
#     print("Subreddit_ID:", comment.subreddit_id)
#     print("Author:", comment.author.name)
#     print("Author_ID:", comment.author.id)
#     print("Score:", comment.score)
#     print("Comment:", comment.body)
