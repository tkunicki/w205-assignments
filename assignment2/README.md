
Assignment Results
------------------
### Notes

  * Utilized Twitter API [app-only auth](https://dev.twitter.com/oauth/application-only) to take advantage of increased [request rate limits](https://dev.twitter.com/rest/public/rate-limits)
  * Optimized per-request result response with `count=100` [(default is `15`)](https://dev.twitter.com/rest/reference/get/search/tweets)
  * Tweets were tokenized with histograms and word clouds generated for 3 classes of tokens:
    * `@` mentions
      * tokens beginning with `@`
      * right stripped punctuation
      * converted to lower-case
    * `#` hashtags
      * tokens beginning with `#`
      * right stripped punctuation
      * converted to lower-case
    * words
      * punctuation was both left and right stripped
      * converted to lower-case
      * tokens of `rt`, `https?:.*`, `&amp;` or in an english word [stop list](stop-word-list.txt) were ignored.
  * Histograms
   * sorted in order of descending frequency 
   * tokens represented with 2 lines
     * first containing token
     * second with frequency represented with `#` characters in normalized log scale and count
  * Word clouds
    * generated because they are shiny.
    * a word cloud was created for the 256 most common tokens in each class
    * support proper arabic text rendering
      * character reordering with unicode bidi algorithm
      * font reshaping using 3rd party python code
      * *unused with analysis below, but of use for analysis of other ISIS tweet streams*
  * Potential improvements
    * use of stemming and other language processing (e.g. removal of `'s` possesive construct)
    * search terms should be removed from histograms and word plots as they will, obviously, dominate

### Analysis:  `q='#isis #anonymous' since=2015-02-05 until=2015-02-24`

 On February 9th the hacking collective know as "Anonymous" initiated a cyber response to ISIS.  This lead to an uptick in traffic related to the hashtags `#isis` and `#anonymous`.  Given that the twitter index goes back roughly 7 days I decided to harvest tweets from the twitter index during the event to observe and analyze it.

#### Tweet List
List of tweets available at: [http://kunicki-w205-assignment2.s3.amazonaws.com/tweet_#isis+#anonymous.txt](http://kunicki-w205-assignment2.s3.amazonaws.com/tweet_%23isis%2B%23anonymous.txt)
 
#### Histograms:
* [words](tweet_%23isis+%23anonymous.words.hist.txt)
* [`@` mentions](tweet_%23isis+%23anonymous.mentions.hist.txt)
* [`#` hastags](tweet_%23isis+%23anonymous.hashtags.hist.txt)
  
#### Word Clouds:
![words](tweet_%23isis+%23anonymous.words.png)
![`@` mentions](tweet_%23isis+%23anonymous.mentions.png)
![`#` hastags](tweet_%23isis+%23anonymous.hashtags.png)

