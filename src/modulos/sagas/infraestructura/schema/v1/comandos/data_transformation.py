from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class ComandoEjecutarModelosPayload(Record):
    cluster_id = String()
    ruta_imagen_anonimizada = String()

class ComandoEjecutarModelos(ComandoIntegracion):
    data = ComandoEjecutarModelosPayload()

class ComandoRevertirEjecucionModelosPayload(Record):
    cluster_id = String()
    ruta_imagen_anonimizada = String()

class ComandoRevertirEjecucionModelos(ComandoIntegracion):
    data = ComandoEjecutarModelosPayload()