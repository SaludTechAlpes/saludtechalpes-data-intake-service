from src.seedwork.aplicacion.sagas import CoordinadorCoreografia, Transaccion
from src.modulos.sagas.infraestructura.pulsar_manager import PulsarManager
from src.modulos.sagas.infraestructura.despachadores import DespachadorComandosSagas
from pulsar.schema import AvroSchema
import pulsar
import threading
import logging
import inspect

from src.modulos.sagas.aplicacion.coordinadores.utils import convertir_evento_a_dominio
from src.modulos.sagas.infraestructura.schema_eventos import SCHEMAS_EVENTOS

from src.modulos.sagas.dominio.eventos.data_intake import DatosImportadosEvento, DatosImportadosFallidoEvento
from src.modulos.sagas.dominio.eventos.data_processor import DatosAnonimizadosEvento, DatosAnonimizadosFallidoEvento, DatosAgrupadosEvento, DatosAgrupadosEventoFallido
from src.modulos.sagas.dominio.eventos.data_transformation import DataFramesGeneradosEvento, DataFramesGeneradosFallidoEvento
from src.modulos.sagas.dominio.comandos.data_intake import RevertirImportacionDatosComando
from src.modulos.sagas.dominio.comandos.data_processor import RevertirAnonimizacionDatosComando, RevertirMapeoComando
from src.modulos.sagas.dominio.comandos.data_transformation import RevertirEjecucionModelosComando


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOPICOS_EVENTOS = [
    "datos-importados-fallido",
    "datos-anonimizados-fallido",
    "datos-agrupados-fallido",
    "generacion-dataframes-fallido",
]


def escuchar_evento(coordinador, consumidor, topico):
    """Escucha eventos en un hilo separado para cada tópico."""
    while True:
        try:
            mensaje = consumidor.receive()
            evento = mensaje.value()
            logger.warning(f"⚠️ Evento fallido detectado en `{topico}`: {evento.data}")
            
            # Procesar el evento fallido y activar compensaciones
            coordinador.procesar_evento(evento)
            consumidor.acknowledge(mensaje)

        except Exception as e:
            logger.error(f"❌ Error procesando evento en `{topico}`: {e}")

class CoordinadorCoreografiaEventos(CoordinadorCoreografia):
    """Coordinador Coreográfico basado en eventos de compensación"""
    
    def __init__(self):
        super().__init__()
        self.inicializar_pasos()
        self.cliente_pulsar = PulsarManager.obtener_cliente()
        self.consumidores = []
        self.despachador = DespachadorComandosSagas()

        # Inicializar consumidores de eventos fallidos
        for topico in TOPICOS_EVENTOS:
            consumidor = self.cliente_pulsar.subscribe(
                topico,
                schema=AvroSchema(SCHEMAS_EVENTOS[topico]),
                subscription_name="saludtech-sub-eventos"
            )
            self.consumidores.append((topico, consumidor))

    def inicializar_pasos(self):
        """Carga los pasos de la saga usando eventos y comandos de dominio."""
        self.pasos = [
            Transaccion(comando=None, evento=DatosImportadosEvento, error=DatosImportadosFallidoEvento, compensacion=RevertirImportacionDatosComando, topico="revertir-importacion-datos"),
            Transaccion(comando=None, evento=DatosAnonimizadosEvento, error=DatosAnonimizadosFallidoEvento, compensacion=RevertirAnonimizacionDatosComando, topico="revertir-anonimizacion-datos"),
            Transaccion(comando=None, evento=DatosAgrupadosEvento, error=DatosAgrupadosEventoFallido, compensacion=RevertirMapeoComando, topico="revertir-mapeo-datos"),
            Transaccion(comando=None, evento=DataFramesGeneradosEvento, error=DataFramesGeneradosFallidoEvento, compensacion=RevertirEjecucionModelosComando, topico="revertir-ejecucion-modelos"),
        ]


    def iniciar_consumidores(self):
        """Crea un hilo separado para cada consumidor de eventos."""
        for topico, consumidor in self.consumidores:
            hilo = threading.Thread(target=escuchar_evento, args=(self, consumidor, topico), daemon=True)
            hilo.start()

    def procesar_evento(self, evento_infra):
        """Convierte el evento de infraestructura a dominio antes de buscar la transacción."""
        try:
            # Convertimos el evento de infraestructura en un evento de dominio
            evento_dominio = convertir_evento_a_dominio(evento_infra)

            # Encuentra el paso de la transacción en base al evento de dominio
            paso_fallido, index = self.obtener_paso_dado_un_evento(evento_dominio)

            logger.info(f"⏳ Ejecutando compensaciones desde el paso {index} hacia atrás...")

            # Ejecutar las compensaciones en orden inverso
            for i in range(index, -1, -1):
                comando_compensacion = self.pasos[i].compensacion
                self.publicar_comando(evento_dominio, comando_compensacion)

        except Exception as e:
            logger.error(f"❌ Error al procesar evento fallido: {e}")



    def publicar_comando(self, evento, comando):
        """Publica un comando de compensación en el tópico correspondiente"""
        logger.warning(f"⚠️ Activando compensación {comando.__name__} tras fallo en {type(evento).__name__}")

        # Obtener el tópico del comando de compensación
        for paso in self.pasos:
            if paso.compensacion == comando:
                topico_destino = paso.topico
                break
        else:
            logger.error(f"❌ No se encontró un tópico para {comando.__name__}")
            return

        # Obtener atributos dinámicamente
        parametros_comando = inspect.signature(comando).parameters

        # logger.info(f"Parámetros esperados por {comando.__name__}: {inspect.signature(comando).parameters}")


        datos_comando = {}

        # logger.info(f"🔍 Evento recibido: {evento}")  # Para ver qué datos tiene el evento

        # logger.info(f"Atributos del evento en publicar_comando: {evento.__dict__}")

        # Lista de atributos que queremos ignorar
        atributos_ignorar = {"id", "_id", "fecha_comando"}

        for atributo in parametros_comando:
            if hasattr(evento, atributo) and atributo not in atributos_ignorar:
                datos_comando[atributo] = getattr(evento, atributo)
            else:
                logger.warning(f"⚠️ El evento {type(evento).__name__} no tiene '{atributo}' requerido para {comando.__name__}")

        comando_compensacion = comando(**datos_comando)
        self.despachador.publicar_comando(comando_compensacion, topico_destino)
        
    def construir_comando(self, evento, tipo_comando):
        ...
    
    def persistir_en_saga_log(self, mensaje):
        ...