from src.seedwork.aplicacion.sagas import CoordinadorCoreografia
from src.modulos.sagas.infraestructura.pulsar_manager import PulsarManager
from src.seedwork.aplicacion.sagas import Transaccion
from src.modulos.sagas.dominio.eventos.data_processor import DatosAnonimizadosEvento, DatosAnonimizadosFallidoEvento, DatosAgrupadosEvento, DatosAgrupadosFallidoEvento
from src.modulos.sagas.dominio.eventos.data_transformation import DataFramesGeneradosEvento, GeneracionDataFramesRevertidoEvento
from src.modulos.sagas.dominio.eventos.medical_history import HistorialMedicoAlmacenadoEvento, HistorialMedicoFallidoEvento
from src.modulos.sagas.dominio.comandos.data_intake import DatosImportadosComando, RevertirDatosImportadosComando
from src.modulos.sagas.dominio.comandos.data_processor import AnonimizarDatosComando, AgruparDatosComando, RevertirAnonimizacionComando, RevertirAgrupamientoComando
from src.modulos.sagas.dominio.comandos.data_transformation import EjecutarModelosComando, RevertirEjecucionModelosComando
from src.modulos.sagas.dominio.comandos.medical_history import EjecutarModelosComando, RevertirHistorialMedicoComando
import pulsar
from pulsar.schema import AvroSchema
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAPA_TRANSACCIONES = [
    Transaccion(index=1, comando=DatosImportadosComando, evento=DatosImportadosEvento, error=DatosImportadosFallidoEvento, compensacion=RevertirDatosImportadosComando, topico="datos-importados"),
    Transaccion(index=2, comando=AnonimizarDatosComando, evento=DatosAnonimizadosEvento, error=DatosAnonimizadosFallidoEvento, compensacion=RevertirAnonimizacionComando, topico="anonimizar-datos"),
    Transaccion(index=3, comando=AgruparDatosComando, evento=DatosAgrupadosEvento, error=DatosAgrupadosFallidoEvento, compensacion=RevertirAgrupamientoComando, topico="mapear-datos"),
    Transaccion(index=4, comando=EjecutarModelosComando, evento=DataFramesGeneradosEvento, error=DataFramesGeneradosFallidoEvento, compensacion=RevertirEjecucionModelosComando, topico="ejecutar-modelos"),
    Transaccion(index=5, comando=HistorialMedicoComando, evento=HistorialMedicoAlmacenadoEvento, error=HistorialMedicoFallidoEvento, compensacion=RevertirHistorialMedicoComando, topico="crear-historial-medico"),
]

TOPICOS_EVENTOS = [
    "datos-importados",
    "datos-anonimizados",
    "datos-agrupados",
    "dataframes-generados",
    "historial-almacenado"
]

class CoordinadorCoreografiaEventos(CoordinadorCoreografia):
    """Coordinador Coreográfico basado en eventos de compensación"""
    def __init__(self):
        super().__init__()
        self.inicializar_pasos()
        self.cliente_pulsar = PulsarManager.obtener_cliente()
        self.consumidores = []
        self.producers = {}

        # Consumidores para eventos de fallo
        for topico in TOPICOS_EVENTOS:
            consumer = self.cliente_pulsar.subscribe(
                topico,  
                schema=AvroSchema(EventoDominio),
                subscription_name="saludtech-sub-eventos"
            )
            self.consumidores.append(consumer)

        # Productores para comandos de compensación
        for paso in self.pasos:
            self.producers[paso.compensacion.__name__] = self.cliente_pulsar.create_producer(
                paso.comando.topico, schema=AvroSchema(type(paso.compensacion))
            )

    def inicializar_pasos(self):
        """Carga los pasos desde `MAPA_TRANSACCIONES`."""
        self.pasos = MAPA_TRANSACCIONES

    def procesar_evento(self, evento):
        """Si el evento es un fallo, activa todas las compensaciones necesarias."""
        logger.warning(f"⚠️ Evento fallido detectado: {type(evento).__name__}")

        # Encuentra en qué punto de la saga ocurrió el fallo
        paso_fallido, index = self.obtener_paso_dado_un_evento(evento)

        logger.info(f"⏳ Ejecutando todas las compensaciones desde el paso {index} hacia atrás...")

        # Recorrer los pasos en orden inverso y ejecutar sus compensaciones
        for i in range(index, -1, -1):  # Desde el index fallido hasta el inicio
            comando_compensacion = self.pasos[i].compensacion
            self.publicar_comando(evento, comando_compensacion)

    def publicar_comando(self, evento, comando):
        """Publica un comando de compensación en el mismo tópico donde se ejecutó el comando original."""
        logger.warning(f"⚠️ Activando compensación {comando.__name__} tras fallo en {type(evento).__name__}")

        # Extraer los atributos del evento fallido
        datos_comando = {"id_saga": evento.id_saga}
        for atributo in atributos_requeridos:
            if hasattr(evento, atributo):
                datos_comando[atributo] = getattr(evento, atributo)
            else:
                logger.warning(f"⚠️ Evento {type(evento).__name__} no tiene el atributo {atributo}")

        # Crear el evento de compensación con los datos correctos
        evento_compensacion = comando(**datos_comando)
        evento_compensacion.es_compensacion = True

        self.producers[comando.__name__].send(evento_compensacion)
        logger.info(f"📤 Comando de compensación {comando.__name__} publicado en {evento.topico}")

    def escuchar_eventos(self):
        """Escucha eventos de fallo y activa todas las compensaciones necesarias."""
        while True:
            for consumer in self.consumidores:
                mensaje = consumer.receive()
                evento = mensaje.value()

                if hasattr(evento, "es_compensacion") and evento.es_compensacion:
                    continue  # No procesamos eventos de compensación, solo fallos

                self.procesar_evento(evento)
                consumer.acknowledge(mensaje)