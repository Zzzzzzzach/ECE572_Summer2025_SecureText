import json
import os
import base64
import bcrypt

USER_FILE = "./../../users.json"

def generate_salt():
    return base64.b64encode(os.urandom(16)).decode('utf-8')

def hash_password(password, salt):
    combined = (password + salt).encode('utf-8')
    return bcrypt.hashpw(combined, bcrypt.gensalt(rounds=12)).decode('utf-8')

with open(USER_FILE, "r", encoding="utf-8") as f:
    users = json.load(f)

updated_count = 0

for username, user_data in users.items():
    hash_method = user_data.get("hash_method", "plaintext")
    
    if hash_method == "plaintext":
        plaintext_password = user_data["password"]
        salt = generate_salt()
        hashed = hash_password(plaintext_password, salt)

        user_data["password"] = hashed
        user_data["salt"] = salt
        user_data["hash_method"] = "bcrypt"

        updated_count += 1

with open(USER_FILE, "w", encoding="utf-8") as f:
    json.dump(users, f, indent=2)

print(f"Migrated {updated_count} user(s) to bcrypt with salt.")
