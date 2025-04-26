from flet import *
import json
import os
from datetime import datetime

# Ruta del archivo de salones
ROOMS_FILE = "data/rooms.json"

def load_rooms():
    """Carga los salones desde el archivo JSON"""
    if not os.path.exists(ROOMS_FILE):
        return {}
    try:
        with open(ROOMS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_rooms(rooms):
    """Guarda los salones en el archivo JSON"""
    os.makedirs(os.path.dirname(ROOMS_FILE), exist_ok=True)
    with open(ROOMS_FILE, "w") as f:
        json.dump(rooms, f, indent=4)

def create_room(name, capacity, location, equipment=None, status="available"):
    """Crea un nuevo salón"""
    rooms = load_rooms()
    
    # Verificar si el salón ya existe
    for room in rooms.values():
        if room["name"].lower() == name.lower():
            return False, "Ya existe un salón con ese nombre"
    
    # Crear nuevo salón
    room_id = str(len(rooms) + 1)
    rooms[room_id] = {
        "name": name,
        "capacity": capacity,
        "location": location,
        "equipment": equipment or [],
        "status": status,
        "created_at": datetime.now().isoformat()
    }
    
    save_rooms(rooms)
    return True, "Salón creado exitosamente"

def get_room(room_id):
    """Obtiene un salón por su ID"""
    rooms = load_rooms()
    return rooms.get(room_id)

def get_all_rooms():
    """Obtiene todos los salones"""
    return load_rooms()

def update_room(room_id, **kwargs):
    """Actualiza los detalles de un salón"""
    rooms = load_rooms()
    if room_id not in rooms:
        return False, "Salón no encontrado"
    
    for key, value in kwargs.items():
        if key in rooms[room_id]:
            rooms[room_id][key] = value
    
    save_rooms(rooms)
    return True, "Salón actualizado exitosamente"

def delete_room(room_id):
    """Elimina un salón"""
    rooms = load_rooms()
    if room_id not in rooms:
        return False, "Salón no encontrado"
    
    del rooms[room_id]
    save_rooms(rooms)
    return True, "Salón eliminado exitosamente" 