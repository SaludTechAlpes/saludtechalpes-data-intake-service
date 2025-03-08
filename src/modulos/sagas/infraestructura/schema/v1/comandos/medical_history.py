from pulsar.schema import *
from dataclasses import dataclass, field
from src.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoHistorialMedicoPayload(ComandoIntegracion):
    id_imagen = String()
    paciente = String()

class ComandoHistorialMedico(ComandoIntegracion):
    data = ComandoHistorialMedicoPayload()

class ComandoRevertirHistorialMedicoPayload(ComandoIntegracion):
    id_imagen = String()
    paciente = String()

class ComandoRevertirHistorialMedico(ComandoIntegracion):
    data = ComandoHistorialMedicoPayload()