from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class DatosAnonimizadosPayload(Record):
    id_imagen_importada = String()
    id_imagen_anonimizada = String()
    ruta_imagen_anonimizada = String()
    id_paciente = String()
    modalidad = String()
    region_anatomica = String()
    fecha_estudio = Long()
    etiquetas_patologicas = Array(String())
    evento_a_fallar = String()

class EventoDatosAnonimizados(EventoIntegracion):
    data = DatosAnonimizadosPayload()

class DatosAnonimizadosFallidoPayload(Record):
    id_imagen_importada = String()
    id_imagen_anonimizada = String()

class EventoDatosAnonimizadosFallido(EventoIntegracion):
    data = DatosAnonimizadosFallidoPayload()

class DatosAgrupadosPayload(Record):
    id_imagen_importada = String()
    id_imagen_anonimizada = String()
    id_imagen_mapeada = String()
    cluster_id = String()
    ruta_imagen_anonimizada = String()
    evento_a_fallar = String()

class EventoDatosAgrupados(EventoIntegracion):
    data = DatosAgrupadosPayload()

class DatosAgrupadosFallidoPayload(Record):
    id_imagen_importada = String()
    id_imagen_anonimizada = String()
    id_imagen_mapeada = String()

class EventoDatosAgrupadosFallido(EventoIntegracion):
    data = DatosAgrupadosFallidoPayload()