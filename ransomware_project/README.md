# Ransomware Simulation Project

This project simulates the lifecycle of a ransomware attack within a controlled virtual environment, implementing a multi-layered defense system. It covers phishing simulations, AES encryption, monitoring, anomaly detection, and automated backup restoration to showcase a comprehensive ransomware attack and defense cycle.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Setup Instructions](#setup-instructions)
3. [Step-by-Step Execution](#step-by-step-execution)
    - [1. Phishing Simulation](#1-phishing-simulation)
    - [2. AES Encryption/Decryption](#2-aes-encryptiondecryption)
    - [3. Real-Time Monitoring with Watchdog](#3-real-time-monitoring-with-watchdog)
    - [4. Anomaly Detection via Hash Comparison](#4-anomaly-detection-via-hash-comparison)
    - [5. Automated Backup Restoration](#5-automated-backup-restoration)
4. [Libraries and Dependencies](#libraries-and-dependencies)
5. [References](#references)

---

## Project Overview
The ransomware project mimics a real ransomware attack by executing encryption, monitoring, detection, and mitigation phases, emphasizing defense strategies within a secure virtual environment:
- **Phishing Simulation**: Hosts a phishing webpage on GitHub to simulate ransomware distribution.
- **AES Encryption**: Encrypts files within a target directory, reflecting a typical ransomware attack.
- **Monitoring Tool**: Real-time monitoring using the Watchdog library to detect unauthorized file changes.
- **Anomaly Detection**: Uses hash comparison to identify abnormal changes in files within the target directory.
- **Backup and Mitigation**: Restores encrypted files from a backup to minimize the impact of the ransomware.

## Setup Instructions
1. **Create Virtual Environment**: Work within a virtual machine (VM) to maintain isolation.
2. **Python Virtual Environment**: Set up a Python virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate

Install Required Libraries: Install required libraries using pip:


pip install cryptography watchdog
Step-by-Step Execution


1. Phishing Simulation
Purpose: The GitHub-hosted webpage simulates a phishing attack by offering a fake promotional download link.
Code: The HTML file (index.html) includes a clickable iPhone image and download link.
Deployment: Host the file on GitHub or another web server.
Instructions:
Create index.html using the provided code.
Upload to GitHub and link to the download file (e.g., WalmartAppInstaller.exe).
Note: This step only simulates phishing for educational purposes; do not distribute malicious software.


2. AES Encryption/Decryption
Purpose: Encrypt files in a specified folder using AES encryption, simulating ransomware data lockdown.
Files:
encrypt.py handles encryption.
decrypt.py prompts the user for a password and handles decryption.
encrypt_decrypt_app.py provides a GUI-based encryption-decryption application.
Execution:


python encrypt.py
python decrypt.py
Explanation:
Encryption: Encrypts all files within the target folder, adding a .enc extension.
Decryption: Decrypts files after prompting for a password and removes the .enc extension.
3. Real-Time Monitoring with Watchdog
Purpose: The Watchdog library monitors file changes, alerting on unauthorized modifications.
File: monitoring_app.py
Execution:


python monitoring_app.py
Functionality: Logs file changes in the target folder every 30 seconds. The GUI includes buttons for start/stop monitoring and refresh logs.
4. Anomaly Detection via Hash Comparison
Purpose: Detects unauthorized file modifications using hash comparisons.
File: detection_app.py
Execution:


python detection_app.py
Functionality: Compares current file hashes against initial values to flag unauthorized changes, with real-time updates every 30 seconds.
5. Automated Backup Restoration
Purpose: Automatically restores the target directory from a secure backup when ransomware is detected.
File: mitigation_app.py
Execution:


python mitigation_app.py
Functionality:
Creates a backup of the target directory.
Detects unauthorized changes and restores affected files from the backup.
GUI includes buttons for start/stop mitigation with real-time log display for ransomware activity.
Libraries and Dependencies
cryptography: Provides AES encryption/decryption.


pip install cryptography
watchdog: Monitors file changes and detects unauthorized access.


pip install watchdog
tkinter: Python’s GUI toolkit, used to display interactive elements.
