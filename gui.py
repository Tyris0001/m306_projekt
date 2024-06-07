import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from classes.sdat_parser import SDATParser
from classes.esl_parser import ESLParser
from classes.meter_data_processor import MeterDataProcessor
import os
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class DataProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Processor")
        logging.debug("Initializing Data Processor App")
        self.create_widgets()

    def create_widgets(self):
        logging.debug("Creating widgets")
        frame = ttk.Frame(self.root, padding="10 10 10 10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.process_button = ttk.Button(frame, text="Process Files", command=self.process_files)
        self.process_button.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        logging.debug("Process button created")

        self.output_label = ttk.Label(frame, text="")
        self.output_label.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        logging.debug("Output label created")

        # Ensure the frame expands to fill the window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

    def process_files(self):
        logging.debug("Processing files")
        sdat_folder = 'SDAT-Files'
        esl_folder = 'ESL-Files'

        if not os.path.exists(sdat_folder) or not os.path.exists(esl_folder):
            logging.error("Folders for SDAT or ESL files do not exist.")
            messagebox.showerror("Error", "Folders for SDAT or ESL files do not exist.")
            return

        sdat_files = [os.path.join(sdat_folder, file) for file in os.listdir(sdat_folder) if file.endswith('.xml')]
        esl_files = [os.path.join(esl_folder, file) for file in os.listdir(esl_folder) if file.endswith('.xml')]

        if not sdat_files or not esl_files:
            logging.error("No SDAT or ESL files found.")
            messagebox.showerror("Error", "No SDAT or ESL files found.")
            return

        logging.debug(f"Found {len(sdat_files)} SDAT files and {len(esl_files)} ESL files")

        esl_data = {}
        sdat_data = {}

        for file in esl_files:
            logging.debug(f"Parsing ESL file: {file}")
            esl_parser = ESLParser(file)
            esl_parser.parse()
            esl_data[file] = esl_parser.get_data()

        for file in sdat_files:
            logging.debug(f"Parsing SDAT file: {file}")
            sdat_parser = SDATParser(file)
            sdat_parser.parse()
            sdat_data[file] = sdat_parser.get_data()

        all_timestamps = []
        all_absolute_values = []

        for file, sdat_values in sdat_data.items():
            logging.debug(f"Processing data for file: {file}")
            meter_data_processor = MeterDataProcessor(sdat_values, esl_data.get(file, []))
            meter_data_processor.process_data()

            for document_id, entries in meter_data_processor.processed_data.items():
                timestamps = [entry['timestamp'] for entry in entries]
                absolute_values = [entry['absolute_value'] for entry in entries]

                all_timestamps.extend(timestamps)
                all_absolute_values.extend(absolute_values)

        logging.debug("Visualization started")
        self.visualize_data(all_timestamps, all_absolute_values)

    def visualize_data(self, timestamps, absolute_values):
        logging.debug("Visualizing data")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(timestamps, absolute_values, label='Absolute Value')
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Absolute Value')
        ax.set_title('Zählerstände über Zeit')
        ax.legend()
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        self.output_label.config(text="Processing complete. Files have been visualized.")
        logging.debug("Processing complete. Files have been visualized.")
        messagebox.showinfo("Success", "Processing complete. Files have been visualized.")


if __name__ == "__main__":
    logging.debug("Starting application")
    root = tk.Tk()
    app = DataProcessorApp(root)
    root.mainloop()
    logging.debug("Application closed")
