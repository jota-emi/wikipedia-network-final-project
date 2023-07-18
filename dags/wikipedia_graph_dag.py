from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Importing the functions
from functions_pipeline import getting_data, cleaning_data, plotting_results

# Default arguments for the DAG
default_args = {
    'owner': 'joao',
    'depends_on_past': False,
    'start_date': datetime(2023,7,17),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# DAG object
dag = DAG(
    dag_id='wikipedia_graph_dag',
    default_args=default_args,
    description='DAG for wikipedia graph',
    schedule_interval=timedelta(days=1),
    catchup=False
)

# Task "Getting the data"
get_data = PythonOperator(
    task_id='get_data',
    python_callable=getting_data,
    dag=dag
)

# Task "Cleaning the data"
clean_data = PythonOperator(
    task_id='clean_data',
    python_callable=cleaning_data,
    dag=dag
)

# Task "Results plotting"
plot_results = PythonOperator(
    task_id='plot_results',
    python_callable=plotting_results,
    dag=dag
)

# Dependencies
get_data >> clean_data >> plot_results

