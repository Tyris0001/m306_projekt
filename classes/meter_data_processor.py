from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from helpers import export_to_csv, export_to_json

class MeterDataProcessor:
    def __init__(self, sdat_data, esl_data):
        self.sdat_data = sdat_data
        self.esl_data = esl_data
        self.processed_data = defaultdict(list)

    def process_data(self):
        esl_dict = {row['obis']: row['value'] for row in self.esl_data}

        for sdat in self.sdat_data:
            document_id = sdat['document_id']
            timestamp = sdat['timestamp']
            volume = sdat['volume']

            absolute_value = esl_dict.get(document_id, 0) + volume
            self.processed_data[document_id].append({
                'timestamp': timestamp,
                'volume': volume,
                'absolute_value': absolute_value
            })

    def export_to_csv(self, file_path):
        data = []
        for document_id, entries in self.processed_data.items():
            for entry in entries:
                data.append({
                    'document_id': document_id,
                    'timestamp': entry['timestamp'],
                    'volume': entry['volume'],
                    'absolute_value': entry['absolute_value']
                })
        export_to_csv(data, file_path)

    def export_to_json(self, file_path):
        export_to_json(self.processed_data, file_path)

    def visualize_data(self):
        for document_id, entries in self.processed_data.items():
            timestamps = [entry['timestamp'] for entry in entries]
            volumes = [entry['volume'] for entry in entries]
            absolute_values = [entry['absolute_value'] for entry in entries]

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(timestamps, volumes, label='Volume')
            ax.plot(timestamps, absolute_values, label='Absolute Value')
            ax.set_xlabel('Timestamp')
            ax.set_ylabel('Value')
            ax.set_title(f'Data for {document_id}')
            ax.legend()
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
