import os
import time
from typing import List
import pandas as pd
import fastparquet as fp
from datetime import date, datetime, timedelta


def _fetch_pageview() -> List[str, int]:
    # Read the file within the mounted volume
    result = []
    with open("/tmp/wikipageviews", "r") as f:
        for line in f:
            domain_code, page_title, view_counts, _ = line.split(" ")
            if domain_code == "en" and len(page_title) < 100:
                result.append([page_title, view_counts])
    
    return result

def _calc_datetime():
    # Get the execute date variable
    timestamp = os.environ.get('EXECUTE_DATE', "None")

    days, times = timestamp.split("T")
    year, month, day = days[:4], days[4:6], days[6:]

    execute_date = date(year=int(year), month=int(month), day=int(day)) - timedelta(days=1)
    execute_date = execute_date.strftime("%Y-%m-%d")

    hour = times[:2]
    execute_time = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour)) - timedelta(days=1)
    execute_time = execute_time.strftime("%Y-%m-%d %H:%M:%S")

    return execute_date, execute_time

def convert_to_parquet(data: List[str, int]) -> None:
    df = pd.DataFrame(data, columns=["page_title", "view_counts"])

    # Get the time related data
    execute_date, execute_time = _calc_datetime()

    # Add execute date and time columns
    df["execute_date"] = execute_date
    df["execute_time"] = execute_time

    # Writes to parquet file
    parquet_path = '/tmp/wiki_pageview.parquet'
    fp.write(parquet_path, df, compression='GZIP')

if __name__ == "__main__":
    pageview = _fetch_pageview()
    convert_to_parquet(data=pageview)
    time.sleep(10)