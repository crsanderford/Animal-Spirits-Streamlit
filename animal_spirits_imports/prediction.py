"""process tweets and produce predictions"""

import pandas as pd
from joblib import load

import re
import string

#from .text_functions import *

def clean_text(text): 
    """Clean our tweets using regex. Remove weird characters and links."""
    cleanedup = text.lower()
    return re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", cleanedup)

process_pipe = load('process_pipe')
ESVM = load('ESVM')

def score_tweet(tweet):
    clean_tweet = clean_text(tweet)
    tweet_processed = process_pipe.transform([clean_tweet])
    predicted = ESVM.predict(tweet_processed)
    return int(predicted[0])