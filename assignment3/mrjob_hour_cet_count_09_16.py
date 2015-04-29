from mrjob_hour_cet_count import HourCETCountJob
import sys


def stream(output):
    for line in output:
        yield job.parse_output_line(line)

if __name__ == '__main__':
    # Creates an instance of our MRJob subclass
    job = HourCETCountJob(args=sys.argv[1:])
    with job.make_runner() as runner:
        # Run the job
        runner.run()
        # process stream and find max
        hour_cet_counts = list(stream(runner.stream_output()))
        print "### tweets by hour"
        for hour_cet_count in hour_cet_counts[8:16]:
            print hour_cet_count[0], hour_cet_count[1]