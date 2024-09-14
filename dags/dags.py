from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from scripts.pipeline import etl_func
import pendulum

default_args = {
    'owner': 'airflow',
    'start_date': pendulum.today('UTC').subtract(days=1),
}

dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    schedule='@daily',
)

etl_operator = PythonOperator(
    task_id='etl_task',
    python_callable=etl_func,
    dag=dag,
)

etl_operator.execute(context={})