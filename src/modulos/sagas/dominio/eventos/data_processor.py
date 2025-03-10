from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime
from typing import List, Optional
from src.seedwork.dominio.eventos import EventoDominio
import src.modulos.sagas.dominio.objetos_valor as ov


@dataclass
class DatosAnonimizadosEvento(EventoDominio):
    id_imagen_importada: Optional[uuid.UUID] = None
    id_imagen_anonimizada: Optional[uuid.UUID] = None
    ruta_imagen_anonimizada: Optional[str] = None
    id_paciente: Optional[uuid.UUID] = None
    modalidad: Optional[ov.Modalidad] = None
    region_anatomica: Optional[ov.RegionAnatomica] = None
    fecha_estudio: Optional[datetime] = None
    etiquetas_patologicas: List[ov.EtiquetaPatologica] = field(default_factory=list) 
    evento_a_fallar: Optional[datetime] = None

@dataclass
class DatosAnonimizadosFallidoEvento(EventoDominio):
    id_imagen_importada: Optional[uuid.UUID] = None
    id_imagen_anonimizada: Optional[uuid.UUID] = None 


@dataclass
class DatosAgrupadosEvento(EventoDominio):
    id_imagen_importada: Optional[uuid.UUID] = None
    id_imagen_anonimizada: Optional[uuid.UUID] = None
    id_imagen_mapeada: Optional[uuid.UUID] = None
    cluster_id: Optional[uuid.UUID] = None
    ruta_imagen_anonimizada: Optional[str] = None
    evento_a_fallar: Optional[str] = None

@dataclass
class DatosAgrupadosEventoFallido(EventoDominio):
    id_imagen_importada: Optional[uuid.UUID] = None
    id_imagen_anonimizada: Optional[uuid.UUID] = None
    id_imagen_mapeada: Optional[uuid.UUID] = None
