import pulsar
from pulsar.schema import AvroSchema
import logging
from src.modulos.sagas.infraestructura.schema.v1.comandos.data_intake import ComandoRevertirDatosImportadosPayload, ComandoRevertirDatosImportados 
from src.modulos.sagas.infraestructura.schema.v1.comandos.data_processor import ComandoRevertirAnonimizacionPayload, ComandoRevertirAnonimizacion, ComandoRevertirAgrupamientoPayload, ComandoRevertirAgrupamiento
from src.modulos.sagas.infraestructura.schema.v1.comandos.data_transformation import ComandoRevertirEjecucionModelosPayload, ComandoRevertirEjecucionModelos 
from src.modulos.sagas.infraestructura.schema.v1.comandos.medical_history import ComandoRevertirHistorialMedicoPayload, ComandoRevertirHistorialMedico 
from src.modulos.sagas.dominio.comandos.data_intake import DatosImportadosComando, RevertirDatosImportadosComando
from src.modulos.sagas.dominio.comandos.data_processor import RevertirAnonimizacionComando, RevertirAgrupamientoComando
from src.modulos.sagas.dominio.comandos.data_transformation import RevertirEjecucionModelosComando
from src.modulos.sagas.dominio.comandos.medical_history import RevertirHistorialMedicoComando
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

        if isinstance(comando, RevertirDatosImportadosComando):
            payload = ComandoRevertirDatosImportadosPayload(id_saga=str(comando.id_saga))
            comando_pulsar = ComandoRevertirDatosImportados(data=payload)
            schema = ComandoRevertirDatosImportados

        elif isinstance(comando, RevertirAnonimizacionComando):
            payload = ComandoRevertirAnonimizacionPayload(id_saga=str(comando.id_saga))
            comando_pulsar = ComandoRevertirAnonimizacion(data=payload)
            schema = ComandoRevertirAnonimizacion

        elif isinstance(comando, RevertirAgrupamientoComando):
            payload = ComandoRevertirAgrupamientoPayload(id_saga=str(comando.id_saga))
            comando_pulsar = ComandoRevertirAgrupamiento(data=payload)
            schema = ComandoRevertirAgrupamiento

        elif isinstance(comando, RevertirEjecucionModelosComando):
            payload = ComandoRevertirEjecucionModelosPayload(id_saga=str(comando.id_saga))
            comando_pulsar = ComandoRevertirEjecucionModelos(data=payload)
            schema = ComandoRevertirEjecucionModelos

        elif isinstance(comando, RevertirHistorialMedicoComando):
            payload = ComandoRevertirHistorialMedicoPayload(id_saga=str(comando.id_saga))
            comando_pulsar = ComandoRevertirHistorialMedico(data=payload)
            schema = ComandoRevertirHistorialMedico

        else:
            logger.error(f"❌ Tipo de comando desconocido: {type(comando).__name__}")
            return

        self._publicar_mensaje(comando_pulsar, topico, schema)
