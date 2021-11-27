from config.config import config
from datetime import datetime, timedelta
from pmaw import PushshiftAPI
from sanitize import TextProcessing
import connect
import requests
import requests.auth
import wallet


class Reddit:
    """
    a class to represent an instance of reddit
    
    Args:
        name (str) - name of the reddit bot
        config_file (str) - file name that holds the reddit bot's configuration
    
    Attributes:
        name (str) - name of the reddit bot
        _bot (dict) - config details of reddit bot including CLIENT_ID and SECRET_KEY
        _auth_token (dict) - oauth access token to be included in API requests
        _pushshift (obj) - instance of Pushshift API
        _post_ids (list) - list of post_id strings from most recent query
        _comment_ids (list) - list of comment_id strings from most recent query
        _subreddits (list) - list of subreddit tuples in queue for insertion to db
        _authors (list) - list of author tuples in queue for insertion to db
        _posts (list) - list of post tuples in queue for insertion to db
        _comments (list) - list of comment tuples in queue for insertion to db
    """

    def __init__(self, name, config_file):
        """Constructs an instance of a Reddit object with necessary attributes"""
        self.name = name
        self._bot = config(name, config_file)
        self._auth_token = self._authorize(self._bot)
        self._pushshift = PushshiftAPI()
        self._post_ids = []
        self._comment_ids = []
        self._subreddits = []
        self._authors = []
        self._posts = []
        self._comments = []
    
    def _authorize(self, params):
        """returns oauth access token for reddit API"""
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
    
    def _call_api(self, id_chunk):
        """
        calls Reddit API and returns json response object
        
        Args:
            id_chunk (str) = a string of ids (comment, post, or subreddit) separated by commas with which to query Reddit API

        Returns:
            JSON response object which holds the results of the Reddit API call
        """
        response = requests.get(f'https://oauth.reddit.com/api/info/?id={id_chunk}', headers=self._auth_token)
        return response.json()['data']['children']

    def _convert_time(self, days):
        """provides the epoch time for (integer) days ago"""
        return int((datetime.today() - timedelta(days=days)).timestamp())

    def _db_write(self, **kwargs):
        """
        writes to postgreSQL db
        
        Args:
            kwargs** (key-value pairs) = table name : data to insert in table
        """
        for key, value in kwargs.items():
            connect.insert_row(f'{key}', value)

    def _parse_comments(self, comments, wallet):
        """add comments into the queue to be inserted into the db
        Args:
            comments (list) - list of comment JSON response objects from the Reddit API
            wallet (obj) - a Wallet object which holds a map of cryptocurrencies and their names/symbols
        """
        counter = 1
        for comment in comments:
            if comment['data']['author'] == '[deleted]': # skip over deleted comments
                continue
            
            print('Preparing comment for the queue...')
            text = TextProcessing.sanitize_text(comment['data']['body'])
            coins = wallet.match_coins(text)

            self._authors.append((comment['data']['author_fullname'], comment['data']['author']))
            self._comments.append((
                't1_' + comment['data']['id'],
                datetime.fromtimestamp(comment['data']['created_utc']),
                comment['data']['parent_id'],
                comment['data']['score'],
                text,
                datetime.utcnow(),
                comment['data']['link_id'],
                comment['data']['author_fullname'],
                coins
            ))

            counter += 1
            print(f'{counter} comments added to the queue.')


    def clear_comments(self):
        """clears list of comment_ids from object"""
        self._comment_ids.clear()

    def clear_posts(self):
        """clears list of post_ids from object"""
        self._post_ids.clear()

    def get_posts(self, query, subreddit, days, wallet, sticky=False):
        """
        Requests pushshift submission objects per search query, prepares and uploads submission response data into db
        and then returns a list of post_ids

        Args:
            query (str) - search term(s)
            subreddit (str) - subreddit to search
            days (int) - timeframe to limit search query (e.g. 10 for posts in past 10 days)
            sticky (bool) - whether to limit search to stickied posts
            wallet (obj) - a Wallet object that contains cryptocurrency

        Return:
            post_ids (list) - list of post_ids whose submission data was returned from pushshift call
        """
        posts = self._pushshift.search_submissions(q=query, subreddit=subreddit, after=self._convert_time(days), stickied=sticky)

        for post in posts:
            # if the post is not in the DB, add post data to insertion queue in tuple form
            if not connect.post_exists(post['id']):
                print("Preparing new Post...")
                text = TextProcessing.sanitize_text(post['selftext'])
                print("Finding coins...")
                coins = wallet.match_coins(text)

                self._post_ids.append(post['id'])
                self._subreddits.append((post['subreddit_id'], post['subreddit']))
                self._authors.append((post['author_fullname'], post['author']))
                self._posts.append(
                    ('t3_' + post['id'], 
                    post['title'], 
                    post['author_fullname'], 
                    coins,
                    post['subreddit_id'],
                    datetime.fromtimestamp(post['created_utc']),
                    text))
    
        # batch insert the queued data to their respective tables
        self._db_write(subreddits=self._subreddits, authors=self._authors, submissions=self._posts)

    def get_comment_ids_from_posts(self, clear=False, posts=None):
        """
        adds a list of all comment IDs for a given list of post IDs using Pushshift API
        
        Args:
            clear (bool) = (optional) if True turns the self._post_ids into an empty list after pulling comments from it
            posts (list) = (optional) pass a list of post_ids as part of API query instead of default self._post_ids
        """
        post_ids = self._post_ids if posts is None else posts
        print("Obtaining comment IDs...")

        for post_id in post_ids:
            self._comment_ids += self._pushshift.search_submission_comment_ids(ids=post_id)
        
        print(f'{len(self._comment_ids)} comments added to the list.')

        if clear: self.clear_posts()
    
    def get_comments(self, wallet, clear=False, comment_id_list=None):
        """
        returns a list of comment JSON response objects from the Reddit API

        Args:
            wallet (obj) = a Wallet object that contains a map of cryptocurrencies and crypto symbols
            clear (bool) = (optional) if True turns self._comment_ids into an empty list after executing method
            comment_id_list (list) = (optional) pass a list of comment_ids as part of the API query instead of using self._comment_ids
        """
        batch = ''
        
        comment_ids = self._comment_ids if comment_id_list is None else comment_id_list
        comments = []

        for i in range(len(comment_ids)):
            if i == 0:
                batch = f't1_{comment_ids[i]}'

            elif i % 100 == 0:
                comments += self._call_api(batch)
                print(f'{len(comments)} out of {len(comment_ids)} comments obtained.')
                batch = f't1_{comment_ids[i]}'

            else:
                batch += f',t1_{comment_ids[i]}'
        
        comments += self._call_api(batch)
        print(f'{len(comments)} comments obtained.')
        
        self._parse_comments(comments, wallet)

        print('Writing comments to database...')
        self._db_write(authors=self._authors, comments=self._comments)

        if clear: self.clear_comments()