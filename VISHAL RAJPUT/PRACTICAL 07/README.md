# Practical 07 - CSV/JSON ETL with Incremental SQLite Loading

## Objective
Load CSV and JSON customer records, validate and clean data, track invalid records, and apply incremental updates in SQLite.

## Contents
- `data/etl_pipeline.py`
- `data/customers.csv`
- `data/customers_additional.csv`
- `data/customer_updates.json`

The previous nested duplicate project has been removed because it contained identical practical files. The unrelated `etl-specialist.agent.md` file was also removed.

## Prerequisites
- Python 3.10+
- Pandas

## Dependency install
```bash
pip install pandas
```

## Execution guidance
```bash
cd Practical-07/data
python etl_pipeline.py --input-dir . --database etl.db
```

## Learning outcomes
- Build validation-first ETL logic.
- Apply record hashing and incremental loading.
