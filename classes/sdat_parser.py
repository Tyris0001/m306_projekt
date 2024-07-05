import datetime,logging
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
class SDATParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def parse(self):
        logger.debug(f"Parsing SDAT file: {self.file_path}")
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        ns = {'rsm': 'http://www.strom.ch'}

        document_id = root.find('.//rsm:DocumentID', ns).text
        type = 'consumption' if 'ID742' in document_id else 'production' if 'ID735' in document_id else 'unknown'

        start_time_elem = root.find('.//rsm:StartDateTime', ns)
        start_time = datetime.fromisoformat(start_time_elem.text) if start_time_elem is not None else None

        resolution_elem = root.find('.//rsm:Resolution/rsm:Resolution', ns)
        resolution = int(resolution_elem.text) if resolution_elem is not None else 15  # Default to 15 minutes

        observations = root.findall('.//rsm:Observation', ns)

        for obs in observations:
            sequence_elem = obs.find('.//rsm:Sequence', ns)
            volume_elem = obs.find('.//rsm:Volume', ns)

            sequence = int(sequence_elem.text) if sequence_elem is not None else None
            volume = float(volume_elem.text) if volume_elem is not None else None

            if start_time and sequence is not None:
                timestamp = start_time + timedelta(minutes=(sequence - 1) * resolution)
                self.data.append({
                    'timestamp': timestamp,
                    'value': volume,
                    'type': type
                })

        logger.debug(f"Parsed {len(self.data)} entries from SDAT file")

    def get_data(self):
        return self.data
