import os
import time
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tkinter import Tk, Text, Button, END

# Folder to monitor
FOLDER_TO_MONITOR = "/home/sec-lab/Target Folder"  # Replace with the path to your target folder
LOG_FILE = "activity.log"

# Set up logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to log actions and update GUI
def log_action(action, log_text_widget=None):
    logging.info(action)
    if log_text_widget:
        refresh_log_display(log_text_widget)

# Function to refresh the log display in the GUI
def refresh_log_display(log_text_widget):
    with open(LOG_FILE, "r") as log_file:
        log_text_widget.delete(1.0, END)
        log_text_widget.insert(END, log_file.read())

# Event Handler for monitoring file changes
class EncryptionDecryptionEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Detect file changes that may indicate encryption or decryption
        for root_dir, _, files in os.walk(FOLDER_TO_MONITOR):
            for file in files:
                file_path = os.path.join(root_dir, file)
                
                if file.endswith(".enc"):
                    log_action(f"Target folder file {file} has been encrypted.")
                elif not file.endswith(".enc"):
                    log_action(f"Target folder file {file} has been decrypted.")

# Function to start monitoring with Watchdog
def start_monitoring(log_text_widget, refresh_interval=30):
    event_handler = EncryptionDecryptionEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=FOLDER_TO_MONITOR, recursive=True)
    observer.start()
    log_action("Started monitoring the target folder for encryption/decryption changes.", log_text_widget)
    
    # Auto-refresh every specified interval
    def auto_refresh():
        while observer.is_alive():
            time.sleep(refresh_interval)
            refresh_log_display(log_text_widget)

    threading.Thread(target=auto_refresh, daemon=True).start()
    return observer

# GUI setup function
def main():
    root = Tk()
    root.title("Folder Monitoring for Encryption/Decryption Changes")

    # Text widget to display logs
    log_text_widget = Text(root, height=15, width=70, state='normal')
    log_text_widget.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    refresh_log_display(log_text_widget)  # Initial display of logs

    # Start/Stop monitoring control
    observer = None

    def on_start():
        nonlocal observer
        if not observer:
            observer = start_monitoring(log_text_widget)
    
    def on_stop():
        nonlocal observer
        if observer:
            observer.stop()
            observer.join()
            observer = None
        root.destroy()  # Close the app

    def on_refresh():
        refresh_log_display(log_text_widget)

    # Start Monitoring button
    Button(root, text="Start Monitoring", command=on_start).grid(row=0, column=0, padx=5, pady=5)

    # Stop Monitoring button
    Button(root, text="End Monitoring", command=on_stop).grid(row=0, column=1, padx=5, pady=5)

    # Refresh Log button
    Button(root, text="Refresh Log", command=on_refresh).grid(row=0, column=2, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()

