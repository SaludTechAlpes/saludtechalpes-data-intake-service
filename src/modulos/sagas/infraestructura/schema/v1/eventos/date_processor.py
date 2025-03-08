from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class DatosAnonimizadosFallidoPayload(Record):
    id_imagen = String()

class EventoDatosAnonimizadosFallido(EventoIntegracion):
    data = DatosAnonimizadosFallidoPayload()
