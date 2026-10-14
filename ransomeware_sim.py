import tkinter as tk
from tkinter import ttk, messagebox
import os
from cryptography.fernet import Fernet

# Set up a safe, sandboxed directory for testing
TARGET_DIR = os.path.join(os.getcwd(), "ransomware_test_env")
KEY_FILE = "symmetric_key.key"

def setup_environment():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        
    # Create sample files to encrypt
    files_to_create = {
        "financial_report.txt": "Q3 Revenue: $4.2M. Confidential.",
        "passwords.txt": "admin:Hunter2!\nroot:supersecret",
        "employee_data.csv": "ID,Name,Role\n001,Jone,SOC Analyst"
    }
    
    for filename, content in files_to_create.items():
        filepath = os.path.join(TARGET_DIR, filename)
        with open(filepath, "w") as f:
            f.write(content)
            
    insert_log(f"[+] Sandboxed test environment created at:\n    {TARGET_DIR}\n", "success")
    update_file_list()

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    insert_log("[+] Symmetric encryption key generated and saved locally.\n", "success")

def load_key():
    if not os.path.exists(KEY_FILE):
        return None
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def execute_ransomware():
    key = load_key()
    if not key:
        insert_log("[-] No encryption key found! Generating one now...\n", "warning")
        generate_key()
        key = load_key()

    f = Fernet(key)
    
    if not os.path.exists(TARGET_DIR) or not os.listdir(TARGET_DIR):
        messagebox.showwarning("Empty Directory", "Please setup the test environment first.")
        return

    btn_encrypt.config(state=tk.DISABLED)
    insert_log("[!] INITIATING ENCRYPTION ROUTINE...\n", "error")
    
    for root_dir, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            # Prevent double-encryption
            if file.endswith(".LOCKED"):
                continue
                
            filepath = os.path.join(root_dir, file)
            
            # Read plaintext
            with open(filepath, "rb") as original_file:
                original_data = original_file.read()
                
            # Encrypt data
            encrypted_data = f.encrypt(original_data)
            
            # Write ciphertext and rename
            with open(filepath, "wb") as encrypted_file:
                encrypted_file.write(encrypted_data)
                
            os.rename(filepath, filepath + ".LOCKED")
            insert_log(f"  [LOCKED] {file}\n", "error")
            
    insert_log("[!] FILES ENCRYPTED. SIMULATION COMPLETE.\n\n", "error")
    update_file_list()
    btn_encrypt.config(state=tk.NORMAL)

def execute_decryption():
    key = load_key()
    if not key:
        insert_log("[-] Decryption key missing! Files are permanently lost.\n", "error")
        return

    f = Fernet(key)
    
    btn_decrypt.config(state=tk.DISABLED)
    insert_log("[*] INITIATING DECRYPTION ROUTINE...\n", "success")
    
    for root_dir, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if not file.endswith(".LOCKED"):
                continue
                
            filepath = os.path.join(root_dir, file)
            
            # Read ciphertext
            with open(filepath, "rb") as encrypted_file:
                encrypted_data = encrypted_file.read()
                
            # Decrypt data
            try:
                decrypted_data = f.decrypt(encrypted_data)
            except Exception:
                insert_log(f"  [FAILED] Invalid key for {file}\n", "error")
                continue
                
            # Write plaintext and restore name
            with open(filepath, "wb") as decrypted_file:
                decrypted_file.write(decrypted_data)
                
            original_filepath = filepath.replace(".LOCKED", "")
            os.rename(filepath, original_filepath)
            insert_log(f"  [UNLOCKED] {os.path.basename(original_filepath)}\n", "success")
            
    insert_log("[*] FILES RESTORED. INCIDENT RESOLVED.\n\n", "success")
    update_file_list()
    btn_decrypt.config(state=tk.NORMAL)

def update_file_list():
    listbox_files.delete(0, tk.END)
    if os.path.exists(TARGET_DIR):
        for file in os.listdir(TARGET_DIR):
            listbox_files.insert(tk.END, f"  {file}")

def insert_log(message, tag=None):
    text_output.config(state=tk.NORMAL)
    if tag:
        text_output.insert(tk.END, message, tag)
    else:
        text_output.insert(tk.END, message)
    text_output.see(tk.END)
    text_output.config(state=tk.DISABLED)

# --- Tkinter GUI Layout ---
root = tk.Tk()
root.title("SOC Toolkit - Ransomware Simulator")
root.geometry("650x650")
root.resizable(False, False)

frame = ttk.Frame(root, padding="15")
frame.pack(fill=tk.BOTH, expand=True)

lbl_title = tk.Label(frame, text="Educational Ransomware Simulator", font=("Helvetica", 13, "bold"))
lbl_title.pack(anchor="w", pady=(0, 5))

lbl_desc = tk.Label(frame, text="Safely demonstrates AES symmetric file encryption/decryption in a sandboxed folder.", font=("Helvetica", 9), fg="#555")
lbl_desc.pack(anchor="w", pady=(0, 15))

# Controls
control_frame = tk.Frame(frame)
control_frame.pack(fill=tk.X, pady=(0, 10))

btn_setup = tk.Button(control_frame, text="1. Setup Test Env", command=setup_environment, bg="#8e44ad", fg="white", font=("Helvetica", 9, "bold"), width=15)
btn_setup.pack(side=tk.LEFT, padx=(0, 10))

btn_encrypt = tk.Button(control_frame, text="2. Execute Ransomware", command=execute_ransomware, bg="#c0392b", fg="white", font=("Helvetica", 9, "bold"), width=20)
btn_encrypt.pack(side=tk.LEFT, padx=(0, 10))

btn_decrypt = tk.Button(control_frame, text="3. Decrypt & Restore", command=execute_decryption, bg="#27ae60", fg="white", font=("Helvetica", 9, "bold"), width=20)
btn_decrypt.pack(side=tk.LEFT)

# File viewer
tk.Label(frame, text="Sandboxed Directory Contents:", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(10, 2))
listbox_files = tk.Listbox(frame, height=5, font=("Consolas", 10), bg="#f4f6f7")
listbox_files.pack(fill=tk.X, pady=(0, 15))

# Output Console
tk.Label(frame, text="Incident Response Logs:", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(0, 2))
text_frame = tk.Frame(frame)
text_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_output = tk.Text(text_frame, font=("Consolas", 10), bg="#1e1e1e", fg="#ecf0f1", yscrollcommand=scrollbar.set)
text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
text_output.tag_config("success", foreground="#2ecc71")
text_output.tag_config("error", foreground="#e74c3c", font=("Consolas", 10, "bold"))
text_output.tag_config("warning", foreground="#f1c40f")
text_output.config(state=tk.DISABLED)
scrollbar.config(command=text_output.yview)

# Initial load
setup_environment()

root.mainloop()