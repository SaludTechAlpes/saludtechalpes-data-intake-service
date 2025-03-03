import pulsar
from pulsar.schema import AvroSchema
import logging
from src.modulos.ingesta.infraestructura.schema.v1.eventos import EventoDatosImportadosPayload, EventoDatosImportados
from src.config.config import Config
logger = logging.getLogger(__name__)

config = Config()

class Despachador:    
    def _publicar_mensaje(self, mensaje, topico, schema):
        try:
            cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:6650')
            logger.info(f"Publicando mensaje en {topico}: {mensaje.data}")
            producer = cliente.create_producer(topico, schema=AvroSchema(schema))
            producer.send(mensaje)
            logger.info(f"Mensaje publicado con éxito en {topico}")
            cliente.close()
        except Exception as e:
            logger.error(f"Error publicando mensaje en {topico}: {e}")
    
    def publicar_evento(self, evento, topico):
        payload = EventoDatosImportadosPayload(
            ruta_imagen=evento.ruta_imagen,
            ruta_metadatos=evento.ruta_metadatos
        )
        evento_ingesta = EventoDatosImportados(data=payload)
        self._publicar_mensaje(evento_ingesta, topico, EventoDatosImportados)

    
    def cerrar(self):
        self.cliente.close()
        logger.info("Cliente Pulsar cerrado.")
