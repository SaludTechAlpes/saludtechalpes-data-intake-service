from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class ComandoImportarDatosPayload(Record):
    ruta_imagen = String()
    ruta_metadatos = String()

class ComandoImportarDatos(ComandoIntegracion):
    data = ComandoImportarDatosPayload()

class ComandoRevertirDatosImportadosPayload(Record):
    ruta_imagen = String()
    ruta_metadatos = String()

class ComandoRevertirDatosImportados(ComandoIntegracion):
    data = ComandoRevertirDatosImportadosPayload()