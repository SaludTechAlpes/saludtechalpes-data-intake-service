from src.modulos.ingesta.dominio.entidades import ImagenMedica, MetadatosImagenMedica
from src.modulos.ingesta.infraestructura.dto import ImagenMedicaDTO, MetadatosImagenDTO
from src.seedwork.dominio.repositorios import Mapeador


class MapeadorImagenMedica(Mapeador):

    def obtener_tipo(self) -> type:
        return ImagenMedica.__class__
    
    def entidad_a_dto(self, imagen: ImagenMedica) -> ImagenMedicaDTO:
        metadatos_dto = None
        if imagen.metadatos:
            metadatos_dto = MetadatosImagenDTO(
                id=imagen.metadatos.id,
                ruta_metadatos_importados=imagen.metadatos.ruta_metadatos_importados,
            )

        return ImagenMedicaDTO(
            id=imagen.id,
            ruta_imagen_importada=imagen.ruta_imagen_importada,
            metadatos=metadatos_dto
        )

    def dto_a_entidad(self, dto: ImagenMedicaDTO) -> ImagenMedica:
        metadatos_entidad = None
        if dto.metadatos:
            metadatos_entidad = MetadatosImagenMedica(
                id=dto.metadatos.id,
                ruta_metadatos_importados=dto.metadatos.ruta_metadatos_importados
            )

        return ImagenMedica(
            id=dto.id,
            ruta_imagen_importada=dto.ruta_imagen_importada,
            metadatos=metadatos_entidad
        )
