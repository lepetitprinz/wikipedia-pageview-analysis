from datetime import timedelta

import airflow.utils.dates
from airflow import DAG
from kubernetes.client import models as k8s
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator


default_args = {
    "owner": "yjkim",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "max_active_runs": 1,
}

dag = DAG(
    dag_id="context_test_dag",
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

log_volume_mount = k8s.V1VolumeMount(
    name="airflow-log-volume",
    mount_path="/log",
    read_only=False
)

# env_vars = [k8s.V1EnvVar(name=name, value=value, value_from=value_from) for name, value, value_from in '{{ ts }}']

context_data = KubernetesPodOperator(
    task_id="context_test",
    image="context-test:0.0.1",
    name="context_test",
    namespace="airflow",
    volumes=[log_volume],
    volume_mounts=[log_volume_mount],
    env_vars= {
        "EXECUTE_DATE": "{{ macros.datetime.strftime(ts, '%Y%m%d%H') }}"
    },
    in_cluster=True,
    is_delete_operator_pod=True,
    startup_timeout_seconds=300,
    execution_timeout=timedelta(minutes=5),
    retries=2,
    image_pull_policy='IfNotPresent',
    service_account_name='airflow',
    get_logs=True,
    dag=dag,
)

context_data 