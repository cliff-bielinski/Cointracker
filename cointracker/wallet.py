import math
import requests

class Wallet:
    """
    a class that represents a collection of cryptocurrencies
    """

    def __init__(self, size):
        """
        initializes an instance of wallet with size (int) number of coins in it
        
        Args:
            size (int) - number of coins (sorted by market capitalization) in the wallet
        """
        self._size = size
        self._coin_list = self._get_coins(self._size)
        self._coin_dict = self._fill_wallet(self._coin_list)

    def _get_coins(self, num_coins):
        """
        Returns a list of coin objects sorted by market cap using by calling coingecko API
        Read more: https://www.coingecko.com/en/api/documentation

        Args:
            num_coins (int) - the number of coins to return sorted by market cap

        Returns:
            A list of coin objects
        """
        min_requestable_pages = math.ceil(num_coins / 250)
        results_per_page = math.ceil(num_coins / min_requestable_pages)
        
        coins = []
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc'
        
        # iterates through a paginated API response to get all coins
        for page_number in range(min_requestable_pages):
            response = requests.get(url + f'&per_page={results_per_page}&page={page_number+1}').json() 
            if response:
                coins += response
            else:
                break
        
        # truncates excess coins from API call
        remainder = len(coins) - num_coins
        
        if remainder > 0:
            coins = coins[:-remainder]
        
        return coins    
    
    def _fill_wallet(self, coin_list):
        """takes a list of coin objects in the wallet and maps cryptocurrency names and symbols to coin IDs"""
        coin_dictionary = {}

        for coin in coin_list:
            coin_dictionary[coin['id'].lower()] = coin['id']
            coin_dictionary[coin['symbol'].lower()] = coin['id']
            coin_dictionary[coin['name'].lower()] = coin['id']

        whitelist = self._get_whitelist()
        
        for word in whitelist:
            if word in coin_dictionary:
                del coin_dictionary[word]

        return coin_dictionary

    def _get_whitelist(self):
        """creates a list of words to be whitelisted from a textfile"""
        file = open('whitelist.txt', 'r')
        content = [line.rstrip() for line in file.readlines()]
        file.close()
        return content
    
    def show_wallet(self):
        """returns a dictionary of cryptocurrency in the wallet with coin names and coin symbols mapped to coin id"""
        return self._coin_dict
    
    def match_coins(self, tokenized_comment):
        """
        returns a set of coins found in a list of words

        Args:
            comment (list) - list of words from a tokenized comment

        Returns:
            a set of coin IDs
        """
        matches = set()
        
        for word in tokenized_comment:
            if word in self._coin_dict:
                matches.add(self._coin_dict[word])

        return list(matches)