from datetime import timedelta
from urllib import request

import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

default_args = {
    "owner": "yjkim",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "max_active_runs": 1,
    "template_searchpath": "/opt/python"  # Path to search for sql file
}

dag = DAG(
    dag_id="wikipedia_pageview_data_sink",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@hourly",
    default_args=default_args
)

ingest_data = KubernetesPodOperator(
    task_id="ingest_wiki_pageview",
    image="python",
    name="get_wiki_pageview",
    namespace="airflow",
    volumes=[{
        'name': 'wiki-volume',
        'persistentVolumeClaim': {
            'claimName': 'wiki-pvc'
        }
    }],
    volume_mounts=[{
        'mountPath': '/mnt/output',
        'name': 'wiki-volume'
    }],
    cmds=["python3"],
    arguments=["download_wiki_pageview.py", "--context_variable", '{{ ts }}'],
    in_cluster=True,
    is_delete_operator_pod=True,
    execution_timeout=timedelta(minutes=10),
    retries=2,
    image_pull_policy='IfNotPresent',
    service_account_name='airflow',
    dag=dag,
)


fetch_data = KubernetesPodOperator(
    task_id="fetch_wiki_pageview",
    image="python",
    name="fetch_wiki_pageview",
    namespace="airflow",
    volumes=[{
        'name': 'wiki-volume',
        'persistentVolumeClaim': {
            'claimName': 'wiki-pvc'
        }
    }],
    volume_mounts=[{
        'mountPath': '/mnt/input',
        'name': 'wiki-volume'
    }],
    cmds=["python3"],
    arguments=["fetch_wiki_pageview.py", "--context_variable", '{{ ts }}'],
    in_cluster=True,
    is_delete_operator_pod=True,
    execution_timeout=timedelta(minutes=5),
    retries=1,
    image_pull_policy='IfNotPresent',
    service_account_name='airflow',
    dag=dag,
)


ingest_data >> fetch_data