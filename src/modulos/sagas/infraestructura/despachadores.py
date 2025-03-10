import pulsar
from pulsar.schema import AvroSchema
import logging
from src.modulos.sagas.infraestructura.schema.v1.comandos.data_intake import ComandoRevertirDatosImportados, ComandoRevertirDatosImportadosPayload
from src.modulos.sagas.infraestructura.schema.v1.comandos.data_processor import ComandoRevetirAnonimizacionDatosPayload, ComandoRevertirAnonimizacionDatos, ComandoRevetirMapeoPayload, ComandoRevertirMapeoDatos
from src.modulos.sagas.infraestructura.schema.v1.comandos.data_transformation import ComandoRevertirEjecucionModelosPayload, ComandoRevertirEjecucionModelos 
from src.modulos.sagas.dominio.comandos.data_intake import RevertirImportacionDatosComando
from src.modulos.sagas.dominio.comandos.data_processor import RevertirAnonimizacionDatosComando, RevertirMapeoComando
from src.modulos.sagas.dominio.comandos.data_transformation import RevertirEjecucionModelosComando
from src.config.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config()

class DespachadorComandosSagas:
    """
    Despachador para publicar comandos de compensación en Apache Pulsar.
    """

    def _publicar_mensaje(self, mensaje, topico, schema):
        """Método interno para publicar un comando en Pulsar."""
        try:
            cliente = pulsar.Client(f'{config.PULSAR_HOST}://{config.BROKER_HOST}:6650')
            logger.info(f"📤 Publicando comando en {topico}: {mensaje.data}")
            publicador = cliente.create_producer(topico, schema=AvroSchema(schema))
            publicador.send(mensaje)
            logger.info(f"✅ Comando publicado con éxito en {topico}")
            cliente.close()
        except Exception as e:
            logger.error(f"❌ Error publicando comando en {topico}: {e}")

    def publicar_comando(self, comando, topico):
        """
        Publica comandos de compensación en Pulsar, determinando el esquema correcto.
        """

        if isinstance(comando, RevertirImportacionDatosComando):
            payload = ComandoRevertirDatosImportadosPayload(
                id_imagen_importada=str(comando.id_imagen_importada), 
                es_compensacion=True
            )
            comando_pulsar = ComandoRevertirDatosImportados(data=payload)
            schema = ComandoRevertirDatosImportados

        elif isinstance(comando, RevertirAnonimizacionDatosComando):
            payload = ComandoRevetirAnonimizacionDatosPayload(
                id_imagen_anonimizada=str(comando.id_imagen_anonimizada),
                es_compensacion=True
            )
            comando_pulsar = ComandoRevertirAnonimizacionDatos(data=payload)
            schema = ComandoRevertirAnonimizacionDatos

        elif isinstance(comando, RevertirMapeoComando):
            payload = ComandoRevetirMapeoPayload(
                id_imagen_mapeada=str(comando.id_imagen_mapeada),
                es_compensacion=True
            )
            comando_pulsar = ComandoRevertirMapeoDatos(data=payload)
            schema = ComandoRevertirMapeoDatos

        elif isinstance(comando, RevertirEjecucionModelosComando):
            payload = ComandoRevertirEjecucionModelosPayload(
                id_dataframe=str(comando.id_dataframe),
            )
            comando_pulsar = ComandoRevertirEjecucionModelos(data=payload)
            schema = ComandoRevertirEjecucionModelos

        else:
            logger.error(f"❌ Tipo de comando desconocido: {type(comando).__name__}")
            return

        self._publicar_mensaje(comando_pulsar, topico, schema)
