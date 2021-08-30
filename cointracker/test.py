from pmaw import PushshiftAPI
from datetime import datetime, timedelta
from config.config import config
import sanitize
import praw
import requests
import requests.auth

class Reddit:
    def __init__(self, name, config_file):
        self.name = name
        self._bot = config(name, config_file)
        self._access_token = _set_oauth_token(self._bot)

    def _set_oauth_token(self, params):
        url = 'https://www.reddit.com/api/v1/access_token'
        data = {
            'grant_type': 'password',
            'username': params['username'],
            'password': params['password']
            }
        headers = {'User-Agent': f'{self.name}'}
        auth = requests.auth.HTTPBasicAuth(params['client_id'], params['client_secret'])
        request = requests.post(url,
                                data=data,
                                headers=headers,
                                auth=auth)
        token = request.json()['access_token']
        headers['Authorization'] = f'bearer {token}'
        return headers

    def get_name(self):
        return self.name


account = config('coinbot', 'praw.ini')

def get_odsaauth_token(params):
    url = 'https://www.reddit.com/api/v1/access_token'
    data = {
        'grant_type': 'password',
        'username': params['username'],
        'password': params['password']
        }
    headers = {'User-Agent': 'CryptoBot by cointrackerpraw'}
    auth = requests.auth.HTTPBasicAuth(params['client_id'], params['client_secret'])
    request = requests.post(url,
                            data=data,
                            headers=headers,
                            auth=auth)
    token = request.json()['access_token']
    headers['Authorization'] = f'bearer {token}'
    return headers

def get_comments(subreddit, ids, token):
    response = requests.get('https://oauth.reddit.com/r/cryptoCurrency/api/info?id=t1_hamfrqo,t1_hamfrrk', headers=token)
    return response.json()

