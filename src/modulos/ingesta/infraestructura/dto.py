from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.config.db import Base
import uuid
import os

def get_uuid():
    return str(uuid.uuid4())

class ImagenMedicaDTO(Base):
    __tablename__ = "imagen_medica"

    if os.getenv("FLASK_ENV") == "test":
        id = Column(String, primary_key=True, default=get_uuid)
        metadatos_id = Column(String, ForeignKey("metadatos_imagen.id", ondelete="CASCADE"), nullable=True)
    else:
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        metadatos_id = Column(UUID(as_uuid=True), ForeignKey("metadatos_imagen.id", ondelete="CASCADE"), nullable=True)

    ruta_imagen_importada = Column(String, nullable=False)
    metadatos = relationship("MetadatosImagenDTO", back_populates="imagen", cascade="all, delete")

class MetadatosImagenDTO(Base):  
    __tablename__ = "metadatos_imagen"

    if os.getenv("FLASK_ENV") == "test":
        id = Column(String, primary_key=True, default=get_uuid)
    else:
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    ruta_metadatos_importados = Column(String, nullable=False)
    imagen = relationship("ImagenMedicaDTO", back_populates="metadatos")
