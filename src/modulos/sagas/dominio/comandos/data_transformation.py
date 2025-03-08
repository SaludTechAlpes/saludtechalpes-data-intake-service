from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from src.seedwork.dominio.comandos import ComandoDominio

@dataclass
class EjecutarModelosComando(ComandoDominio):
    """
    Comando que activa la ejecución de modelos IA y la generación de DataFrames.
    """
    cluster_id: Optional[str] = None
    ruta_imagen_anonimizada: Optional[str] = None


@dataclass
class RevertirEjecucionModelosComando(ComandoDominio):
    """
    Comando que activa la ejecución de modelos IA y la generación de DataFrames.
    """
    cluster_id: Optional[str] = None
    ruta_imagen_anonimizada: Optional[str] = None