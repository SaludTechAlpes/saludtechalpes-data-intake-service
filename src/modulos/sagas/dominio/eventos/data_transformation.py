from __future__ import annotations
from dataclasses import dataclass
import uuid
from datetime import datetime
from typing import Optional
from src.seedwork.dominio.eventos import EventoDominio

@dataclass
class DataFramesGeneradosEvento(EventoDominio):
    id_dataframe: Optional[str] = None
    cluster_id: Optional[str] = None
    ruta_archivo_parquet: Optional[str] = None
    fecha_generacion: Optional[datetime] = None
    evento_a_fallar: Optional[str] = None

@dataclass
class DataFramesGeneradosFallidoEvento(EventoDominio):
    id_imagen_importada: Optional[str] = None
    id_imagen_anonimizada: Optional[str] = None
    id_imagen_mapeada: Optional[str] = None
    id_dataframe: Optional[str] = None