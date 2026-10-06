# Practical 01 - Parsing, Anomaly Checks, Binary/Pickle, Regex, SQLite CRUD

## Objective
Practice multi-format parsing, basic data-quality checks, binary and pickle file handling, regex operations, and SQLite CRUD.

## Contents
- `setup_data.py`
- `ex1_parsing_and_anomalies.py`
- `ex2_binary_files.py`
- `ex3_regex_operations.py`
- `ex4_database_crud.py`
- Sample files: `sample.csv`, `sample.html`, `sample.xml`, `sample.json`, `sample.txt`
- Artifacts: `records.bin`, `app.pkl`, `app.db`

## Prerequisites
- Python 3.10+
- `beautifulsoup4` (for HTML parsing in `ex1_parsing_and_anomalies.py`)

## Dependency install
```bash
pip install beautifulsoup4
```

## Execution guidance (important path note)
These scripts reference files under a relative `data/` directory. Run from `Practical-01` and create data files first:

```bash
cd Practical-01
python setup_data.py
python ex1_parsing_and_anomalies.py
python ex2_binary_files.py
python ex3_regex_operations.py
python ex4_database_crud.py
```

## Expected/available outputs
- Console anomaly messages from parsing script
- Binary and pickle read/write console output
- Regex extraction/masking output
- SQLite CRUD console output
- Generated/updated files inside `data/` (when scripts are run as written)

## Security and safety
- `pickle.load` in `ex2_binary_files.py` should only be used with trusted local files.

## Troubleshooting
- `FileNotFoundError` for `data/...`: run `setup_data.py` first and confirm current directory is `Practical-01`.
- `ModuleNotFoundError: bs4`: install `beautifulsoup4`.

## Verification status
- Script execution was **not re-run in this documentation stage**.

## Learning outcomes
- Understand parsing patterns across CSV/HTML/XML/JSON.
- Identify simple anomalies in row-level records.
- Practice binary serialization and regex-based text processing.
- Apply basic SQLite CRUD workflow.
