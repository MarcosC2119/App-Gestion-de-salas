from flet import *
import json
import os
from datetime import datetime
import hashlib

# Ruta del archivo de usuarios
USERS_FILE = "data/users.json"

def load_users():
    """Carga los usuarios desde el archivo JSON"""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    """Guarda los usuarios en el archivo JSON"""
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    """Hashea una contraseña usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email, password, name, role="teacher"):
    """Crea un nuevo usuario"""
    users = load_users()
    
    # Verificar si el email ya existe
    for user in users.values():
        if user["email"].lower() == email.lower():
            return False, "Ya existe un usuario con ese email"
    
    # Crear nuevo usuario
    user_id = str(len(users) + 1)
    users[user_id] = {
        "email": email,
        "password": hash_password(password),
        "name": name,
        "role": role,
        "created_at": datetime.now().isoformat(),
        "last_login": None
    }
    
    save_users(users)
    return True, "Usuario creado exitosamente"

def authenticate_user(email, password):
    """Autentica un usuario"""
    users = load_users()
    for user_id, user in users.items():
        if user["email"].lower() == email.lower() and user["password"] == hash_password(password):
            # Actualizar último login
            user["last_login"] = datetime.now().isoformat()
            save_users(users)
            return True, user_id, user
    return False, None, None

def get_user(user_id):
    """Obtiene un usuario por su ID"""
    users = load_users()
    return users.get(user_id)

def update_user(user_id, **kwargs):
    """Actualiza los detalles de un usuario"""
    users = load_users()
    if user_id not in users:
        return False, "Usuario no encontrado"
    
    for key, value in kwargs.items():
        if key in users[user_id]:
            if key == "password":
                users[user_id][key] = hash_password(value)
            else:
                users[user_id][key] = value
    
    save_users(users)
    return True, "Usuario actualizado exitosamente"

def delete_user(user_id):
    """Elimina un usuario"""
    users = load_users()
    if user_id not in users:
        return False, "Usuario no encontrado"
    
    del users[user_id]
    save_users(users)
    return True, "Usuario eliminado exitosamente" 