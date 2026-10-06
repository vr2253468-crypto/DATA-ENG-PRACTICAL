import csv

with open('locations.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(f"ID: {row['id']}, City: {row['city']}, Country: {row['country']}")