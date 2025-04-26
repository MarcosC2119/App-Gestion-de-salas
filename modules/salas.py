from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Sala:
    id: int
    nombre: str
    capacidad: int
    tiene_proyector: bool
    tiene_pizarra_digital: bool
    es_accesible: bool

@dataclass
class Reserva:
    id: int
    sala_id: int
    usuario_email: str
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: str  # 'activa', 'cancelada', 'completada'

class GestorSalas:
    def __init__(self):
        # Simulación de datos
        self.salas = [
            Sala(1, "Sala A101", 30, True, True, True),
            Sala(2, "Sala B202", 20, True, False, True),
            Sala(3, "Sala C303", 40, True, True, False),
            Sala(4, "Sala D404", 25, False, True, True),
        ]
        self.reservas = []
        self._next_reserva_id = 1

    def buscar_salas_disponibles(
        self,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        capacidad_min: int = 0,
        requiere_proyector: bool = False,
        requiere_pizarra: bool = False,
        requiere_accesible: bool = False
    ) -> List[Sala]:
        salas_disponibles = []
        for sala in self.salas:
            if (sala.capacidad >= capacidad_min and
                (not requiere_proyector or sala.tiene_proyector) and
                (not requiere_pizarra or sala.tiene_pizarra_digital) and
                (not requiere_accesible or sala.es_accesible)):
                
                # Verificar si la sala está disponible en el horario
                disponible = True
                for reserva in self.reservas:
                    if (reserva.sala_id == sala.id and
                        reserva.estado == 'activa' and
                        not (fecha_fin <= reserva.fecha_inicio or
                             fecha_inicio >= reserva.fecha_fin)):
                        disponible = False
                        break
                
                if disponible:
                    salas_disponibles.append(sala)
        
        return salas_disponibles

    def crear_reserva(
        self,
        sala_id: int,
        usuario_email: str,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> Optional[Reserva]:
        # Verificar disponibilidad
        sala = next((s for s in self.salas if s.id == sala_id), None)
        if not sala:
            return None

        # Crear la reserva
        reserva = Reserva(
            id=self._next_reserva_id,
            sala_id=sala_id,
            usuario_email=usuario_email,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado='activa'
        )
        self._next_reserva_id += 1
        self.reservas.append(reserva)
        return reserva

    def cancelar_reserva(self, reserva_id: int) -> bool:
        reserva = next((r for r in self.reservas if r.id == reserva_id), None)
        if reserva and reserva.estado == 'activa':
            reserva.estado = 'cancelada'
            return True
        return False

    def obtener_reservas_usuario(self, usuario_email: str) -> List[Reserva]:
        return [r for r in self.reservas if r.usuario_email == usuario_email and r.estado == 'activa']

    def obtener_historial_reservas(self, usuario_email: str) -> List[Reserva]:
        return [r for r in self.reservas if r.usuario_email == usuario_email] 