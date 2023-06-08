import gzip
import shutil
import argparse
import logging
from urllib import request
from datetime import datetime

def _parse_variable():
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

    zip_path = "/mnt/output/wikipageviews.gz"
    file_path = "/mnt/output/wikipageviews"
    request.urlretrieve(url, zip_path)
    with gzip.open(zip_path, 'rb') as f_in:
        with open(file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

if __name__ == "__main__":
    # Configure logging to write to the log file
    logging.basicConfig(
        filename='/logs/my_task.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.info('This is a python log message')

    variables = _parse_variable()
    get_data(variables)
