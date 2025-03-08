from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class EventoDatosImportadosFallidoPayload(Record):
    ruta_imagen = String()
    ruta_metadatos = String()

class EventoDatosImportadosFallido(EventoIntegracion):
    data = EventoDatosImportadosFallidoPayload()