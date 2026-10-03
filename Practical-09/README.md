# Practical 09 - Incremental E-commerce ETL with SQLite

## Objective
Implement historical and incremental loads for e-commerce CSV datasets with data-quality tracking and reporting.

## Contents
- `etl_pipeline.py`
- `requirements.txt`
- `data/*.csv`
- `tests/test_pipeline.py`

Generated SQLite databases and report CSVs are intentionally excluded because the pipeline recreates them.

## Prerequisites
- Python 3.10+
- Pandas

## Dependency install
```bash
pip install -r requirements.txt
```

## Execution
```bash
cd Practical-09
python etl_pipeline.py
python -m unittest tests/test_pipeline.py
```

## Learning outcomes
- Build idempotent ETL with validation rules.
- Apply upserts and data-quality issue logging.
- Understand historical versus incremental loading.
