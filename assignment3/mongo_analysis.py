#!/usr/bin/env python

import pymongo
import bson.code
import bson.json_util

import prague_tweets

mongo_url = "mongodb://localhost:27017"
mongo_db_name = "w205_assignment3"
mongo_collection_name = "prague_tweets"

mongo_count_reducer = """
    function (key, values) {
        var total = 0;
        for (var i = 0; i < values.length; i++) {
            total += values[i];
        }
        return total;
    }
"""

mongo_hashtag_mapper = """
    function () {
        this.hashtags.forEach(function(hashtag) {
            emit(hashtag.toLowerCase(), 1);
        });
    }
"""

mongo_screenname_mapper = """
    function () {
        emit(this.screen_name, 1)
    }
"""

mongo_hour_mapper = """
    function () {
        var date = new Date(this.created_at)
        var hour_cet = (date.getUTCHours() + 1) % 24
        emit(hour_cet, 1)
    }
"""


def load_data(tweet_collection):
    tweet_collection.insert(transform_json(prague_tweets.tweets()))


def transform_json(tweets):
    for tweet in tweets:
        yield {
            'created_at': prague_tweets.string_to_datetime(tweet[u'created_at']),
            'screen_name': tweet[u'user'][u'screen_name'],
            'hashtags': [hashtag[u'text'] for hashtag in tweet[u'entities'][u'hashtags']]
        }


count_reducer = bson.code.Code(mongo_count_reducer)


def count_hashtags(tweet_collection, limit=10):
    hashtag_mapper = bson.code.Code(mongo_hashtag_mapper)
    counts = tweet_collection.map_reduce(hashtag_mapper, count_reducer, "hastag_counts") \
        .find().sort(u'value', -1).limit(limit)
    return map(lambda count: (count[u'_id'], int(count[u'value'])), counts)


def count_tweets(tweet_collection, limit=1):
    screenname_mapper = bson.code.Code(mongo_screenname_mapper)
    counts = tweet_collection.map_reduce(screenname_mapper, count_reducer, "tweet_counts")\
        .find().sort(u'value', -1).limit(limit)
    return map(lambda count: (count[u'_id'], int(count[u'value'])), counts)


def count_hours(tweet_collection, start_hour_cet=0, end_hour_cet=24):
    query = {'$and': [{'_id': {'$gte': start_hour_cet}}, {'_id': {'$lte': end_hour_cet}}]}
    hours_mapper = bson.code.Code(mongo_hour_mapper)
    counts = tweet_collection.map_reduce(hours_mapper, count_reducer, "hour_counts")\
        .find(query).sort(u'_id', 1)
    return map(lambda count: ("%02d:00+0100" % count[u'_id'], int(count[u'value'])), counts)


if __name__ == '__main__':

    client = pymongo.MongoClient(mongo_url)
    try:
        client.drop_database(mongo_db_name)
        db = client[mongo_db_name]
        collection = db[mongo_collection_name]

        load_data(collection)

        print "\n### top tweeter"
        count_tweets(collection)
        for (key, value) in count_tweets(collection, 1):
            print key, value
        print "\n### top 10 hashtags"
        for key, value in count_hashtags(collection, 10):
            print key, value
        print "\n### tweets by hour"
        for (key, value) in count_hours(collection, 9, 16):
            print key, value

    finally:
        client.close()
