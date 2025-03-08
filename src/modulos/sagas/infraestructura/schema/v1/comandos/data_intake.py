from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class ComandoDatosImportadosPayload(Record):
    ruta_imagen = String()
    ruta_metadatos = String()

class ComandoDatosImportados(ComandoIntegracion):
    data = ComandoEjecutarModelosPayload()

class ComandoRevertirDatosImportadosPayload(Record):
    ruta_imagen = String()
    ruta_metadatos = String()

class ComandoRevertirDatosImportados(ComandoIntegracion):
    data = ComandoEjecutarModelosPayload()