import csv
import json
import logging

def export_to_csv(data, file_path):
    if not data:
        return
    fieldnames = data[0].keys()
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)
    logging.debug(f"Data exported to CSV: {file_path}")

def export_to_json(data, file_path):
    with open(file_path, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)
    logging.debug(f"Data exported to JSON: {file_path}")
