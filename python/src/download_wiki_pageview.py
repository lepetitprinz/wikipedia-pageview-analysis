from urllib import request
import argparse
from datetime import datetime

def parse_variable():
    parser = argparse.ArgumentParser()
    parser.add_argument('--context_variable', type=str)
    args = parser.parse_args()

    return args.context_variable


def get_data(variables):
    time = datetime.strptime(variables, "%Y-%m-%dT%H:%M:%S%z")
    year, month, day, hour, *_ = time.timetuple()
    url = (
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{year}/{year}-{month:0>2}/pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    )
    request.urlretrieve(url, "/mnt/output/wikipageviews.gz")

if __name__ == "__main__":
    variables = parse_variable()
    app.get_data(variables)
