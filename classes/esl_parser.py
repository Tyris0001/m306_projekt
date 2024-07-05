import datetime,logging
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
class ESLParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def parse(self):
        logger.debug(f"Parsing ESL file: {self.file_path}")
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        for meter in root.findall('.//Meter'):
            for time_period in meter.findall('.//TimePeriod'):
                end_time = time_period.get('end')
                consumption_value = 0
                production_value = 0

                for value_row in time_period.findall('.//ValueRow'):
                    obis = value_row.get('obis')
                    value = float(value_row.get('value'))

                    if obis in ['1-1:1.8.1', '1-1:1.8.2']:
                        consumption_value += value
                    elif obis in ['1-1:2.8.1', '1-1:2.8.2']:
                        production_value += value

                timestamp = datetime.fromisoformat(end_time)

                if consumption_value > 0:
                    self.data.append({
                        'timestamp': timestamp,
                        'value': consumption_value,
                        'type': 'consumption'
                    })

                if production_value > 0:
                    self.data.append({
                        'timestamp': timestamp,
                        'value': production_value,
                        'type': 'production'
                    })

        logger.debug(f"Parsed {len(self.data)} entries from ESL file")

    def get_data(self):
        return self.data