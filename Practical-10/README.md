# Practical 10 - End-to-End Star-Schema ETL

## Objective
Run a complete CSV-to-warehouse pipeline using Pandas and SQLite, then generate analytical reports and an HTML dashboard.

## Contents
- `run_pipeline.py`
- `requirements.txt`
- `data/*.csv`
- `scripts/*.py`
- `tests/test_pipeline.py`

Generated SQLite database and report/dashboard files are excluded because the pipeline recreates them.

## Prerequisites
- Python 3.10+
- Dependencies listed in `requirements.txt`

## Dependency install
```bash
pip install -r requirements.txt
```

## Execution guidance
```bash
cd Practical-10
python run_pipeline.py
python -m unittest tests/test_pipeline.py
```

## Learning outcomes
- Build a reproducible ETL workflow.
- Clean and transform source data.
- Load a star-schema warehouse.
- Generate analytical reports and a dashboard.
