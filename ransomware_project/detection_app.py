import os
import hashlib
import time
from tkinter import Tk, Text, Button, END, messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Folder to monitor and authorized activity hours
FOLDER_TO_MONITOR = "/home/sec-lab/Target Folder"
AUTHORIZED_HOURS = range(9, 18)  # 9 AM to 6 PM

# Function to calculate file hash with error handling for missing files
def calculate_file_hash(filepath):
    if not os.path.exists(filepath):
        return None  # Return None if file does not exist
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Store initial file hashes for comparison
initial_hashes = {}
for root_dir, _, files in os.walk(FOLDER_TO_MONITOR):
    for file in files:
        file_path = os.path.join(root_dir, file)
        initial_hashes[file_path] = calculate_file_hash(file_path)

# Event handler class for monitoring
class TargetFolderEventHandler(FileSystemEventHandler):
    def __init__(self, log_display):
        self.log_display = log_display

    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            new_hash = calculate_file_hash(file_path)

            # Check if file exists and hash can be calculated
            if new_hash is None:
                self.log_action(f"File {file_path} not found or deleted.")
                return  # Skip to the next file if not found

            original_hash = initial_hashes.get(file_path)
            if original_hash and new_hash != original_hash:
                self.log_action(f"Unauthorized change detected in {file_path}")
                initial_hashes[file_path] = new_hash  # Update hash after detection

            # Time-based check
            current_hour = datetime.now().hour
            if current_hour not in AUTHORIZED_HOURS:
                self.log_action(f"Unauthorized activity outside of authorized hours on {file_path}")

    def log_action(self, action):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {action}\n"
        self.log_display.insert(END, log_message)
        self.log_display.see(END)

# GUI Application for Detection
class DetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detection Monitoring")
        self.log_display = Text(root, height=20, width=80)
        self.log_display.pack()

        # Buttons for control
        self.start_button = Button(root, text="Start Detection", command=self.start_detection)
        self.start_button.pack(side="left", padx=5, pady=5)

        self.stop_button = Button(root, text="Stop Detection", command=self.stop_detection)
        self.stop_button.pack(side="right", padx=5, pady=5)

        self.refresh_button = Button(root, text="Refresh Logs", command=self.refresh_logs)
        self.refresh_button.pack(side="bottom", pady=5)

        self.observer = None

    def start_detection(self):
        if self.observer is None:
            event_handler = TargetFolderEventHandler(self.log_display)
            self.observer = Observer()
            self.observer.schedule(event_handler, FOLDER_TO_MONITOR, recursive=True)
            self.observer.start()
            self.log_action("Detection started for unauthorized access.")

    def stop_detection(self):
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.log_action("Detection stopped.")
            messagebox.showinfo("Detection Monitoring", "Detection has been stopped.")
            self.root.quit()  # Close the application

    def refresh_logs(self):
        self.log_display.insert(END, "Log refreshed\n")
        self.log_display.see(END)

    def log_action(self, action):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {action}\n"
        self.log_display.insert(END, log_message)
        self.log_display.see(END)

if __name__ == "__main__":
    root = Tk()
    app = DetectionApp(root)
    root.mainloop()

