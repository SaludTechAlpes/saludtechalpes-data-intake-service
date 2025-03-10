from src.modulos.sagas.infraestructura.schema.v1.eventos.data_intake import EventoDatosImportadosFallido
from src.modulos.sagas.infraestructura.schema.v1.eventos.date_processor import EventoDatosAnonimizadosFallido, EventoDatosAgrupadosFallido
from src.modulos.sagas.infraestructura.schema.v1.eventos.data_transformation import EventoDataFramesGeneradosFallido
from src.modulos.sagas.dominio.eventos.data_intake import DatosImportadosFallidoEvento
from src.modulos.sagas.dominio.eventos.data_processor import DatosAnonimizadosFallidoEvento, DatosAgrupadosEventoFallido
from src.modulos.sagas.dominio.eventos.data_transformation import DataFramesGeneradosFallidoEvento

def convertir_evento_a_dominio(evento_infra):
    """Convierte eventos de infraestructura a eventos de dominio."""
    
    if isinstance(evento_infra, EventoDatosImportadosFallido):
        return DatosImportadosFallidoEvento(
            id_imagen_importada=evento_infra.data.id_imagen_importada
        )

    elif isinstance(evento_infra, EventoDatosAnonimizadosFallido):
        return DatosAnonimizadosFallidoEvento(
            id_imagen_importada=evento_infra.data.id_imagen_importada,
            id_imagen_anonimizada=evento_infra.data.id_imagen_anonimizada
        )

    elif isinstance(evento_infra, EventoDatosAgrupadosFallido):
        return DatosAgrupadosEventoFallido(
            id_imagen_importada=evento_infra.data.id_imagen_importada,
            id_imagen_anonimizada=evento_infra.data.id_imagen_anonimizada,
            id_imagen_mapeada=evento_infra.data.id_imagen_mapeada
        )

    elif isinstance(evento_infra, EventoDataFramesGeneradosFallido):
        return DataFramesGeneradosFallidoEvento(
            id_imagen_importada=evento_infra.data.id_imagen_importada,
            id_imagen_anonimizada=evento_infra.data.id_imagen_anonimizada,
            id_imagen_mapeada=evento_infra.data.id_imagen_mapeada,
            id_dataframe=evento_infra.data.id_dataframe
        )

    else:
        raise ValueError(f"Evento de infraestructura desconocido: {type(evento_infra).__name__}")
