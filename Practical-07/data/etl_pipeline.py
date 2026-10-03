from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


EXPECTED_COLUMNS = ["id", "name", "age", "city", "sales"]
DATABASE_PATH = Path("data/etl.db")


def read_csv_files(input_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
	valid_records: list[dict[str, Any]] = []
	invalid_records: list[dict[str, Any]] = []

	for path in sorted(input_dir.glob("*.csv")):
		with path.open("r", newline="", encoding="utf-8-sig") as handle:
			reader = csv.reader(handle)
			header = next(reader, [])
			if header != EXPECTED_COLUMNS:
				invalid_records.append({"source_file": path.name, "row_number": 1, "reason": "Unexpected header", "raw_data": json.dumps(header)})
				continue

			for row_number, row in enumerate(reader, start=2):
				if len(row) != len(EXPECTED_COLUMNS):
					invalid_records.append({"source_file": path.name, "row_number": row_number, "reason": "Wrong number of fields", "raw_data": json.dumps(row)})
					continue
				valid_records.append(dict(zip(EXPECTED_COLUMNS, row)) | {"source_file": path.name, "source_type": "csv"})

	return valid_records, invalid_records


def read_json_files(input_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
	valid_records: list[dict[str, Any]] = []
	invalid_records: list[dict[str, Any]] = []

	for path in sorted(input_dir.glob("*.json")):
		try:
			payload = json.loads(path.read_text(encoding="utf-8"))
			items = payload if isinstance(payload, list) else payload.get("customers", [])
			if not isinstance(items, list):
				raise ValueError("JSON must contain a list or a customers list")
		except (OSError, json.JSONDecodeError, AttributeError, ValueError) as error:
			invalid_records.append({"source_file": path.name, "row_number": 0, "reason": f"Invalid JSON: {error}", "raw_data": ""})
			continue

		for row_number, item in enumerate(items, start=1):
			if not isinstance(item, dict):
				invalid_records.append({"source_file": path.name, "row_number": row_number, "reason": "JSON item is not an object", "raw_data": json.dumps(item)})
				continue
			valid_records.append({
				"id": item.get("id"),
				"name": item.get("full_name", item.get("name")),
				"age": item.get("age"),
				"city": item.get("location", item.get("city")),
				"sales": item.get("total_sales", item.get("sales")),
				"source_file": path.name,
				"source_type": "json",
			})

	return valid_records, invalid_records


def transform_records(records: list[dict[str, Any]]) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
	frame = pd.DataFrame(records, columns=EXPECTED_COLUMNS + ["source_file", "source_type"])
	invalid_records: list[dict[str, Any]] = []
	if frame.empty:
		return frame, invalid_records

	frame["id"] = pd.to_numeric(frame["id"], errors="coerce")
	frame["age"] = pd.to_numeric(frame["age"], errors="coerce")
	frame["sales"] = pd.to_numeric(frame["sales"], errors="coerce")
	frame["name"] = frame["name"].astype("string").str.strip()
	frame["city"] = frame["city"].astype("string").str.strip().str.title()

	invalid_mask = (
		frame["id"].isna()
		| frame["name"].isna()
		| frame["name"].eq("")
		| frame["age"].isna()
		| frame["age"].lt(0)
		| frame["sales"].isna()
		| frame["sales"].lt(0)
		| frame["city"].isna()
		| frame["city"].eq("")
	)
	for index, row in frame.loc[invalid_mask].iterrows():
		invalid_records.append({"source_file": row["source_file"], "row_number": index + 1, "reason": "Failed field validation", "raw_data": row.to_json()})

	clean = frame.loc[~invalid_mask].copy()
	clean["id"] = clean["id"].astype(int)
	clean["age"] = clean["age"].astype(int)
	clean["sales"] = clean["sales"].astype(float)
	clean = clean.drop_duplicates(subset=["source_type", "source_file", "id"], keep="last")
	return clean, invalid_records


def validate_before_load(frame: pd.DataFrame) -> None:
	required = EXPECTED_COLUMNS + ["source_file", "source_type"]
	missing = [column for column in required if column not in frame.columns]
	if missing or frame["id"].duplicated().any():
		raise ValueError(f"Target validation failed; missing={missing}, duplicate_ids={frame['id'].duplicated().any()}")


def load_incrementally(frame: pd.DataFrame, invalid_records: list[dict[str, Any]], database_path: Path) -> tuple[int, int]:
	database_path.parent.mkdir(parents=True, exist_ok=True)
	loaded = 0
	skipped = 0
	now = datetime.now(timezone.utc).isoformat()

	with sqlite3.connect(database_path) as connection:
		connection.execute("CREATE TABLE IF NOT EXISTS customers (record_key TEXT PRIMARY KEY, id INTEGER NOT NULL, name TEXT NOT NULL, age INTEGER NOT NULL, city TEXT NOT NULL, sales REAL NOT NULL, source_file TEXT NOT NULL, source_type TEXT NOT NULL, record_hash TEXT NOT NULL, loaded_at TEXT NOT NULL)")
		connection.execute("CREATE TABLE IF NOT EXISTS invalid_records (source_file TEXT, row_number INTEGER, reason TEXT, raw_data TEXT, recorded_at TEXT NOT NULL)")
		connection.executemany("INSERT INTO invalid_records VALUES (?, ?, ?, ?, ?)", [(row["source_file"], row["row_number"], row["reason"], row["raw_data"], now) for row in invalid_records])

		for row in frame.to_dict("records"):
			record_key = f"{row['source_type']}:{row['source_file']}:{row['id']}"
			record_hash = hashlib.sha256(json.dumps(row, sort_keys=True, default=str).encode()).hexdigest()
			existing = connection.execute("SELECT record_hash FROM customers WHERE record_key = ?", (record_key,)).fetchone()
			if existing and existing[0] == record_hash:
				skipped += 1
				continue
			connection.execute("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(record_key) DO UPDATE SET id=excluded.id, name=excluded.name, age=excluded.age, city=excluded.city, sales=excluded.sales, source_file=excluded.source_file, source_type=excluded.source_type, record_hash=excluded.record_hash, loaded_at=excluded.loaded_at", (record_key, row["id"], row["name"], row["age"], row["city"], row["sales"], row["source_file"], row["source_type"], record_hash, now))
			loaded += 1

	return loaded, skipped


def main() -> None:
	parser = argparse.ArgumentParser(description="Load CSV and JSON customer data incrementally into SQLite.")
	parser.add_argument("--input-dir", type=Path, default=Path("data"))
	parser.add_argument("--database", type=Path, default=DATABASE_PATH)
	args = parser.parse_args()

	csv_records, csv_invalid = read_csv_files(args.input_dir)
	json_records, json_invalid = read_json_files(args.input_dir)
	clean_records, transform_invalid = transform_records(csv_records + json_records)
	validate_before_load(clean_records)
	loaded, skipped = load_incrementally(clean_records, csv_invalid + json_invalid + transform_invalid, args.database)
	print(f"Loaded or updated: {loaded}; skipped unchanged: {skipped}; invalid records: {len(csv_invalid + json_invalid + transform_invalid)}")


if __name__ == "__main__":
	main()