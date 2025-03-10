from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoRevertirDatosImportadosPayload(Record):
    id_imagen_importada = String()
    es_compensacion = Boolean()

class ComandoRevertirDatosImportados(ComandoIntegracion):
    data = ComandoRevertirDatosImportadosPayload()