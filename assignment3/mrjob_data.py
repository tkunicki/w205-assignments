#!/usr/bin/env python

import prague_tweets


def transform_data():
    with open('mrjob.txt', 'wb') as writer:
        for tweet in prague_tweets.tweets():
            record = [
                prague_tweets.string_to_datetime(tweet[u'created_at']).isoformat() + 'Z',
                tweet[u'user'][u'screen_name'],
            ]
            record += [hashtag[u'text'] for hashtag in tweet[u'entities'][u'hashtags']]
            writer.write(','.join(record) + '\n')

if __name__ == '__main__':
    transform_data()