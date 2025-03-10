from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class ComandoEjecutarModelosPayload(Record):
    id_imagen_importada = String()
    id_imagen_anonimizada = String()
    id_imagen_mapeada = String()
    cluster_id = String()
    ruta_imagen_anonimizada = String()
    evento_a_fallar = String()

class ComandoEjecutarModelos(ComandoIntegracion):
    data = ComandoEjecutarModelosPayload()

class ComandoRevertirEjecucionModelosPayload(Record):
    id_dataframe = String()

class ComandoRevertirEjecucionModelos(ComandoIntegracion):
    data = ComandoRevertirEjecucionModelosPayload()