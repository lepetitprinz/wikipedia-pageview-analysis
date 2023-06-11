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
}

dag = DAG(
    dag_id="wikipedia_pageview_ingest_data",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@daily",
    default_args=default_args
)
    
log_volume = k8s.V1Volume(
    name="airflow-log-volume",
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(
        claim_name="airflow-log-pvc"
    )
)

data_volume = k8s.V1Volume(
    name="airflow-data-volume",
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(
        claim_name="airflow-data-pvc"
    )
)

log_volume_mount = k8s.V1VolumeMount(
    name="airflow-log-volume",
    mount_path="/log",
    read_only=False
)

data_volume_mount = k8s.V1VolumeMount(
    name="airflow-data-volume",
    mount_path="/tmp",
    read_only=False
)

ingest_data = KubernetesPodOperator(
    task_id="ingest_wiki_pageview",
    image="ingest-wiki:0.0.1",
    name="ingest_wiki_pageview",
    namespace="airflow",
    volumes=[data_volume, log_volume],
    volume_mounts=[data_volume_mount, log_volume_mount],
    env_vars= {
        "EXECUTE_DATE": "{{ ts_nodash }}"
    },
    in_cluster=True,
    is_delete_operator_pod=True,
    startup_timeout_seconds=600,
    execution_timeout=timedelta(minutes=10),
    retries=2,
    image_pull_policy='IfNotPresent',
    service_account_name='airflow',
    get_logs=True,
    dag=dag,
)

ingest_data 