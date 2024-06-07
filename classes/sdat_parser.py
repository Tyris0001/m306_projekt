import xml.etree.ElementTree as ET
from datetime import timedelta
from dateutil import parser as date_parser
from classes.helpers import export_to_csv, export_to_json
import logging

class SDATParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []
        logging.debug(f"SDATParser initialized for file: {file_path}")

    def parse(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        document_id_elem = root.find('.//{http://www.strom.ch}DocumentID')
        document_id = document_id_elem.text if document_id_elem is not None else None

        start_time_elem = root.find('.//{http://www.strom.ch}StartDateTime')
        start_time = start_time_elem.text if start_time_elem is not None else None

        resolution_value_elem = root.find('.//{http://www.strom.ch}Resolution')
        resolution_value = int(resolution_value_elem.find('{http://www.strom.ch}Resolution').text) if resolution_value_elem is not None else None

        observations = root.findall('.//{http://www.strom.ch}Observation')

        for obs in observations:
            sequence_elem = obs.find('.//{http://www.strom.ch}Sequence')
            volume_elem = obs.find('.//{http://www.strom.ch}Volume')

            sequence = int(sequence_elem.text) if sequence_elem is not None else None
            volume = float(volume_elem.text) if volume_elem is not None else None

            if start_time and resolution_value:
                timestamp = date_parser.parse(start_time) + timedelta(minutes=sequence * resolution_value)
                timestamp = timestamp.isoformat()

                self.data.append({
                    'document_id': document_id,
                    'timestamp': timestamp,
                    'sequence': sequence,
                    'volume': volume
                })
        logging.debug(f"SDAT file parsed: {self.file_path}")

    def get_data(self):
        unique_data = {entry['timestamp']: entry for entry in self.data}
        sorted_data = sorted(unique_data.values(), key=lambda x: x['timestamp'])
        logging.debug(f"SDAT data processed: {self.file_path}")
        return sorted_data

    def export_to_csv(self, file_path):
        export_to_csv(self.get_data(), file_path)

    def export_to_json(self, file_path):
        export_to_json(self.get_data(), file_path)
