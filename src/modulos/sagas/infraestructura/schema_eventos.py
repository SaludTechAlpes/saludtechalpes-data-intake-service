from src.modulos.sagas.infraestructura.schema.v1.eventos.data_intake import EventoDatosImportadosFallido
from src.modulos.sagas.infraestructura.schema.v1.eventos.date_processor import EventoDatosAnonimizadosFallido, EventoDatosAgrupadosFallido
from src.modulos.sagas.infraestructura.schema.v1.eventos.data_transformation import EventoDataFramesGeneradosFallido

SCHEMAS_EVENTOS = {
    "datos-importados-fallido": EventoDatosImportadosFallido,
    "datos-anonimizados-fallido": EventoDatosAnonimizadosFallido,
    "datos-agrupados-fallido": EventoDatosAgrupadosFallido,
    "generacion-dataframes-fallido": EventoDataFramesGeneradosFallido,
}
