from flet import *
import json
import os
from datetime import datetime

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

def authenticate_user(email, password):
    """Autentica un usuario con email y contraseña"""
    users = load_users()
    if email in users and users[email]["password"] == password:
        return {
            "email": email,
            "role": users[email]["role"],
            "name": users[email]["name"]
        }
    return None

def create_user(email, password, role, name):
    """Crea un nuevo usuario"""
    users = load_users()
    if email in users:
        return False, "El usuario ya existe"
    
    users[email] = {
        "password": password,
        "role": role,
        "name": name,
        "created_at": datetime.now().isoformat()
    }
    save_users(users)
    return True, "Usuario creado exitosamente"

def update_user(email, **kwargs):
    """Actualiza los datos de un usuario"""
    users = load_users()
    if email not in users:
        return False, "Usuario no encontrado"
    
    for key, value in kwargs.items():
        if key in users[email]:
            users[email][key] = value
    
    save_users(users)
    return True, "Usuario actualizado exitosamente"

def delete_user(email):
    """Elimina un usuario"""
    users = load_users()
    if email not in users:
        return False, "Usuario no encontrado"
    
    del users[email]
    save_users(users)
    return True, "Usuario eliminado exitosamente"

class Auth:
    @staticmethod
    def login(email: str, password: str) -> tuple[bool, str]:
        # Simulación de autenticación
        if email == "docente@test.com" and password == "123456":
            return True, "docente"
        elif email == "admin@test.com" and password == "123456":
            return True, "administrativo"
        return False, None

    @staticmethod
    def cambiar_contrasena(email: str, current_password: str, new_password: str) -> bool:
        # Simulación de cambio de contraseña
        return True

    @staticmethod
    def enviar_codigo_recuperacion(email: str) -> bool:
        # Simulación de envío de código de recuperación
        return True 