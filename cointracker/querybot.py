import reddit
import wallet

if __name__ == '__main__':
    session = reddit.Reddit('coinbot', 'praw.ini')
    coin_wallet = wallet.Wallet(1000)
    session.get_posts('daily', 'cryptocurrency', 2, coin_wallet, True)
    session.get_comment_ids_from_posts(True)
    session.get_comments(coin_wallet, True)
