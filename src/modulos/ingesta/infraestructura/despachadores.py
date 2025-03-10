import pulsar
from pulsar.schema import AvroSchema
import logging
from src.modulos.ingesta.infraestructura.schema.v1.comandos import ComandoRevertirDatosImportadosPayload, ComandoRevertirDatosImportados
from src.modulos.ingesta.infraestructura.schema.v1.eventos import EventoDatosImportadosPayload, EventoDatosImportados, EventoDatosImportadosFallidoPayload, EventoDatosImportadosFallido
from src.config.config import Config
logger = logging.getLogger(__name__)

config = Config()

class Despachador:    
    def _publicar_mensaje(self, mensaje, topico, schema):
        try:
            cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:{config.BROKER_PORT}')
            logger.info(f"📤 Publicando mensaje en {topico}: {mensaje.data}")
            producer = cliente.create_producer(topico, schema=AvroSchema(schema))
            producer.send(mensaje)
            logger.info(f"✅ Mensaje publicado con éxito en {topico}")
            cliente.close()
        except Exception as e:
            logger.error(f"❌ Error publicando mensaje en {topico}: {e}")
    
    def publicar_evento(self, evento, topico):
        payload = EventoDatosImportadosPayload(
            id_imagen_importada=evento.id_imagen_importada,
            ruta_imagen_importada=evento.ruta_imagen_importada,
            ruta_metadatos_importados=evento.ruta_metadatos_importados,
            evento_a_fallar=evento.evento_a_fallar
        )
        evento_ingesta = EventoDatosImportados(data=payload)
        self._publicar_mensaje(evento_ingesta, topico, EventoDatosImportados)

    def publicar_evento_fallido(self, evento, topico):
        payload = EventoDatosImportadosFallidoPayload(
            id_imagen_importada=str(evento.id_imagen_importada),
        )
        evento_gordo=EventoDatosImportadosFallido(data=payload)
        self._publicar_mensaje(evento_gordo, topico, EventoDatosImportadosFallido)

    def publicar_comando(self, evento, topico):
        payload = ComandoRevertirDatosImportadosPayload(
            id_imagen_importada=evento.id_imagen_importada,
            es_compensacion=True
        )
        comando_compensacion=ComandoRevertirDatosImportados(data=payload)
        self._publicar_mensaje(comando_compensacion, topico, ComandoRevertirDatosImportados)

