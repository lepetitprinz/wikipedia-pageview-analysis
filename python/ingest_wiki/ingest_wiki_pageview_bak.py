import os
import gzip
import shutil
from urllib import request
from datetime import datetime


def get_data(context):
    time = datetime.strptime(context, "%Y-%m-%dT%H:%M:%S%z")
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
    execute_date = os.environ.get('EXECUTE_DATE')
    print(execute_date)

    get_data(context=execute_date)