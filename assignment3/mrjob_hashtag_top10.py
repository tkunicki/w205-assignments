from mrjob_hashtag_count import HashtagCountJob
import heapq
import operator
import sys


def stream(output):
    for line in output:
        yield job.parse_output_line(line)

if __name__ == '__main__':
    # Creates an instance of our MRJob subclass
    job = HashtagCountJob(args=sys.argv[1:])
    with job.make_runner() as runner:
        # Run the job
        runner.run()
        # process stream and find top 10 using heap
        print "### top 10 hashtags"
        for hashtags in heapq.nlargest(10, stream(runner.stream_output()), key=operator.itemgetter(1)):
            print hashtags[0], hashtags[1]