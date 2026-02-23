import json
import os

# Foydalanuvchilar saqlanadigan fayl nomi
USER_FILE = "users.json"

# users dictionary (global)
users = {}

# Fayldan usersni o‘qish
if os.path.exists(USER_FILE):
    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
    except json.JSONDecodeError:
        users = {}
else:
    users = {}

# Foydalanuvchi qo‘shish funksiyasi
def add_user(user_id, username, first_name):
    user_id = str(user_id)
    if user_id not in users:
        users[user_id] = {"username": username, "first_name": first_name}
        save_users()

# Usersni faylga yozish funksiyasi
def save_users():
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# Users sonini olish
def get_users():
    return users