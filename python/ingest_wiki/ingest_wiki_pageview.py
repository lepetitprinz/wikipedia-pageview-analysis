import os
import time
import gzip
import shutil
from urllib import request
from datetime import datetime
from datetime import timedelta


def get_data(context):
    yesterday = datetime.now() - timedelta(days=1)
    year, month, day, hour, *_ = yesterday.timetuple()
    url = (
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{year}/{year}-{month:0>2}/pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    )

    path = "/tmp"
    zip_path = path + "/wikipageviews.gz"
    file_path = path + "/wikipageviews"

    if not os.path.exists(path):
        os.makedirs(path)

    request.urlretrieve(url, zip_path)
    with gzip.open(zip_path, 'rb') as f_in:
        with open(file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    time.sleep(10)

if __name__ == "__main__":
    execute_date = os.environ.get('EXECUTE_DATE')
    get_data(context=execute_date)
