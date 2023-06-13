import os
from typing import Dict
from datetime import date, datetime, timedelta


def _fetch_pageview() -> Dict[str, int]:
    # Read the file within the mounted volume
    result = {}
    with open("/tmp/wikipageviews", "r") as f:
        for line in f:
            domain_code, page_title, view_counts, _ = line.split(" ")
            if domain_code == "en" and len(page_title) < 100:
                result[page_title] = view_counts
    
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

def convert_to_sql(data: Dict[str, int]) -> None:
    # Get the time related data
    execute_date, execute_time = _calc_datetime()

    # Save pageview data to sql statement
    with open("/tmp/wiki_pageview.sql", "w") as f:
        for page_name, pageview_cnt in data.items():
            f.write(
                "INSERT INTO pageview_counts VALUES ("
                f"'{execute_date}', '{execute_time}', '{page_name}', {pageview_cnt}"
                ");\n"
            )

if __name__ == "__main__":
    pageview = _fetch_pageview()
    convert_to_sql(data=pageview)