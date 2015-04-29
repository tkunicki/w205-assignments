from mrjob_tweet_count import TweetCountJob
import operator
import sys


def stream(output):
    for line in output:
        yield job.parse_output_line(line)

if __name__ == '__main__':
    # Creates an instance of our MRJob subclass
    job = TweetCountJob(args=sys.argv[1:])
    with job.make_runner() as runner:
        # Run the job
        runner.run()
        # process stream and find max
        max_tweeter = max(stream(runner.stream_output()), key=operator.itemgetter(1))
        print "### top tweeter"
        print max_tweeter[0], max_tweeter[1]