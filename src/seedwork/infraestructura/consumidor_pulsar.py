import pulsar, _pulsar
from pulsar.schema import AvroSchema
import logging
import traceback
from src.seedwork.infraestructura.consumidor import Consumidor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsumidorPulsar(Consumidor):
    """
    Implementación de `Consumidor` usando Apache Pulsar.
    """

    def __init__(self, cliente: pulsar.Client, topico: str, suscripcion: str, schema):
        """
        Inicializa el consumidor de Pulsar.
        """
        super().__init__(topico, suscripcion)
        self.cliente = cliente
        self.schema = schema
        self.consumidor = None

    def suscribirse(self):
        """
        Se suscribe a un tópico en Pulsar y procesa los mensajes recibidos.
        """
        try:
            self.consumidor = self.cliente.subscribe(
                self.topico,
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name=self.suscripcion,
                schema=AvroSchema(self.schema)
            )

            while True:
                mensaje = self.consumidor.receive()
                data = mensaje.value().data
                logger.info(f'Mensaje recibido en {self.topico}: {data}')

                try:
                    self.procesar_mensaje(data)
                    self.consumidor.acknowledge(mensaje)
                    logger.info("Mensaje procesado con éxito")
                except Exception as e:
                    logger.error(f"Error procesando comando: {e}")
                    self.consumidor.negative_acknowledge(mensaje)

        except Exception as error:
            logger.error(f'Error suscribiéndose al tópico {self.topico}: {error}')
            traceback.print_exc()
        finally:
            self.cerrar()

    def cerrar(self):
        """
        Cierra el cliente de Pulsar cuando se detiene el servicio.
        """
        if self.cliente:
            self.cliente.close()
            logger.info("Cliente Pulsar cerrado")
