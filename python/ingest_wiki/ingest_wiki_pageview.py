import os
import time
import gzip
import shutil
from datetime import timedelta, date
from urllib import request


def calc_datetime(execute_time: str):
    days, times = execute_time.split("T")
    year, month, day = days[:4], days[4:6], days[6:]
    yesterday = date(year=int(year), month=int(month), day=int(day)) - timedelta(days=1)
    year, month, day, *_ = yesterday.timetuple()
    hour = times[:2]

    print(f"Execution Timestamp: {year}-{month}-{day} {hour}H")

    return year, month, day, hour

def get_data(execute_date: str) -> None:
    # Calculate the datetime
    year, month, day, hour, *_ = calc_datetime(execute_date)

    # Define the URL
    url = (
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{year}/{year}-{month:0>2}/pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    )

    path = "/tmp"
    zip_path = path + "/wikipageviews.gz"
    file_path = path + "/wikipageviews"

    if not os.path.exists(path):
        os.makedirs(path)

    # Download the wiki pageview data
    request.urlretrieve(url, zip_path)
    print("Donwloading the wiki pageviews is finished.")

    with gzip.open(zip_path, 'rb') as f_in:
        with open(file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    print("Unzipping the wiki pageviews is finished.")
    
    time.sleep(10)

if __name__ == "__main__":
    execute_date = os.environ.get('EXECUTE_DATE', "None")
    get_data(execute_date=execute_date)
