"""retrieve tweets, score and store them."""
import tweepy
from decouple import config
from animal_spirits_imports.dbmodels import *
from animal_spirits_imports.prediction import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

import psycopg2



# Create engine
db_uri = config('DATABASE_URL')
engine = create_engine(db_uri, echo=True)
Session = sessionmaker(bind=engine)

# Create All Tables
Tweet.metadata.create_all(engine)
IndicatorRecord.metadata.create_all(engine)

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
API = tweepy.API(TWITTER_AUTH, wait_on_rate_limit=True)

#newest_tweet_id = 0

def insert_tweets(quantity):
    "add tweets to the database"

    session = Session()
    
    # setting a value for the most recent tweet
    try:
        newest_tweet_id = session.query(func.max(Tweet.id)).scalar()
    except:
        newest_tweet_id = 0


    # pulling in a set of tweets based on the most recent tweet
    try:
        search_term = "#btc -filter:retweets"
        tweets = tweepy.Cursor(API.search,
                    q=search_term,
                    tweet_mode='extended',
                    lang="en",
                    since_id=newest_tweet_id).items(quantity)
        
        """if tweets:
            newest_tweet_id = tweets[0].id"""
        
        for tweet in tweets:
            
            db_tweet = Tweet(
                id = tweet.id,
             text = clean_text(tweet.full_text),
              sentiment = score_tweet(clean_text(tweet.full_text))
              )
            session.add(db_tweet)

    except Exception as e:
        print(f'Error processing: {e}')
        raise e

    else:
        session.commit()
        session.close()

def delete_tweets():
    """deletes oldest tweets from database if nearing capacity."""

    session = Session()

    # get a count of tweets in the DB
    tweetcount = session.query(func.count(Tweet.id)).scalar()
    print(tweetcount)

    # if the number of tweets exceeds a threshold:
    if tweetcount >= 8950:
        # get the oldest tweets;
        oldest_thousand = session.query(Tweet).order_by(Tweet.id).limit(1000)
        # find the id of the newest among them;
        last_entry = oldest_thousand[-1].id
        print(last_entry)
        # and delete everything at or below that id.
        to_delete = session.query(Tweet).filter(Tweet.id <= last_entry)
        to_delete.delete(synchronize_session=False)

    session.commit()
    session.close()

def insert_indicator_record(value_to_insert, time_to_insert):
    "add an indicator record to the database"

    session = Session()


    # pulling in a set of tweets based on the most recent tweet
    try:
        db_record = IndicatorRecord(
            time_generated=time_to_insert,
            indicator_value=value_to_insert)
        session.add(db_record)

    except Exception as e:
        print(f'Error processing: {e}')
        raise e

    else:
        session.commit()
        session.close()

def delete_indicator_records():
    """deletes oldest tweets from database if nearing capacity."""

    session = Session()

    # get a count of tweets in the DB
    recordcount = session.query(func.count(IndicatorRecord.time_generated)).scalar()
    print(recordcount)

    # if the number of tweets exceeds a threshold:
    if recordcount >= 975:
        # get the oldest records;
        oldest_twentyfive = session.query(IndicatorRecord).order_by(IndicatorRecord.time_generated).limit(25)
        # find the id of the newest among them;
        last_entry = oldest_twentyfive[-1].time_generated
        print(last_entry)
        # and delete everything at or below that id.
        to_delete = session.query(IndicatorRecord).filter(IndicatorRecord.time_generated <= last_entry)
        to_delete.delete(synchronize_session=False)

    session.commit()
    session.close()


