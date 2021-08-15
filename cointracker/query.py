import requests
from pprint import pprint

def request_data(data_type, coin, subreddit, timeframe, size):
    """
    Retrieves query data from pushshift API
    data_type can be 'comment' or 'submission'
    timeframe in 'value+s/m/h/d' (second, minute, hour, day) e.g. '30d' for past 30 days
    returns query results in JSON

    https://github.com/pushshift/api
    """

    search_params = {'q': coin, 'subreddit': subreddit, 'after': timeframe, 'size': size}
    url = "https://api.pushshift.io/reddit/search/{}/".format(data_type)

    data = requests.get(url, params=search_params)

    return data.json()
