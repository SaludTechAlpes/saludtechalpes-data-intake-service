from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoAnonimizarDatosPayload(ComandoIntegracion):
    ruta_imagen = String()
    ruta_metadatos = String()

class ComandoAnonimizarDatos(ComandoIntegracion):
    data = ComandoAnonimizarDatosPayload()

class ComandoAgruparDatosPayload(ComandoIntegracion):
    id_imagen = String()
    etiquetas_patologicas = Array(String())
    ruta_imagen_anonimizada = String()

class ComandoAgruparDatos(ComandoIntegracion):
    data = ComandoAnonimizarDatosPayload()

class ComandoRevertirAnonimizacionPayload(ComandoIntegracion):
    ruta_imagen = String()
    ruta_metadatos = String()

class ComandoRevertirAnonimizacion(ComandoIntegracion):
    data = ComandoAnonimizarDatosPayload()

class ComandoRevertirAgrupamientoPayload(ComandoIntegracion):
    id_imagen = String()
    etiquetas_patologicas = Array(String())
    ruta_imagen_anonimizada = String()

class ComandoRevertirAgrupamiento(ComandoIntegracion):
    data = ComandoAnonimizarDatosPayload()