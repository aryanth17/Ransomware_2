import smtplib
import tkinter as tk
from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email():
    # Get values from entry fields
    sender_email = sender_entry.get()
    sender_password = password_entry.get()
    target_email = target_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", tk.END)
    
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = target_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Establish a secure session with the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, target_email, text)
        server.quit()
        
        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email:\n{e}")

# Create the main window
window = tk.Tk()
window.title("Email Sender")

# Labels and entry fields
tk.Label(window, text="Your Email:").grid(row=0, column=0, sticky=tk.W)
sender_entry = tk.Entry(window, width=30)
sender_entry.grid(row=0, column=1)

tk.Label(window, text="Password:").grid(row=1, column=0, sticky=tk.W)
password_entry = tk.Entry(window, width=30, show="*")
password_entry.grid(row=1, column=1)

tk.Label(window, text="Target Email:").grid(row=2, column=0, sticky=tk.W)
target_entry = tk.Entry(window, width=30)
target_entry.grid(row=2, column=1)

tk.Label(window, text="Subject:").grid(row=3, column=0, sticky=tk.W)
subject_entry = tk.Entry(window, width=30)
subject_entry.grid(row=3, column=1)

tk.Label(window, text="Body:").grid(row=4, column=0, sticky=tk.N)
body_text = tk.Text(window, height=10, width=30)
body_text.grid(row=4, column=1)

# Send button
send_button = tk.Button(window, text="Send Email", command=send_email)
send_button.grid(row=5, column=1, pady=10)

# Start the GUI loop
window.mainloop()

