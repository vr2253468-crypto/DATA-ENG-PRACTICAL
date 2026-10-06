from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

# Default arguments for the workflow pipeline execution
default_args = {
    "owner": "data_engineering_lab",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG context
with DAG(
    "university_etl_orchestration",
    default_args=default_args,
    description="Lab assignment for API and Flat File ETL orchestration",
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    # Task 1: Pipeline Init Anchor
    start_pipeline = EmptyOperator(task_id="start_pipeline")

    # Task 2: Run Python Extraction Script
    execute_extraction = BashOperator(
        task_id="run_extraction_script",
        bash_command="python3 data_extraction.py",
        cwd="{{ dag.folder }}",
    )

    # Task 3: Finalize and Log Metrics
    pipeline_complete = BashOperator(
        task_id="log_pipeline_success",
        bash_command='echo "ETL Execution completed successfully at $(date)"',
    )

    start_pipeline >> execute_extraction >> pipeline_complete
