from mrjob.job import MRJob


class TweetCountJob(MRJob):

    def mapper(self, _, line):
        yield line.split(',')[1], 1

    def combiner(self, word, counts):
        yield word, sum(counts)

    def reducer(self, word, counts):
        yield word, sum(counts)


if __name__ == '__main__':
    TweetCountJob.run()