import os
import json
import tweepy
import pandas as pd
from textblob import TextBlob
from dotenv import load_dotenv
from classify_sentences import classify
import json

# load environmental variables
load_dotenv()


def stream_tweets(tweet_count=100, language="hi", query="#construction"):
    """Function which stream tweets

    Parameters:
        tweet_count (int): Specifies number of tweets to stream
        languagre (str): Specifies the language tweet shoudl be streamed in
        query (str): phrase/hashtage to be streamed

    Returns
        Dictionary: 'id': tweets
    """

    # Get Environmental variables from dotenv file
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_secret = os.getenv("ACCESS_SECRET")
    text_query = query
    count = tweet_count
    tweets = {}

    # authenticating api keys
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)

    # searching for tweets with hashtag #construction
    try:
        api = tweepy.API(auth)
        for i in tweepy.Cursor(
            api.search, q=text_query, lang=language, tweet_mode="extended"
        ).items(count):
            tweets[i.id] = i.full_text

    except Exception as e:
        print("Error ", e)

    return tweets


def raw_json():
    """Function to save tweets output to .json object

    Parameters:
        tweets(str): streamed tweets

    returns:
        raw.json file containing streamed tweets
    """
    tweets = stream_tweets()

    with open("raw.json", "w") as f:
        json.dump(tweets, f)


def translate(input_json="raw.json", language="en"):
    """Function that converts tweets from specified language to English

    Parameters:
        input_json(json object): saved .json object containing streamed tweets.

    Returns:
        String of tweets converted to english
    """
    input_ = input_json
    translated_tweets = {}

    try:  # loading the raw.json file
        with open(input_, "r") as raw_tweets:
            input_data = json.loads(raw_tweets.read())
            input_tweet = input_data

        for i_d, full_text in input_tweet.items():
            translated_tweets[i_d] = str(
                TextBlob(full_text).translate(from_lang="hi", to=language)
            )

    except Exception as e:
        print("Error -> ", e)

    return translated_tweets


def translate_json(translated_tweets):
    """Function to save translated tweets output to .json object

    Parameters:
        tweets(str): streamed tweets

    returns:
        translated.json file containing translated tweets
    """
    translated_tweets = translate()

    with open("translated.json", "w") as f:
        json.dump(translated_tweets, f)


def make_metadata(translated_tweets):
    """Function to compile data about streamed tweets after classifcation

    Parameters:
        translated tweets(dict) : streamed tweets after translation

    Retruns:
        .json file with metadata of streamed tweets
    """
    translated_tweets = translate()
    no_positive = 0
    no_negative = 0
    no_neutral = 0

    for translated_tweet in translated_tweets:
        sentiment = classify(translated_tweet)
        if sentiment == "postive":
            no_positive = no_positive + 1
        elif sentiment == "negative":
            no_negative = no_negative + 1
        elif sentiment == "neutral":
            no_neutral = no_neutral + 1

    metadata = {
        "positive_count": no_positive,
        "negative_count": no_negative,
        "neutral_count": no_neutral,
    }
    with open("metadata.json", "w") as f:
        json.dump(metadata, f)


def process_tweets():
    raw_json()
    translated_tweets = translate()
    translate_json(translated_tweets)
    make_metadata(translated_tweets)
