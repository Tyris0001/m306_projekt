import webview
import json
import os
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pandas as pd
import base64
import logging

from classes.esl_parser import ESLParser
from classes.sdat_parser import SDATParser

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class EnergyVisualizationApp:
    def __init__(self):
        self.parsed_data = {'entries': []}
        logger.debug("EnergyVisualizationApp initialized")

    def process_files(self, file_data_list):
        logger.debug(f"Processing {len(file_data_list)} files")
        for file_data in file_data_list:
            file_name = file_data['name']
            file_content = base64.b64decode(file_data['content'].split(',')[1])

            with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name

            logger.debug(f"Processing file: {file_name}")
            if file_name.lower().endswith('.xml'):
                if 'esl' in file_name.lower():
                    parser = ESLParser(temp_file_path)
                elif 'sdat' in file_name.lower():
                    parser = SDATParser(temp_file_path)
                else:
                    logger.warning(f"Unknown file type: {file_name}")
                    continue

                parser.parse()
                new_data = parser.get_data()
                self.parsed_data['entries'].extend(new_data)
                logger.debug(f"Added {len(new_data)} entries from {file_name}")

            os.unlink(temp_file_path)  # Delete the temporary file

        logger.debug(f"Finished processing files. Total entries: {len(self.parsed_data['entries'])}")
        return {"success": True, "message": f"Processed {len(file_data_list)} files"}

    def get_chart_data(self):
        logger.debug("Getting chart data")
        df = pd.DataFrame(self.parsed_data['entries'])
        if df.empty:
            logger.warning("No data available for chart")
            return {'production': [], 'consumption': []}

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

        # Group by type and timestamp, then cumsum the values
        production = df[df['type'] == 'production'].groupby('timestamp')['value'].sum().cumsum().reset_index()
        consumption = df[df['type'] == 'consumption'].groupby('timestamp')['value'].sum().cumsum().reset_index()

        # Convert timestamps to ISO format strings
        production['timestamp'] = production['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')
        consumption['timestamp'] = consumption['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')

        logger.debug(
            f"Chart data prepared. Production entries: {len(production)}, Consumption entries: {len(consumption)}")
        return {
            'production': production.to_dict('records'),
            'consumption': consumption.to_dict('records')
        }


def create_window():
    logger.debug("Creating application window")
    with open('./templates/index.html', 'r') as file:
        html_content = file.read()

    app = EnergyVisualizationApp()
    window = webview.create_window('Energy Visualization', html=html_content, js_api=app)
    return window


if __name__ == '__main__':
    window = create_window()
    webview.start(debug=True)