from mrjob.job import MRJob


class HashtagCountJob(MRJob):

    def mapper(self, _, line):
        for item in line.split(',')[2:]:
            yield item.lower(), 1

    def combiner(self, word, counts):
        yield word, sum(counts)

    def reducer(self, word, counts):
        yield word, sum(counts)


if __name__ == '__main__':
    HashtagCountJob.run()