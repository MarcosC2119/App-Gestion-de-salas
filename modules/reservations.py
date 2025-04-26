from flet import *
import json
import os
from datetime import datetime, timedelta
from modules.rooms import get_room
from modules.users import get_user

# Ruta del archivo de reservas
RESERVATIONS_FILE = "data/reservations.json"
QR_DIR = "data/qr_codes"

def load_reservations():
    """Carga las reservas desde el archivo JSON"""
    if not os.path.exists(RESERVATIONS_FILE):
        return {}
    try:
        with open(RESERVATIONS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_reservations(reservations):
    """Guarda las reservas en el archivo JSON"""
    os.makedirs(os.path.dirname(RESERVATIONS_FILE), exist_ok=True)
    with open(RESERVATIONS_FILE, "w") as f:
        json.dump(reservations, f, indent=4)

def create_reservation(room_id, user_id, start_time, end_time, purpose, attendees=None):
    """Crea una nueva reserva"""
    reservations = load_reservations()
    
    # Verificar si el salón existe
    room = get_room(room_id)
    if not room:
        return False, "Salón no encontrado"
    
    # Verificar si el usuario existe
    user = get_user(user_id)
    if not user:
        return False, "Usuario no encontrado"
    
    # Verificar disponibilidad del salón
    for reservation in reservations.values():
        if reservation["room_id"] == room_id:
            # Convertir strings a datetime para comparación
            existing_start = datetime.fromisoformat(reservation["start_time"])
            existing_end = datetime.fromisoformat(reservation["end_time"])
            new_start = datetime.fromisoformat(start_time)
            new_end = datetime.fromisoformat(end_time)
            
            # Verificar superposición de horarios
            if (new_start < existing_end and new_end > existing_start):
                return False, "El salón ya está reservado en ese horario"
    
    # Crear nueva reserva
    reservation_id = str(len(reservations) + 1)
    reservations[reservation_id] = {
        "room_id": room_id,
        "user_id": user_id,
        "start_time": start_time,
        "end_time": end_time,
        "purpose": purpose,
        "attendees": attendees or [],
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    
    save_reservations(reservations)
    return True, "Reserva creada exitosamente"

def get_reservation(reservation_id):
    """Obtiene una reserva por su ID"""
    reservations = load_reservations()
    return reservations.get(reservation_id)

def get_user_reservations(user_id):
    """Obtiene todas las reservas de un usuario"""
    reservations = load_reservations()
    return {id: res for id, res in reservations.items() if res["user_id"] == user_id}

def get_room_reservations(room_id):
    """Obtiene todas las reservas de un salón"""
    reservations = load_reservations()
    return {id: res for id, res in reservations.items() if res["room_id"] == room_id}

def update_reservation(reservation_id, **kwargs):
    """Actualiza los detalles de una reserva"""
    reservations = load_reservations()
    if reservation_id not in reservations:
        return False, "Reserva no encontrada"
    
    for key, value in kwargs.items():
        if key in reservations[reservation_id]:
            reservations[reservation_id][key] = value
    
    save_reservations(reservations)
    return True, "Reserva actualizada exitosamente"

def delete_reservation(reservation_id):
    """Elimina una reserva"""
    reservations = load_reservations()
    if reservation_id not in reservations:
        return False, "Reserva no encontrada"
    
    del reservations[reservation_id]
    save_reservations(reservations)
    return True, "Reserva eliminada exitosamente"

def check_room_availability(room_id, start_time, end_time):
    """Verifica la disponibilidad de un salón en un horario específico"""
    reservations = get_room_reservations(room_id)
    new_start = datetime.fromisoformat(start_time)
    new_end = datetime.fromisoformat(end_time)
    
    for reservation in reservations.values():
        existing_start = datetime.fromisoformat(reservation["start_time"])
        existing_end = datetime.fromisoformat(reservation["end_time"])
        
        if (new_start < existing_end and new_end > existing_start):
            return False
    
    return True

def delete_qr_code(reservation_id):
    """Elimina el código QR de una reserva"""
    try:
        filename = f"{QR_DIR}/reservation_{reservation_id}.png"
        if os.path.exists(filename):
            os.remove(filename)
            return True, "Código QR eliminado exitosamente"
        return False, "Código QR no encontrado"
    except Exception as e:
        return False, f"Error al eliminar código QR: {str(e)}"

def cancelar_reserva(reservation_id, user_id):
    """Cancela una reserva (para usuarios normales)"""
    try:
        # Verificar si la reserva existe
        reservation = get_reservation(reservation_id)
        if not reservation:
            return False, "Reserva no encontrada"
        
        # Verificar si el usuario es el dueño de la reserva
        if reservation["user_id"] != user_id:
            return False, "No tienes permiso para cancelar esta reserva"
        
        # Verificar si la reserva ya está cancelada
        if reservation.get("status") == "cancelled":
            return False, "La reserva ya está cancelada"
        
        # Actualizar el estado de la reserva
        success, message = update_reservation(reservation_id, status="cancelled")
        if success:
            # Eliminar el código QR si existe
            delete_qr_code(reservation_id)
            return True, "Reserva cancelada exitosamente"
        return False, message
        
    except Exception as e:
        return False, f"Error al cancelar la reserva: {str(e)}"

def cancelar_reserva_admin(reservation_id):
    """Cancela una reserva (para administradores)"""
    try:
        # Verificar si la reserva existe
        reservation = get_reservation(reservation_id)
        if not reservation:
            return False, "Reserva no encontrada"
        
        # Verificar si la reserva ya está cancelada
        if reservation.get("status") == "cancelled":
            return False, "La reserva ya está cancelada"
        
        # Actualizar el estado de la reserva
        success, message = update_reservation(reservation_id, status="cancelled")
        if success:
            # Eliminar el código QR si existe
            delete_qr_code(reservation_id)
            return True, "Reserva cancelada exitosamente"
        return False, message
        
    except Exception as e:
        return False, f"Error al cancelar la reserva: {str(e)}" 