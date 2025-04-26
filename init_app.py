import os
import json

def init_app():
    """Inicializa la aplicación creando los directorios y archivos necesarios"""
    # Directorios necesarios
    directories = [
        "data",
        "data/qr_codes",
        "assets"
    ]
    
    # Crear directorios si no existen
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Crear archivos JSON vacíos si no existen
    json_files = {
        "data/users.json": {},
        "data/rooms.json": {},
        "data/reservations.json": {}
    }
    
    for file_path, default_data in json_files.items():
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=4)
    
    print("Aplicación inicializada correctamente")

if __name__ == "__main__":
    init_app() 