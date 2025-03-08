from __future__ import annotations
from dataclasses import dataclass
import uuid
from datetime import datetime
from typing import Optional
from src.seedwork.dominio.eventos import EventoDominio

@dataclass
class DataFramesGeneradosEvento(EventoDominio):
    dataframe_id: Optional[str] = None #nuevo
    cluster_id: Optional[str] = None
    ruta_archivo_parquet: Optional[str] = None
    fecha_generacion: Optional[datetime] = None


@dataclass
class DataFramesGeneradosFallidoEvento(EventoDominio):
    dataframe_id: Optional[str] = None
