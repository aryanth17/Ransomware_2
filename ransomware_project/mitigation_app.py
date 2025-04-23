import os
import shutil
import hashlib
import time
from tkinter import Tk, Text, Button, END, messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Paths for the folder to monitor and the backup folder
FOLDER_TO_MONITOR = "/home/sec-lab/Target Folder"  # Replace with your target folder path
BACKUP_FOLDER = "/home/sec-lab/Target Folder Backup"  # Replace with your backup folder path

# Create backup folder if it doesn't exist
if not os.path.exists(BACKUP_FOLDER):
    os.makedirs(BACKUP_FOLDER)

# Function to create an initial backup
def create_backup():
    for root_dir, _, files in os.walk(FOLDER_TO_MONITOR):
        for file in files:
            src_file = os.path.join(root_dir, file)
            dest_file = os.path.join(BACKUP_FOLDER, file)
            shutil.copy2(src_file, dest_file)

# Function to restore files from the backup
def restore_from_backup():
    for root_dir, _, files in os.walk(BACKUP_FOLDER):
        for file in files:
            backup_file = os.path.join(root_dir, file)
            target_file = os.path.join(FOLDER_TO_MONITOR, file)
            shutil.copy2(backup_file, target_file)

# Function to calculate file hash for integrity checking
def calculate_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Store initial file hashes for comparison
initial_hashes = {os.path.join(root_dir, file): calculate_file_hash(os.path.join(root_dir, file))
                  for root_dir, _, files in os.walk(FOLDER_TO_MONITOR) for file in files}

# Event handler for monitoring and mitigation
class MitigationEventHandler(FileSystemEventHandler):
    def __init__(self, log_display):
        self.log_display = log_display

    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            new_hash = calculate_file_hash(file_path)
            original_hash = initial_hashes.get(file_path)
            
            # If file is modified and hash doesn't match, trigger mitigation
            if original_hash and new_hash != original_hash:
                self.log_action(f"Unauthorized change detected in {file_path}. Restoring from backup.")
                restore_from_backup()  # Restore the modified file from backup
                initial_hashes[file_path] = new_hash  # Update the hash to prevent repeated restoration

    def log_action(self, action):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {action}\n"
        self.log_display.insert(END, log_message)
        self.log_display.see(END)

# GUI application for mitigation
class MitigationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mitigation Monitoring")
        self.log_display = Text(root, height=20, width=80)
        self.log_display.pack()

        # Buttons for control
        self.start_button = Button(root, text="Start Mitigation", command=self.start_mitigation)
        self.start_button.pack(side="left", padx=5, pady=5)

        self.stop_button = Button(root, text="Stop Mitigation", command=self.stop_mitigation)
        self.stop_button.pack(side="right", padx=5, pady=5)

        self.observer = None
        create_backup()  # Create initial backup

    def start_mitigation(self):
        if self.observer is None:
            event_handler = MitigationEventHandler(self.log_display)
            self.observer = Observer()
            self.observer.schedule(event_handler, FOLDER_TO_MONITOR, recursive=True)
            self.observer.start()
            self.log_action("Mitigation started with real-time monitoring for unauthorized changes.")

    def stop_mitigation(self):
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.log_action("Mitigation stopped.")
            messagebox.showinfo("Mitigation Monitoring", "Mitigation has been stopped.")
            self.root.quit()  # Close the application

    def log_action(self, action):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {action}\n"
        self.log_display.insert(END, log_message)
        self.log_display.see(END)

if __name__ == "__main__":
    root = Tk()
    app = MitigationApp(root)
    root.mainloop()

