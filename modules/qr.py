import qrcode
from PIL import Image
import io
import json
from datetime import datetime
import os
from modules.reservations import get_reservation
from modules.rooms import get_room

# Directorio para almacenar los códigos QR
QR_DIR = "data/qr_codes"

class QRManager:
    @staticmethod
    def generar_qr(
        reserva_id: int,
        sala_id: int,
        usuario_email: str,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> bytes:
        try:
            # Crear el contenido del QR
            contenido = {
                "reserva_id": reserva_id,
                "sala_id": sala_id,
                "usuario_email": usuario_email,
                "fecha_inicio": fecha_inicio.isoformat(),
                "fecha_fin": fecha_fin.isoformat()
            }

            # Generar el código QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(json.dumps(contenido))
            qr.make(fit=True)

            # Crear la imagen
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convertir la imagen a bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            return img_byte_arr
        except Exception as e:
            print(f"Error al generar QR: {str(e)}")
            return None

    @staticmethod
    def validar_qr(qr_data: str) -> dict:
        """
        Valida y decodifica la información del código QR.
        
        Args:
            qr_data: Datos del código QR en formato JSON
            
        Returns:
            dict: Información decodificada o None si es inválida
        """
        try:
            data = json.loads(qr_data)
            # Verificar que todos los campos necesarios estén presentes
            required_fields = ["reserva_id", "sala_id", "usuario_email", 
                             "fecha_inicio", "fecha_fin"]
            if all(field in data for field in required_fields):
                # Convertir strings de fecha a datetime
                data["fecha_inicio"] = datetime.fromisoformat(data["fecha_inicio"])
                data["fecha_fin"] = datetime.fromisoformat(data["fecha_fin"])
                return data
            return None
        except Exception as e:
            print(f"Error al validar QR: {str(e)}")
            return None

def generate_qr_code(reservation_id):
    """Genera un código QR para una reserva"""
    try:
        # Verificar si la reserva existe
        reservation = get_reservation(reservation_id)
        if not reservation:
            return False, "Reserva no encontrada"
        
        # Verificar si el salón existe
        room = get_room(reservation["room_id"])
        if not room:
            return False, "Salón no encontrado"
        
        # Crear directorio si no existe
        os.makedirs(QR_DIR, exist_ok=True)
        
        # Crear el contenido del QR
        qr_content = {
            "reservation_id": reservation_id,
            "room_id": reservation["room_id"],
            "room_name": room["name"],
            "start_time": reservation["start_time"],
            "end_time": reservation["end_time"],
            "purpose": reservation["purpose"]
        }
        
        # Generar el código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(qr_content))
        qr.make(fit=True)
        
        # Crear la imagen
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Guardar la imagen
        filename = f"{QR_DIR}/reservation_{reservation_id}.png"
        img.save(filename)
        
        return True, filename
    except Exception as e:
        return False, f"Error al generar código QR: {str(e)}"

def scan_qr_code(image_path):
    """Escanea un código QR desde una imagen"""
    try:
        from pyzbar.pyzbar import decode
        from PIL import Image
        
        # Verificar si la imagen existe
        if not os.path.exists(image_path):
            return False, "Imagen no encontrada"
        
        # Decodificar el código QR
        img = Image.open(image_path)
        decoded = decode(img)
        
        if not decoded:
            return False, "No se pudo decodificar el código QR"
        
        # Obtener el contenido del QR
        qr_content = json.loads(decoded[0].data.decode())
        
        # Verificar si la reserva existe
        reservation = get_reservation(qr_content["reservation_id"])
        if not reservation:
            return False, "Reserva no encontrada"
        
        # Verificar si el salón existe
        room = get_room(qr_content["room_id"])
        if not room:
            return False, "Salón no encontrado"
        
        # Verificar si la reserva está activa
        current_time = datetime.now()
        start_time = datetime.fromisoformat(reservation["start_time"])
        end_time = datetime.fromisoformat(reservation["end_time"])
        
        if current_time < start_time:
            return False, "La reserva aún no ha comenzado"
        elif current_time > end_time:
            return False, "La reserva ya ha finalizado"
        
        return True, {
            "reservation": reservation,
            "room": room
        }
        
    except ImportError:
        return False, "Módulo pyzbar no instalado. Ejecute: pip install pyzbar"
    except Exception as e:
        return False, f"Error al escanear el código QR: {str(e)}"

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