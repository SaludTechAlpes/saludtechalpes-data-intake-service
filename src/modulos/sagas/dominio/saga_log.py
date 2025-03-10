from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
import uuid

@dataclass
class SagaLog:
    id_saga: str
    estado: str  # "en_progreso", "completado", "fallo"
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    eventos: List[Dict[str, str]] = field(default_factory=list)  # Lista de eventos recibidos
    comandos: List[Dict[str, str]] = field(default_factory=list)  # Lista de comandos enviados
    datos_eliminados: bool = False

    def registrar_evento(self, tipo_evento: str, estado: str):
        """Registra un evento en la saga"""
        self.eventos.append({
            "tipo": tipo_evento,
            "estado": estado,
            "fecha": datetime.utcnow().isoformat()
        })
        self.fecha_actualizacion = datetime.utcnow()

    def registrar_comando(self, tipo_comando: str, estado: str):
        """Registra un comando en la saga"""
        self.comandos.append({
            "tipo": tipo_comando,
            "estado": estado,
            "fecha": datetime.utcnow().isoformat()
        })
        self.fecha_actualizacion = datetime.utcnow()

    def completar_saga(self):
        """Marca la saga como completada"""
        self.estado = "completado"
        self.fecha_actualizacion = datetime.utcnow()

    def fallar_saga(self):
        """Marca la saga como fallida"""
        self.estado = "fallo"
        self.fecha_actualizacion = datetime.utcnow()

    def marcar_datos_eliminados(self):
        """Registra que los datos crudos han sido eliminados"""
        self.datos_eliminados = True
        self.fecha_actualizacion = datetime.utcnow()
