from datetime import timedelta
from urllib import request

import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


default_args = {
    "owner": "yjkim",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=3),
    "max_active_runs": 1,
    "template_searchpath": "/tmp"  # Path to search for sql file
}

dag = DAG(
    dag_id="wikipedia_pageview_data_sink",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@hourly",
    default_args=default_args
)

def _get_data(output_path, **context):
    year, month, day, hour, *_ = context["execution_date"].timetuple()
    url = (
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{year}/{year}-{month:0>2}/pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    )
    request.urlretrieve(url, output_path)

get_data = PythonOperator(
    task_id="get_data",
    python_callable=_get_data,
    op_kwargs={
        "output_path": "/tmp/wikipageviews.gz",
    },
    dag=dag,
)

extract_gz = BashOperator(
    task_id="extract_gz",
    bash_command="gunzip --force /tmp/wikipageviews.gz",
    dag=dag,
)

def _fetch_pageviews(execution_date):
    result = dict.fromkeys(pagenames, 0)
    with open("/tmp/wikipageviews", "r") as f:
        for line in f:
            domain_code, page_title, view_counts, _ = line.split(" ")
            if domain_code == "en":
                result[page_title] = view_counts
    
    with open("/tmp/postgres_query.sql", "w") as f:
        for pagename, pageviewcount in result.items():
            f.write(
                "INSERT INTO pageview_counts VALUES ("
                f"'{pagename}', {pageviewcount}, '{execution_date}'"
                ");\n"
            )

fetch_pageviews = PythonOperator(
    task_id="fetch_pageviews",
    python_callable=_fetch_pageviews,
    dag=dag,
)

write_to_postgres = PostgresOperator(
    task_id="write_to_postgres",
    postgres_conn_id="my_postgres",  # Identifier to credentials to use for connection
    sql="postgres_query.sql",  # SQL query or path to file containing SQL queries
    dag=dag,
)

get_data >> extract_gz >> fetch_pageviews >> write_to_postgres