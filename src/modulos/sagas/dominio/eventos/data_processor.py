from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime
from typing import List, Optional
from src.seedwork.dominio.eventos import EventoDominio
import src.modulos.sagas.dominio.objetos_valor as ov


@dataclass
class DatosAnonimizadosEvento(EventoDominio):
    id_imagen: Optional[uuid.UUID] = None
    ruta_imagen_anonimizada: Optional[str] = None
    id_paciente: Optional[uuid.UUID] = None
    modalidad: Optional[ov.Modalidad] = None
    region_anatomica: Optional[ov.RegionAnatomica] = None
    fecha_estudio: Optional[datetime] = None
    etiquetas_patologicas: List[ov.EtiquetaPatologica] = field(default_factory=list) 

@dataclass
class DatosAgrupadosEvento(EventoDominio):
    cluster_id: Optional[str] = None
    ruta_imagen_anonimizada: Optional[str] = None


@dataclass
class DatosAnonimizadosFallidoEvento(EventoDominio):
    id_imagen: Optional[uuid.UUID] = None

@dataclass
class DatosAgrupadosFallidoEvento(EventoDominio):
    id_imagen_mapeada: Optional[uuid.UUID] = None