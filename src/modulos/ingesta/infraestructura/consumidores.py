from src.modulos.ingesta.dominio.comandos import RevertirImportacionDatosComando
from src.seedwork.infraestructura.consumidor_pulsar import ConsumidorPulsar
from src.modulos.ingesta.infraestructura.schema.v1.comandos import ComandoRevertirDatosImportados
from src.modulos.ingesta.infraestructura.despachadores import Despachador
from src.modulos.ingesta.dominio.puertos.procesar_comando_modelos import PuertoProcesarComandoImportarDatos
import pulsar
import logging
from src.config.config import Config


config = Config()

# Configuración de logs
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ConsumidorComandoRevertirImportacionDatos(ConsumidorPulsar):
    """
    Consumidor de comandos de ejecución de modelos en Modelos IA.
    """
    def __init__(self, puerto_modelos: PuertoProcesarComandoImportarDatos):
        cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:{config.BROKER_PORT}')
        super().__init__(cliente, "revertir-importacion-datos", "saludtech-sub-comandos", ComandoRevertirDatosImportados)
        self.puerto_modelos = puerto_modelos

    def procesar_mensaje(self, data):
        self.puerto_modelos.procesar_comando_revertir_importacion(
            id_imagen_importada=data.id_imagen_importada,
        )