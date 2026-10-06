import csv
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def parse_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        return [dict(row) for row in csv.DictReader(f)]

def parse_html(path):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        table = soup.find("table")
        if table:
            headers = [th.text.strip() for th in table.find_all("th")]
            for tr in table.find_all("tr")[1:]:
                cells = [td.text.strip() for td in tr.find_all("td")]
                if len(cells) == len(headers):
                    records.append(dict(zip(headers, cells)))
    return records

def parse_xml(path):
    tree = ET.parse(path)
    return [{c.tag: (c.text.strip() if c.text else None) for c in u} for u in tree.getroot().findall("user")]

def parse_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def detect_anomalies(records, name):
    print(f"\n--- Quality Audit: {name} ({len(records)} rows) ---")
    for idx, row in enumerate(records, start=1):
        for k, v in row.items():
            if v is None or str(v).strip() == "":
                print(f"  [ANOMALY] Row {idx}: Missing field '{k}'")
        if "age" in row and row["age"] is not None:
            try:
                age = float(row["age"])
                if age < 0 or age > 120:
                    print(f"  [ANOMALY] Row {idx}: Invalid age value ({age})")
            except ValueError:
                print(f"  [ANOMALY] Row {idx}: Non-numeric age '{row['age']}'")
        if "salary" in row and row["salary"] is not None:
            try:
                salary = float(row["salary"])
                if salary < 0:
                    print(f"  [ANOMALY] Row {idx}: Negative salary ({salary})")
            except ValueError:
                print(f"  [ANOMALY] Row {idx}: Non-numeric salary '{row['salary']}'")

if __name__ == "__main__":
    detect_anomalies(parse_csv("data/sample.csv"), "CSV")
    detect_anomalies(parse_html("data/sample.html"), "HTML")
    detect_anomalies(parse_xml("data/sample.xml"), "XML")
    detect_anomalies(parse_json("data/sample.json"), "JSON")