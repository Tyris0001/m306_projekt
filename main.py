from classes.sdat_parser import SDATParser
from classes.esl_parser import ESLParser
from classes.meter_data_processor import MeterDataProcessor
import os

os.makedirs('Processed-Data/SDAT/csv', exist_ok=True)
os.makedirs('Processed-Data/SDAT/json', exist_ok=True)
os.makedirs('Processed-Data/ESL/csv', exist_ok=True)
os.makedirs('Processed-Data/ESL/json', exist_ok=True)

esl_files = []
sdat_files = []

for file in os.listdir('ESL-Files'):
    if file.endswith('.xml'):
        esl_files.append(file)

for file in os.listdir('SDAT-Files'):
    if file.endswith('.xml'):
        sdat_files.append(file)

esl_data = {}
sdat_data = {}

for file in esl_files:
    esl_parser = ESLParser(f'ESL-Files/{file}')
    esl_parser.parse()
    esl_data[file] = esl_parser.get_data()
    esl_parser.export_to_csv(f'Processed-Data/ESL/csv/{file}.csv')
    esl_parser.export_to_json(f'Processed-Data/ESL/json/{file}.json')

for file in sdat_files:
    sdat_parser = SDATParser(f'SDAT-Files/{file}')
    sdat_parser.parse()
    sdat_data[file] = sdat_parser.get_data()
    meter_data_processor = MeterDataProcessor(sdat_data[file], esl_data.get(file, []))
    meter_data_processor.process_data()
    meter_data_processor.export_to_csv(f'Processed-Data/SDAT/csv/{file}.csv')
    meter_data_processor.export_to_json(f'Processed-Data/SDAT/json/{file}.json')
    meter_data_processor.visualize_data()
