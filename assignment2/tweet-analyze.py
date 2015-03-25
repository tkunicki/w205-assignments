#! /usr/bin/env python

__author__ = 'tkunicki'

import codecs
import collections
import math
import operator
import re
import string
import sys
# sudo pip install git+git://github.com/amueller/word_cloud.git
# sudo pip install Image
import wordcloud
# wget http://raw.githubusercontent.com/mpcabd/python-arabic-reshaper/master/arabic_reshaper.py
import arabic_reshaper
# sudo pip install python-bidi
from bidi.algorithm import get_display
from unicodedata import bidirectional


word_excludes = [
    'rt',
    'https?.*',
    '&amp;'
]


def load_stop_words(file_name="stop-word-list.txt"):
    with open(file_name, "r") as f:
        return f.read().splitlines()


def accept_word(word):
    for f in word_excludes:
        if re.match(f, word.lower()):
            return False
    return True


def accept_mention(word):
    return word.startswith("@")


def accept_hashtag(word):
    return word.startswith("#")


def analyze_tweet_file(tweet_file):
    with codecs.open(tweet_file, 'r', encoding='utf8') as tweet_stream:
        mentions, hashtags, words = analyze_tweet_stream(tweet_stream)
    basename = tweet_file.replace(".txt", "")
    counts_out(mentions, basename + ".mentions")
    counts_out(hashtags, basename + ".hashtags")
    counts_out(words, basename + ".words")


def analyze_tweet_stream(tweet_stream):

    stop_words = load_stop_words()

    mentions = collections.Counter()
    hashtags = collections.Counter()
    words = collections.Counter()

    for tweet in tweet_stream:
        tokens = tweet.split()
        for token in tokens:
            if len(token) > 0:
                if accept_hashtag(token):
                    hashtags[token.rstrip(string.punctuation).lower()] += 1
                elif accept_mention(token):
                    mentions[token.rstrip(string.punctuation).lower()] += 1
                elif accept_word(token):
                    word = token.strip(string.punctuation).lower()
                    if word not in stop_words:
                        words[word] += 1

    return mentions, hashtags, words


def counts_out(counts, basename):

    count_max = counts.most_common()[0][1]
    if count_max == 0:
        return

    counts_sorted = sorted(counts.items(),
                           key=operator.itemgetter(1),
                           reverse=True)

    count_range = 80 - math.ceil(math.log10(count_max)) - 2
    count_max_log = math.log(count_max)
    if count_max_log == 0:
        count_max_log = 1

    hist_out_file = basename + ".hist.txt"
    with codecs.open(hist_out_file, 'w', encoding='utf8') as hist_out:
        for word, count in counts_sorted:
            hist_out.write("%s\n" % word)
            count_log = math.log(count)
            if count_log == 0:
                count_log = 1
            hashes = '#' * int(count_log / count_max_log * count_range)
            hist_out.write("%s %s\n" % (hashes, count))
        hist_out.write("\n")

    # NOTE: font_path is OS X specific
    wc = wordcloud.WordCloud(font_path='/Library/Fonts/Arial.ttf',
                             width=800, height=400)
    wc.fit_words(map(order_and_shape, filter(bad_unicode, counts.most_common(256))))
    wc.to_file(basename + ".png")


def order_and_shape(wc):
    return get_display(arabic_reshaper.reshape(wc[0])), wc[1]


def bad_unicode(wc):
    w = wc[0]
    if not isinstance(w, unicode):
        w = unicode(w)
    prev_surrogate = False
    for _ch in w:
        if sys.maxunicode == 0xffff and (0xD800 <= ord(_ch) <= 0xDBFF):
            prev_surrogate = _ch
            continue
        elif prev_surrogate:
            _ch = prev_surrogate + _ch
            prev_surrogate = False
        if bidirectional(_ch) == '':
            return False
    return True


def usage():
    print "usage: %s filename" % sys.argv[0]
    print "  basename: base file name to merge."


if __name__ == "__main__":

    if len(sys.argv) != 2:
        usage()

    analyze_tweet_file(sys.argv[1])
