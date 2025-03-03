from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class EventoDatosImportadosPayload(Record):
    ruta_imagen = String()
    ruta_metadatos = String()

class EventoDatosImportados(EventoIntegracion):
    data = EventoDatosImportadosPayload()