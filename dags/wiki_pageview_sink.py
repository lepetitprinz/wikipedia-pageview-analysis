from datetime import timedelta

import airflow.utils.dates
from airflow import DAG
from kubernetes.client import models as k8s
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

volume = k8s.V1Volume(
    name="wiki-airflow-volume",
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(
        claim_name="wiki-airflow-pvc"
    )
)

volume_mount = k8s.V1VolumeMount(
    name="wiki-airflow-volume",
    mount_path="/mnt/airflow/data",
    sub_path=None,
    read_only=False
)

ingest_data = KubernetesPodOperator(
    task_id="ingest_wiki_pageview",
    image="python",
    name="get_wiki_pageview",
    namespace="airflow",
    volumes=[volume],
    volume_mounts=[volume_mount],
    cmds=["python3"],
    arguments=["/opt/airflow/scripts/download_wiki_pageview.py", "--context_variable", '{{ ts }}'],
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
    volumes=[volume],
    volume_mounts=[volume_mount],
    cmds=["python3"],
    arguments=["/opt/airflow/scripts/fetch_wiki_pageview.py", "--context_variable", '{{ ts }}'],
    in_cluster=True,
    is_delete_operator_pod=True,
    execution_timeout=timedelta(minutes=30),
    retries=1,
    image_pull_policy='IfNotPresent',
    service_account_name='airflow',
    dag=dag,
)


ingest_data >> fetch_data