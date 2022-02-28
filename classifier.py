import json
import sklearn.linear_model.logistic
from classify_sentences import classify
from main import translate


def classifier(input_json="translated.json"):
    """
    Classifies the tweets and determines the sentiment

    """

    # Create a Dict that stores the outputs of the Sentiments
    input = input_json
    classified_result = {}
    positive_no = 0
    negative_no = 0
    neutral_no = 0

    try:
        with open(input, "rb") as input_data:
            translated_tweet = json.load(input_data)

    except Exception as e:
        print("Error - Could not load file", e)

    for id, full_text in translated_tweet.items():
        classified_result[id] = classify(full_text)

        if classified_result == "positive":
            positive_no += 1
        else:
            return 0
        if classified_result == "negative":
            negative_no += 1
        else:
            return 0
        if classified_result == "neutral":
            neutral_no += 1
        else:
            return 0

    with open("classified.json", "w") as f:
        json_object = json.dumps(classified_result, f, indent=4)


def Metadata():
    positive_no = 0
    negative_no = 0
    neutral_no = 0

    translated_tweets_ = translate()
    metadata_json = {"tweetCount": len(translated_tweets_)}
    metadata_json["sentiments"] = {
        "positive#": positive_no,
        "negative#": negative_no,
        "neutral#": neutral_no,
    }
    with open("metadata.json", "w") as f:
        meta_dump = json.dumps(metadata_json, f, indent=4)
