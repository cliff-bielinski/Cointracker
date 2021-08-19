import praw

# initializes an instance of Reddit using Python Reddit API wrapper
reddit = praw.Reddit('coinbot', user_agent='cryptoscraper bot')

comment_list = []

# iterates through the hottest submission of the subreddit and adds every comment object to a list
for submission in reddit.subreddit("MUD").hot(limit=1):
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        comment_list.append(comment)

for comment in comment_list:
    print("Time:", comment.created_utc)
    print("ID:", comment.id)
    print("Parent_ID:", comment.parent_id)
    print("Link_ID:", comment.link_id)
    print("Subreddit_ID:", comment.subreddit_id)
    print("Author:", comment.author.name)
    print("Author_ID:", comment.author.id)
    print("Score:", comment.score)
    print("Comment:", comment.body)
    print()