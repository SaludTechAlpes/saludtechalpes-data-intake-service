from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import src.modulos.sagas.dominio.objetos_valor as ov

@dataclass
class AnonimizarDatosComando():
    ruta_imagen: Optional[str] = None
    ruta_metadatos:Optional[str] = None

@dataclass
class AgruparDatosComando:
    id_imagen = String()
    etiquetas_patologicas: List[ov.EtiquetaPatologica] = field(default_factory=list)
    ruta_imagen_anonimizada: Optional[str] = None


@dataclass
class RevertirAnonimizacionComando():
    id_imagen: Optional[uuid.UUID] = None


@dataclass
class RevertirAgrupamientoComando():
    id_imagen_mapeada: Optional[uuid.UUID] = None