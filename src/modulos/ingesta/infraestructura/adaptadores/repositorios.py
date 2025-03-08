from uuid import UUID
from sqlalchemy import delete
from src.modulos.ingesta.dominio.puertos.repositorios import RepositorioIngesta
from src.modulos.ingesta.dominio.entidades import ImagenMedica, MetadatosImagenMedica
from src.modulos.ingesta.infraestructura.dto import ImagenMedicaDTO, MetadatosImagenDTO
from src.modulos.ingesta.infraestructura.mapeadores import MapeadorImagenMedica
from src.config.db import get_db
import logging

logger = logging.getLogger(__name__)

class RepositorioIngestaPostgres(RepositorioIngesta):
    """
    Implementación del repositorio para almacenar DataFrames en PostgreSQL.
    """

    def __init__(self):
        self.session = next(get_db())
        self.mapeador = MapeadorImagenMedica()

    def obtener_por_id(self, id: UUID) -> ImagenMedica:
        """
        Obtiene un Imagen médica por su ID.
        """
        imagen_dto = self.session.query(ImagenMedicaDTO).filter_by(id=str(id)).one_or_none()
        if not imagen_dto:
            return None
        return self.mapeador.dto_a_entidad(imagen_dto)

    def obtener_todos(self) -> list[ImagenMedica]:
        """
        Obtiene todos las Imagenes médicas almacenadas en la base de datos.
        """
        imagenes_dto = self.session.query(DataFrameDTO).all()
        return [self.mapeador.dto_a_entidad(imagen_dto) for imagen_dto in imagenes_dto]

    def agregar(self, imagen: ImagenMedica):
        """
        Agrega una nueva Imagen médica a la base de datos.
        """
        imagen_dto = self.mapeador.entidad_a_dto(imagen)
        self.session.add(imagen_dto)
        self.session.commit()

    def actualizar(self, imagen: ImagenMedica):
        """
        Actualiza una Imagen médica existente en la base de datos.
        """
        imagen_dto = self.mapeador.entidad_a_dto(imagen)
        self.session.merge(imagen_dto)
        self.session.commit()

    def eliminar(self, id: UUID):
        """
        Elimina una Imagen médica de la base de datos por su ID.
        """
        self.session.execute(
            delete(ImagenMedicaDTO).where(ImagenMedicaDTO.id == str(id))
        )
        self.session.commit()