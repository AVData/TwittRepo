import tweepy
import basilica
from decouple import config
from twitoff.models import DB, Tweet, User


TWITTER_USERS = ['elonmusk',
                 'nasa',
                 'google',
                 'heavyweight',
                 'sentientcells',
                 'spotify',
                 'championsleague',
                 'replyall',
                 'thisamerlife']

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_API_KEY'),
                                   config('TWITTER_CONSUMER_API_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)
BASILICA = basilica.Connection(config('BASILICA_KEY'))


def add_or_update_user(name):
    '''
    Adds or updates user and their tweets.
    Returns error if user doesn't exist or is private.
    '''
    try:
        # Gets user through tweepy API
        twitter_user = TWITTER.get_user(name)

        # Adds db_user to user table
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id,
                        name=name))
        DB.session.add(db_user)

        # adds recent non-retweet/reply tweets
        # twitter API has a limit of 200 per request
        tweets = twitter_user.timeline(count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       tweet_mode='extended',
                                       since_id=db_user.newest_tweet_id)

        # Includes additional user info to User table in our database
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # looping over tweets
        for tweet in tweets:

            # as Bruno states, we need to get basilica embedding for each tweet
            embedding = BASILICA.embed_sentence(tweet.full_text,
                                                model='twitter')

            # Adds tweet info to Tweets table
            db_tweet = Tweet(id=tweet.id,
                             text=tweet.full_text[:300],
                             embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print(f'Encountered error while processing {name}: {e}')
        raise e
    else:
        DB.session.commit()

def add_default_users(users=TWITTER_USERS):
    for user in users:
        add_or_update_user(user)

def update_all_users():
    for user in User.query.all():
        add_or_update_user(user.name)
