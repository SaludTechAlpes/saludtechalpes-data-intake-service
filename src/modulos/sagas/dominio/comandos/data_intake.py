from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import src.modulos.sagas.dominio.objetos_valor as ov

@dataclass
class DatosImportadosComando():
    ruta_imagen: Optional[str] = None
    ruta_metadatos:Optional[str] = None

@dataclass
class RevertirDatosImportadosComando():
    ruta_imagen: Optional[str] = None
    ruta_metadatos:Optional[str] = None
