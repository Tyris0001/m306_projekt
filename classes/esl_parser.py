import xml.etree.ElementTree as ET
from datetime import datetime
from classes.helpers import export_to_csv, export_to_json

class ESLParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def parse(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        time_period_elem = root.find('.//TimePeriod')
        time_period = time_period_elem.attrib['end'] if time_period_elem is not None else None
        value_rows = root.findall('.//ValueRow')

        for row in value_rows:
            obis = row.attrib.get('obis')
            value = float(row.attrib.get('value'))
            status = row.attrib.get('status')

            if time_period:
                timestamp = datetime.fromisoformat(time_period).isoformat()

                self.data.append({
                    'timestamp': timestamp,
                    'obis': obis,
                    'value': value,
                    'status': status
                })

    def get_data(self):
        unique_data = {entry['timestamp']: entry for entry in self.data}
        sorted_data = sorted(unique_data.values(), key=lambda x: x['timestamp'])
        return sorted_data

    def export_to_csv(self, file_path):
        export_to_csv(self.get_data(), file_path)

    def export_to_json(self, file_path):
        export_to_json(self.get_data(), file_path)
