from flask import Flask, render_template
from flask import Flask
from flask import render_template, jsonify
from main import stream_tweets, translate
from classifier import classifier
import json


app = Flask(__name__)

# json files location
RAW_TWEETS_JSON = "/raw.json"
TRANSLATED_TWEETS_JSON = "/translated.json"
SENTIMENTS_JSON = "/sentiments.json"
METADATA_JSON = "/metatdata.json"


@app.route("/")
def main():
    return "Welcome!"


def process(raw_file):
    raw_json = json.loads(raw_file)
    translate(raw_json)


@app.route("/tweets")
def get_data():
    metadata_result = {}
    translatedTweets = {}
    rawTweets = {}

    with open("metadata.json", "r") as f:
        metadata_result = json.loads(f.read())

    with open("translated.json", "r") as f:
        translatedTweets = json.loads(f.read())

    with open("raw.json", "r") as f:
        rawTweets = json.loads(f.read())

    positiveCount = metadata_result.get("positive_count")
    neutralCount = metadata_result.get("neutral_count")
    negativeCount = metadata_result.get("negative_count")
    tweetIds = rawTweets.keys()
    tweetTotal = positiveCount + neutralCount + negativeCount

    return render_template(
        "index.html",
        positiveCount=positiveCount,
        neutralCount=neutralCount,
        negativeCount=negativeCount,
        tweetTotal=tweetTotal,
        tweetIds=tweetIds,
        translatedTweets=translatedTweets,
        rawTweets=rawTweets,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
