import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from classes.sdat_parser import SDATParser
from classes.esl_parser import ESLParser
from classes.meter_data_processor import MeterDataProcessor
import os
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DataProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Processor")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10 10 10 10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.figure = plt.Figure(figsize=(12, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.process_button = ttk.Button(frame, text="Process Files", command=self.process_files)
        self.process_button.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.output_label = ttk.Label(frame, text="")
        self.output_label.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Ensure the frame expands to fill the window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

    def process_files(self):
        logging.debug("Starting file processing")
        sdat_folder = 'SDAT-Files'
        esl_folder = 'ESL-Files'

        if not os.path.exists(sdat_folder) or not os.path.exists(esl_folder):
            messagebox.showerror("Error", "Folders for SDAT or ESL files do not exist.")
            return

        sdat_files = [os.path.join(sdat_folder, file) for file in os.listdir(sdat_folder) if file.endswith('.xml')]
        esl_files = [os.path.join(esl_folder, file) for file in os.listdir(esl_folder) if file.endswith('.xml')]

        if not sdat_files or not esl_files:
            messagebox.showerror("Error", "No SDAT or ESL files found.")
            return

        with ThreadPoolExecutor() as executor:
            esl_futures = {executor.submit(self.parse_esl, file): file for file in esl_files}
            sdat_futures = {executor.submit(self.parse_sdat, file): file for file in sdat_files}

            esl_data = {esl_futures[future]: future.result() for future in esl_futures}
            sdat_data = {sdat_futures[future]: future.result() for future in sdat_futures}

        all_timestamps = []
        all_absolute_values = []

        for file, sdat_values in sdat_data.items():
            meter_data_processor = MeterDataProcessor(sdat_values, esl_data.get(file, []))
            meter_data_processor.process_data()

            for document_id, entries in meter_data_processor.processed_data.items():
                timestamps = [entry['timestamp'] for entry in entries]
                absolute_values = [entry['absolute_value'] for entry in entries]

                all_timestamps.extend(timestamps)
                all_absolute_values.extend(absolute_values)
                logging.debug(f"File {file} - Processed {len(timestamps)} entries")

        logging.debug("Visualizing data")
        self.visualize_data(all_timestamps, all_absolute_values)

    def parse_esl(self, file):
        esl_parser = ESLParser(file)
        esl_parser.parse()
        return esl_parser.get_data()

    def parse_sdat(self, file):
        sdat_parser = SDATParser(file)
        sdat_parser.parse()
        return sdat_parser.get_data()

    def visualize_data(self, timestamps, absolute_values):
        logging.debug(f"Visualizing {len(timestamps)} timestamps and {len(absolute_values)} values")
        self.ax.clear()  # Clear any previous data
        self.ax.plot(timestamps, absolute_values, label='Absolute Value', marker='o', linestyle='-')
        self.ax.set_xlabel('Timestamp')
        self.ax.set_ylabel('Absolute Value')
        self.ax.set_title('Zählerstände über Zeit')
        self.ax.legend()
        self.ax.xaxis.set_major_locator(mdates.MonthLocator())
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(self.ax.get_xticklabels(), rotation=45, ha='right')
        self.canvas.draw()

        self.output_label.config(text="Processing complete. Files have been visualized.")
        logging.debug("Visualization complete")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataProcessorApp(root)
    root.mainloop()
