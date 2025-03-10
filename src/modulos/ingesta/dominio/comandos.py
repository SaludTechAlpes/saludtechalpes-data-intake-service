from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from src.seedwork.dominio.comandos import ComandoDominio

@dataclass
class ImportarDatosComando(ComandoDominio):
    id_imagen_importada: Optional[str] = None
    ruta_imagen: Optional[str] = None
    ruta_metadatos:Optional[str] = None

@dataclass
class RevertirImportacionDatosComando(ComandoDominio):
    id_imagen_importada: Optional[str] = None
    es_compensacion: Optional[bool] = True

    
