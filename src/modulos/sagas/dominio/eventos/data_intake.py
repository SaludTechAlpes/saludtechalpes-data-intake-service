from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from src.seedwork.dominio.eventos import EventoDominio

@dataclass
class DatosImportadosEvento(EventoDominio):
    id_imagen_importada: Optional[str] = None #nuevo
    ruta_imagen: Optional[str] = None
    ruta_metadatos:Optional[str] = None

class DatosImportadosFallidoEvento(EventoDominio):
    id_imagen_importada: Optional[str] = None #nuevo