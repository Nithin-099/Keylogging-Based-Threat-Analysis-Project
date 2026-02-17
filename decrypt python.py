from cryptography.fernet import Fernet
def decrypt_file():
key = open("key.key", "rb").read()
fernet = Fernet(key)
with open("keylog_encrypted.txt", "rb") asf:
lines = f.readlines()
print("\n---Decrypted Log Content---\n")
for line in lines:
line = line.strip() # remove trailing newline
if line: # avoid empty lines
try:
decrypted = fernet.decrypt(line)
print(decrypted.decode(), end='') # use end='' to preserve formatting
except Exception as e:
print(f"[Failed to decrypt a line: {e}]")
decrypt_file()
