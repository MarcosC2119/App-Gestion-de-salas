from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Tutorial:
    id: int
    titulo: str
    descripcion: str
    duracion: str
    url: str

@dataclass
class ProgresoUsuario:
    usuario_email: str
    tutoriales_completados: List[int]
    ultimo_acceso: datetime

class GestorCapacitacion:
    def __init__(self):
        self.tutoriales = [
            Tutorial(1, "Introducción al Sistema", 
                    "Aprende los conceptos básicos del sistema de reservas",
                    "10 minutos",
                    "https://example.com/tutorial1"),
            Tutorial(2, "Cómo Reservar una Sala", 
                    "Guía paso a paso para realizar una reserva",
                    "15 minutos",
                    "https://example.com/tutorial2"),
            Tutorial(3, "Uso del Escáner QR", 
                    "Aprende a utilizar el escáner QR para verificar reservas",
                    "8 minutos",
                    "https://example.com/tutorial3"),
        ]
        self.tutoriales_completados = {}  # usuario_email -> set(tutorial_ids)
        self.progreso_usuarios = {}

    def obtener_tutoriales(self) -> List[Tutorial]:
        return self.tutoriales

    def obtener_tutoriales_pendientes(self, usuario_email: str) -> List[Tutorial]:
        completados = self.tutoriales_completados.get(usuario_email, set())
        return [t for t in self.tutoriales if t.id not in completados]

    def obtener_progreso(self, usuario_email: str) -> float:
        completados = len(self.tutoriales_completados.get(usuario_email, set()))
        total = len(self.tutoriales)
        return (completados / total) * 100 if total > 0 else 0

    def marcar_completado(self, usuario_email: str, tutorial_id: int) -> bool:
        if usuario_email not in self.tutoriales_completados:
            self.tutoriales_completados[usuario_email] = set()
        self.tutoriales_completados[usuario_email].add(tutorial_id)
        return True

    def obtener_progreso_usuario(self, usuario_email: str) -> ProgresoUsuario:
        if usuario_email not in self.progreso_usuarios:
            return ProgresoUsuario(
                usuario_email=usuario_email,
                tutoriales_completados=[],
                ultimo_acceso=datetime.now()
            )
        return self.progreso_usuarios[usuario_email]

    def actualizar_progreso_usuario(self, usuario_email: str, tutorial_id: int) -> bool:
        if usuario_email not in self.progreso_usuarios:
            self.progreso_usuarios[usuario_email] = ProgresoUsuario(
                usuario_email=usuario_email,
                tutoriales_completados=[],
                ultimo_acceso=datetime.now()
            )
        
        if tutorial_id not in self.progreso_usuarios[usuario_email].tutoriales_completados:
            self.progreso_usuarios[usuario_email].tutoriales_completados.append(tutorial_id)
            return True
        return False

    def actualizar_progreso_usuario_completo(self, usuario_email: str) -> bool:
        if usuario_email not in self.progreso_usuarios:
            self.progreso_usuarios[usuario_email] = ProgresoUsuario(
                usuario_email=usuario_email,
                tutoriales_completados=[],
                ultimo_acceso=datetime.now()
            )
        
        self.progreso_usuarios[usuario_email].tutoriales_completados = [t.id for t in self.tutoriales]
        return True

    def actualizar_ultimo_acceso(self, usuario_email: str) -> bool:
        if usuario_email not in self.progreso_usuarios:
            self.progreso_usuarios[usuario_email] = ProgresoUsuario(
                usuario_email=usuario_email,
                tutoriales_completados=[],
                ultimo_acceso=datetime.now()
            )
        
        self.progreso_usuarios[usuario_email].ultimo_acceso = datetime.now()
        return True 