from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone
from typing import List

import src.modulos.ingesta.dominio.objetos_valor as ov
from src.seedwork.dominio.entidades import AgregacionRaiz, Entidad

@dataclass
class ImagenMedica(AgregacionRaiz):
    id: uuid.UUID = None
    ruta_imagen_importada: str = ""
    metadatos: MetadatosAnonimizados = field(default_factory=lambda: MetadatosImagenMedica(
        ruta_metadatos_importados = ""
    ))


@dataclass
class MetadatosImagenMedica(Entidad):
    id: uuid.UUID = None
    ruta_metadatos_importados: str = ""
