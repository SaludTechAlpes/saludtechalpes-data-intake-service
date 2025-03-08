from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class HistorialMedicoComando:
    id_imagen: Optional[uuid.UUID] = None
    paciente: str = ''

@dataclass
class RevertirHistorialMedicoComando:
    id_imagen: Optional[uuid.UUID] = None
    paciente: str = ''