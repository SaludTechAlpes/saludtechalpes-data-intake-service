from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from src.seedwork.dominio.eventos import EventoDominio

@dataclass
class ImportarDatosComando(EventoDominio):
    id_imagen_importada: Optional[str] = None
    ruta_imagen: Optional[str] = None
    ruta_metadatos:Optional[str] = None

@dataclass
class RevertirImportacionDatosComando(EventoDominio):
    id_imagen_importada: Optional[str] = None
    es_compensacion: Optional[bool] = True



    
    
