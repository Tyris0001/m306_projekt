import csv
import json

def export_to_csv(data, file_path):
    if not data:
        return
    fieldnames = data[0].keys()
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

def export_to_json(data, file_path):
    with open(file_path, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)
