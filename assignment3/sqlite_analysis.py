#!/usr/bin/env python

import sqlite3
import os
import os.path
import prague_tweets


sqlite3_db_name = "w250-assignment3.db"

sqlite3_tweets_create = """
CREATE TABLE tweets (
    id INTEGER NOT NULL UNIQUE,
    screen_name TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY(id)
);
"""

sqllite3_tweets_insert = """
INSERT INTO tweets (id, created_at, screen_name) VALUES(?, ?, ?);
"""

sqlite3_hashtags_create = """
CREATE TABLE hashtags (
    id INTEGER NOT NULL UNIQUE,
    tweet_id INTEGER NOT NULL,
    hashtag TEXT NOT NULL,
    PRIMARY KEY(id)
);
"""

sqllite3_hashtags_insert = """
INSERT INTO hashtags (id, tweet_id, hashtag) VALUES(?, ?, ?);
"""

sqlite3_hashtags_count = """
SELECT LOWER(hashtag) as hashtag_lower, COUNT(*) FROM hashtags GROUP BY hashtag_lower ORDER BY COUNT(*) DESC LIMIT %d;
"""

sqlite3_screenname_count = """
SELECT screen_name, COUNT(*) FROM tweets GROUP BY screen_name ORDER BY COUNT(*) DESC LIMIT %d;
"""

sqlite3_hours_count = """
SELECT (strftime('%H', created_at) + 1) % 24 AS hour_cet, COUNT(*)
FROM tweets
WHERE hour_cet >= ? AND hour_cet <= ?
GROUP BY hour_cet
ORDER BY hour_cet ASC;
"""


def create_schema(tweet_connection):
    tweet_connection.execute(sqlite3_tweets_create)
    tweet_connection.execute(sqlite3_hashtags_create)


def load_data(tweet_connection):
    tweet_id = 0
    hashtag_id = 0
    for tweet in prague_tweets.tweets():
        created_at = prague_tweets.string_to_datetime(tweet[u'created_at']).isoformat() + "Z"
        screen_name = tweet[u'user'][u'screen_name']
        tweet_connection.execute(sqllite3_tweets_insert, (tweet_id, created_at, screen_name))
        for entity in tweet[u'entities'][u'hashtags']:
            tweet_connection.execute(sqllite3_hashtags_insert, (hashtag_id, tweet_id, entity[u'text']))
            hashtag_id += 1
        tweet_id += 1
    tweet_connection.commit()


def count_hashtags(tweet_connection, limit=10):
    cursor = tweet_connection.cursor()
    cursor.execute(sqlite3_hashtags_count % limit)
    return map(lambda row: (row[0], row[1]), cursor.fetchall())


def count_tweets(tweet_connection, limit=1):
    cursor = tweet_connection.cursor()
    cursor.execute(sqlite3_screenname_count % limit)
    return map(lambda row: (row[0], row[1]), cursor.fetchall())


def count_hours(tweet_connection, start=9, end=16):
    cursor = tweet_connection.cursor()
    cursor.execute(sqlite3_hours_count, (start, end))
    return map(lambda row: ("%02d:00+0100" % row[0], row[1]), cursor.fetchall())


if __name__ == '__main__':

    if os.path.isfile(sqlite3_db_name):
        os.remove(sqlite3_db_name)

    connection = sqlite3.connect(sqlite3_db_name)

    try:
        create_schema(connection)
        load_data(connection)

        count_hashtags(connection)
        print "\n### top 10 hastags"
        for key, value in count_hashtags(connection, 10):
            print key, value

        print "\n### top tweeter"
        count_tweets(connection)
        for (key, value) in count_tweets(connection, 1):
            print key, value

        print "\n### tweets by hour"
        for (key, value) in count_hours(connection):
            print key, value

    finally:
        connection.close()
