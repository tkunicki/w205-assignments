#!/usr/bin/env python

import contextlib
import datetime
import json
import os.path
import urllib2

tweet_url_base =\
    "https://raw.githubusercontent.com/alexmilowski/data-science/master/assignments/organizing-tweets/"

tweet_files = [
    "prague-2015-02-14.json",
    "prague-2015-02-15.json"
]


def acquire(tweet_file):
    if not os.path.isfile(tweet_file):
        url = tweet_url_base + tweet_file
        print "file '%s' is missing, downloading from %s" % (tweet_file, url)
        with contextlib.closing(urllib2.urlopen(url)) as tweet_reader, open(tweet_file, 'wb') as tweet_writer:
            tweet_writer.write(tweet_reader.read())


def tweets():
    for tweet_file in tweet_files:
        acquire(tweet_file)
        print "reading '%s'" % tweet_file
        with open(tweet_file, 'r') as tweet_reader:
            for line in tweet_reader:
                if len(line) > 2:
                    if line[-2] == ',':
                        line = line[:-2]
                    else:
                        line = line[:-1]
                    yield json.loads(line)


def string_to_datetime(twitter_date) :
    return datetime.datetime.strptime(twitter_date, "%a %b %d %H:%M:%S +0000 %Y")