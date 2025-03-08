from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import src.modulos.mapeo.dominio.objetos_valor as ov

@dataclass
class AnonimizarDatosComando():
    id_imagen_ingestada: Optional[uuid.UUID] = None
    ruta_imagen: Optional[str] = None
    ruta_metadatos:Optional[str] = None

@dataclass
class AgruparDatosComando:
    id_imagen_anonimizada: Optional[uuid.UUID] = None
    etiquetas_patologicas: List[ov.EtiquetaPatologica] = field(default_factory=list)
    ruta_imagen_anonimizada: Optional[str] = None


@dataclass
class RevertirAnonimizacionComando():
    id_imagen: Optional[uuid.UUID] = None


@dataclass
class RevertirAgrupamientoComando():
    id_imagen_mapeada: Optional[uuid.UUID] = None