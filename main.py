from gui import DataProcessorApp
import tkinter as tk
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    logging.debug("Starting application")
    root = tk.Tk()
    app = DataProcessorApp(root)
    root.mainloop()
    logging.debug("Application closed")
