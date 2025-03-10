from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class DataFramesGeneradosPayload(Record):
    id_dataframe = String()
    cluster_id = String()
    ruta_archivo_parquet = String()
    fecha_generacion = String()
    evento_a_fallar = String()
    
class EventoDataFramesGenerados(EventoIntegracion):
    data = DataFramesGeneradosPayload()

class DataFramesGeneradosFallidoPayload(Record):
    id_imagen_importada = String()
    id_imagen_anonimizada = String()
    id_imagen_mapeada = String()
    id_dataframe = String()

class EventoDataFramesGeneradosFallido(EventoIntegracion):
    data = DataFramesGeneradosFallidoPayload()