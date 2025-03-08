from __future__ import annotations
from dataclasses import dataclass
import uuid
from datetime import datetime
from typing import Optional
from src.seedwork.dominio.eventos import EventoDominio


@dataclass
class HistorialMedicoAlmacenadoEvento(EventoDominio):
    id_historial_medico: Optional[str] = None

@dataclass
class HistorialMedicoFallidoEvento(EventoDominio):
    id_historial_medico: Optional[str] = None