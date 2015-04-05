from mrjob.job import MRJob
import dateutil.parser


class HourCETCountJob(MRJob):

    def mapper(self, _, line):
        hour_cet = (dateutil.parser.parse(line.split(',')[0]).hour + 1) % 24
        yield "%02d:00+0100" % hour_cet, 1

    def combiner(self, word, counts):
        yield word, sum(counts)

    def reducer(self, word, counts):
        yield word, sum(counts)


if __name__ == '__main__':
    HourCETCountJob.run()