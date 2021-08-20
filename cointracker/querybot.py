import praw
import requests
import math

def get_comments(reddit, subreddit, submission_num):
    """
    returns a list of comment objects using the Reddit API
    submission_num is an integer for the number of submissions to take comments from (sorted by "Hot")
    """
    comments = []

    for submission in reddit.subreddit(subreddit).hot(limit = submission_num):
        submission.comments.replace_more(limit=None) # flattens comment tree without limit
        for comment in submission.comments.list():
            comments.append(comment)
    
    return comments

def get_coin_list(num_coins):
    """
    Returns a list of coin objects sorted by market cap using by calling coingecko API
    Read more: https://www.coingecko.com/en/api/documentation
    """
    pages = math.ceil(num_coins / 250)
    remainder = num_coins % 250
    coins = []
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc'
    
    # iterates through a paginated API response to get all coins
    for page in range(1, pages + 1):
        coins += requests.get(url + f'&per_page=250&page={page}').json()
    
    # truncates excess coins from API call
    if remainder != 0:
        coins = coins[:-(250-remainder)]
    
    return coins    

def make_coin_dict(coin_list):
    """takes a list of coin objects and returns a map of cryptocurrency names and symbols to coin IDs"""
    coin_dictionary = {}

    for coin in coin_list:
        coin_dictionary[coin['id'].lower()] = coin['id']
        coin_dictionary[coin['symbol'].lower()] = coin['id']
        coin_dictionary[coin['name'].lower()] = coin['id']

    return coin_dictionary


if __name__ == '__main__':
    reddit = praw.Reddit('coinbot', user_agent = 'cryptoscraper bot')
    coin_reference = make_coin_dict(get_coin_list(1000))
    comment_list = get_comments(reddit, 'MUD', 1)
    

# for comment in comment_list:
#     print("Time:", comment.created_utc)
#     print("ID:", comment.id)
#     print("Parent_ID:", comment.parent_id)
#     print("Link_ID:", comment.link_id)
#     print("Subreddit_ID:", comment.subreddit_id)
#     print("Author:", comment.author.name)
#     print("Author_ID:", comment.author.id)
#     print("Score:", comment.score)
#     print("Comment:", comment.body)
