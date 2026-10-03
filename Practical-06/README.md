# Practical 06 - Airflow DAG Orchestration Structure

## Objective
Represent an ETL-like workflow in Apache Airflow DAG format.

## Contents
- `dags/data_extraction.py`
- `dags/data_pipeline_dag.py`

The previous nested duplicate DAG directory has been removed because its files were identical to the canonical `dags/` files.

## Prerequisites
- Apache Airflow
- A Python environment compatible with the installed Airflow version

## Execution guidance

Place the `dags/` directory in the appropriate Airflow DAG location or configure the Airflow environment to load it.

## Learning outcomes
- Understand Airflow DAG structure.
- Understand task dependencies and simple ETL-style orchestration.
