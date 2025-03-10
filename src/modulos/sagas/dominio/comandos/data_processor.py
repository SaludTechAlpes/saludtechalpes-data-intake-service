from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import List, Optional

import src.modulos.sagas.dominio.objetos_valor as ov
from src.seedwork.dominio.comandos import ComandoDominio



@dataclass
class AnonimizarDatosComando(ComandoDominio):
    id_imagen_importada: Optional[uuid.UUID] = None
    ruta_imagen_importada: Optional[str] = None
    ruta_metadatos_importados:Optional[str] = None
    evento_a_fallar: Optional[str] = None

@dataclass
class RevertirAnonimizacionDatosComando(ComandoDominio):
    id_imagen_anonimizada: Optional[uuid.UUID] = None
    es_compensacion: Optional[bool] = True


@dataclass
class MapearDatosComando(ComandoDominio):
    id_imagen_importada: Optional[uuid.UUID] = None
    id_imagen_anonimizada: Optional[uuid.UUID] = None
    etiquetas_patologicas: List[ov.EtiquetaPatologica] = field(default_factory=list)
    ruta_imagen_anonimizada: Optional[str] = None
    evento_a_fallar: Optional[str] = None

@dataclass
class RevertirMapeoComando(ComandoDominio):
    id_imagen_mapeada: Optional[uuid.UUID] = None
    es_compensacion: Optional[bool] = True