#! /usr/bin/env python

__author__ = 'tkunicki'

import codecs
import glob
import json
import os
import re
import sys


def sort_key(name):
    m = re.match(".*_(\d{4})-(\d{2})-(\d{2})\.(\d+)\.json", name)
    if m:
        k = m.group(1) + m.group(2) + m.group(3) + m.group(4).rjust(6, '0')
        return int(k)
    else:
        return -1
    

def merge_tweet_json(basename):

    tweet_in_files = glob.glob(basename + "_*-*-*.*.json")
    tweet_in_files.sort(key=sort_key)

    tweet_out_file = basename + '.txt'
    with codecs.open(tweet_out_file, 'w', encoding='utf8') as tweet_out:
        for tweet_in_file in tweet_in_files:
            print "processing: ", tweet_in_file
            with codecs.open(tweet_in_file, 'r', encoding='utf8') as tweet_in:
                tweets = json.loads(tweet_in.read().decode())
                for tweet in tweets:
                    tweet_out.write(tweet["text"] + "\n")
    print "wrote:", tweet_out_file


def usage():
    print "usage: %s basename" % sys.argv[0]
    print "  basename: base file name to merge."


if __name__ == "__main__":

    if len(sys.argv) != 2:
        usage()

    merge_tweet_json(sys.argv[1])
