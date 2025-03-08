from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class DatosImportadosEvento():
    id_imagen_importada: Optional[str] = None
    ruta_imagen: Optional[str] = None
    ruta_metadatos:Optional[str] = None
