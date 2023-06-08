from datetime import timedelta

import airflow.utils.dates
from airflow import DAG
from kubernetes.client import models as k8s
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from minio import Minio


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
    schedule_interval="@daily",
    default_args=default_args
)

def save_logs_to_minio():
    # MinIO configuration
    minio_endpoint = 'minio:9000'
    minio_access_key = 'accesskey'
    minio_secret_key = 'secretkey'
    minio_bucket_name = 'airflow'

    # Connect to MinIO
    minio_client = Minio(
        minio_endpoint, 
        access_key=minio_access_key, 
        secret_key=minio_secret_key, 
        secure=False
        )
    
    # Read the log file
    log_file_path = '/logs/wiki_ingest_task.log'
    with open(log_file_path, 'r') as file:
        log_content = file.read()

    # Upload the log file to MinIO
    minio_client.put_object(
        minio_bucket_name, 
        'logs/wiki_ingest_task.log',
        log_content        
        )

volume = k8s.V1Volume(
    name="wiki-airflow-volume",
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(
        claim_name="wiki-airflow-pvc"
    )
)

log_volume_mount = k8s.V1VolumeMount(
    name="wiki-log-volume",
    mount_path="/log",
    sub_path=None,
    read_only=False
)

data_volume_mount = k8s.V1VolumeMount(
    name="wiki-airflow-volume",
    mount_path="/mnt/airflow/data",
    read_only=False
)

ingest_data = KubernetesPodOperator(
    task_id="ingest_wiki_pageview",
    image="python-image",
    name="get_wiki_pageview",
    namespace="airflow",
    volumes=[volume],
    volume_mounts=[data_volume_mount, log_volume_mount],
    cmds=["python3"],
    arguments=["/opt/airflow/scripts/download_wiki_pageview.py", "--context_variable", '{{ ts }}'],
    in_cluster=True,
    is_delete_operator_pod=True,
    execution_timeout=timedelta(minutes=10),
    retries=2,
    image_pull_policy='IfNotPresent',
    service_account_name='airflow',
    get_logs=True,
    dag=dag,
)

fetch_data = KubernetesPodOperator(
    task_id="fetch_wiki_pageview",
    image="python",
    name="fetch_wiki_pageview",
    namespace="airflow",
    volumes=[volume],
    volume_mounts=[data_volume_mount, log_volume_mount],
    cmds=["python3"],
    arguments=["/opt/airflow/scripts/fetch_wiki_pageview.py", "--context_variable", '{{ ts }}'],
    in_cluster=True,
    is_delete_operator_pod=True,
    execution_timeout=timedelta(minutes=30),
    retries=1,
    image_pull_policy='IfNotPresent',
    service_account_name='airflow',
    get_logs=True,
    dag=dag,
)

save_logs_task = PythonOperator(
    task_id='save_logs_to_minio',
    python_callable=save_logs_to_minio,
    get_logs=True,
    dag=dag
)

ingest_data >> fetch_data >> save_logs_task