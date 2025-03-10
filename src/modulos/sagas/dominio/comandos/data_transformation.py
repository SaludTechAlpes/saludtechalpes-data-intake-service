from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from src.seedwork.dominio.comandos import ComandoDominio

@dataclass
class EjecutarModelosComando(ComandoDominio):
    id_imagen_importada: Optional[str] = None
    id_imagen_anonimizada: Optional[str] = None
    id_imagen_mapeada: Optional[str] = None
    cluster_id: Optional[str] = None
    ruta_imagen_anonimizada: Optional[str] = None
    evento_a_fallar: Optional[str] = None

@dataclass
class RevertirEjecucionModelosComando(ComandoDominio):
    id_dataframe: Optional[str] = None