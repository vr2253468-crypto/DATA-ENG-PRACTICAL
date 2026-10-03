import json
from datetime import datetime, timezone
from pathlib import Path


OUTPUT_PATH = Path(__file__).parent / "output" / "extracted_data.json"


def extract_data():
    return {
        "source": "local_pipeline_check",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "status": "extracted",
    }


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(extract_data(), indent=2) + "\n", encoding="utf-8")
    print(f"Extracted data written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
