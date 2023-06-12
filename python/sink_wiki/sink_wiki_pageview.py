import os
import psycopg2
from typing import Dict
from datetime import date, datetime, timedelta


def _fetch_pageview() -> Dict[str, int]:
    # Read the file within the mounted volume
    result = {}
    with open("/mnt/wikipageviews", "r") as f:
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

def sink_pageview(data: Dict[str, int]) -> None:
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host='localhost',
        port='5432',
        dbname='wiki',
        user='postgres',
        password='postgres'
    )

    # Create a cursor object to execute SQL statements
    cursor = conn.cursor()

    # Get the time related data
    execute_date, execute_time = _calc_datetime()

    # Execute SQL statements to save the data in the database
    for page_name, pageview_cnt in data.items():
        cursor.execute("INSERT INTO pageview_counts (execute_date, execute_time, page_name, pageview_cnt) VALUES (%s, %s, %s, %s)",
                    (execute_date, execute_time, page_name, pageview_cnt))

    # Commit the changes and close the cursor and connection
    conn.commit()
    print("Commited to database.")
    cursor.close()
    conn.close()
    print("Database connection is closed.")

if __name__ == "__main__":
    pageview = _fetch_pageview()
    sink_pageview(data=pageview)