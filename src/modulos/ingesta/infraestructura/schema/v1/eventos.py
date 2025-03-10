from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class EventoDatosImportadosPayload(Record):
    id_imagen_importada = String()
    ruta_imagen_importada = String()
    ruta_metadatos_importados = String()
    evento_a_fallar = String()

class EventoDatosImportados(EventoIntegracion):
    data = EventoDatosImportadosPayload()

class EventoDatosImportadosFallidoPayload(Record):
    id_imagen_importada = String()
class EventoDatosImportadosFallido(EventoIntegracion):
    data = EventoDatosImportadosFallidoPayload()