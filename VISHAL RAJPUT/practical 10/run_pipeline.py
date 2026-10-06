from scripts.pipeline import run_pipeline


if __name__ == "__main__":
    result = run_pipeline()
    print(f"Loaded {result['loaded_rows']} valid rows ({result['rejected_rows']} rejected)")
    print(f"Warehouse: {result['database']}")
    print(f"Dashboard: {result['reports']['dashboard.html']}")
