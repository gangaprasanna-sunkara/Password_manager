from cryptography.fernet import Fernet  # For encryption and decryption
import os  # For checking if files exist

# ---------------------------------------
# Create and save encryption key only once
# ---------------------------------------
def write_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

# ---------------------------------------
# Load encryption key from key.key file
# ---------------------------------------
def load_key():
    with open("key.key", "rb") as file:
        return file.read()

# ---------------------------------------
# Load the encryption key and define Fernet object
# This must come BEFORE any function uses `fer`
# ---------------------------------------
write_key()
key = load_key()
fer = Fernet(key)

# ---------------------------------------
# Set up master password only once (and encrypt it)
# ---------------------------------------
def setup_master_password():
    if not os.path.exists("master.key"):
        master_pwd = input("🔐 Set your master password (only once): ")
        encrypted_pwd = fer.encrypt(master_pwd.encode())  # Encrypt master password
        with open("master.key", "wb") as f:  # Write as binary
            f.write(encrypted_pwd)
        print("✅ Master password saved successfully.")

# ---------------------------------------
# Ask user to enter master password and verify
# ---------------------------------------
def verify_master_password():
    entered = input("🔑 Enter master password to view saved passwords: ")
    with open("master.key", "rb") as f:
        encrypted_saved = f.read()
    try:
        decrypted_saved = fer.decrypt(encrypted_saved).decode()
        return entered == decrypted_saved
    except:
        return False

# ---------------------------------------
# Create master key if not already saved
# ---------------------------------------
setup_master_password()

# ---------------------------------------
# Function to view saved passwords
# ---------------------------------------
def view():
    if not verify_master_password():
        print("❌ Incorrect master password. Access denied.")
        return

    if not os.path.exists("passwords.txt"):
        print("ℹ️ No passwords saved yet.")
        return

    with open("passwords.txt", 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            if "|" in data:
                user, passw = data.split("|")
                try:
                    decrypted = fer.decrypt(passw.encode()).decode()
                    print(f"👤 User: {user} | 🔐 Password: {decrypted}")
                except Exception:
                    print(f"⚠️ Error decrypting password for user: {user}")

# ---------------------------------------
# Function to add a new password
# ---------------------------------------
def add():
    name = input("📛 Enter Account Name: ")
    pwd = input("🔐 Enter Password: ")
    encrypted = fer.encrypt(pwd.encode()).decode()
    with open("passwords.txt", 'a') as f:
        f.write(name + "|" + encrypted + "\n")
    print("✅ Password added successfully.")

# ---------------------------------------
# Main loop to show menu
# ---------------------------------------
while True:
    print("\n🔒 --- Simple Password Manager ---")
    mode = input("Choose an option: view / add / q (quit): ").lower()

    if mode == "q":
        print("👋 Goodbye!")
        break
    elif mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("⚠️ Invalid option. Please type 'view', 'add', or 'q'.")



































