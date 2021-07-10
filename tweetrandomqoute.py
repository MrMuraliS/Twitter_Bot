from time import sleep
import tweepy
from tweepy import OAuthHandler
from tweepy.error import RateLimitError, TweepError
import requests

from os import config
import time

# Authenticate to Twitter
access_token = config['Access_Token']
access_token_secret = config['Access_Token_Secret']
consumer_key = config['API_Key']
consumer_secret = config['API_secret_Key']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
print('Authenticated')

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# public_tweets = api.get_user('tarak9999')
# for user in public_tweets.friends(count=5):
#     print(user.screen_name)

# print(public_tweets.followers_count)
# print(public_tweets.friends_count)
# print(public_tweets.friends)

user = api.me()
# print(user.friends_count)

def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.RateLimitError:
        time.sleep(1000)
    except StopIteration:
        print('Done')


""" Randome qoute Tweet """

def random_qoute():
    i = 0
    while True:
        try:

            url = 'http://api.quotable.io/random'

            response = requests.get(url).json()
            content = response['content']
            author = response['author']
            tag = response['tags'][0]

            api.update_status(f'{content} #{tag}')
            # api.update_status(f'{content}  #{tag} \n\n ~~{author}')
            print(f'Qoute- {i+1} is tweeted')
            time.sleep(60 * 60)
        except TweepError as e:
            print(e.reason)
        except RateLimitError:
            time.sleep(1000)
        i += 1
    # print('All processed')

if __name__ == "__main__":
    random_qoute()