from datetime import datetime, timedelta

from kubernetes.client import models as k8s
from airflow.models import DAG, Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

dag_id = 'kubernetes-test-dag'

task_default_args = {
    'owner': 'admin',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 1, 1),
    'depends_on_past': False,
    'email': ['admin@example.com'],
    'email_on_retry': False,
    'email_on_failure': False,
    'execution_timeout': timedelta(hours=1)
}

dag = DAG(
    dag_id=dag_id,
    description='kubernetes pod operator',
    default_args=task_default_args,
    schedule_interval='0 0 * * *',
    max_active_runs=1
)

resources = k8s.V1ResourceRequirements(
    limits={"memory": "1Gi", "cpu": "1"},
    requests={"memory": "500Mi", "cpu": "0.5"},
)

start = DummyOperator(task_id="start", dag=dag)

run = KubernetesPodOperator(
    # The ID specified for the task
    task_id="kubernetes-pod-operator",
    image='debian',
    image_pull_policy="IfNotPresent",
    # launch the pod on the same cluster as Airflow is running
    in_cluster=True,
    namespace='airflow',
    # Pod configuration
    # name of task you want to run, used to generate Pod ID
    name="example", 
    cmds=["bash", "-cx"],
    arguments=["echo", "10"],
    service_account_name="airflow",
    container_resources=resources,
    # delete Pod after the task is finished
    is_delete_operator_pod=True,
    # determines whether to use the stdout of the container as task-logs to the Airflow logging system
    get_logs=True,
    do_xcom_push=True,
    dag=dag,
)

start >> run