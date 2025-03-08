from src.seedwork.aplicacion.sagas import CoordinadorCoreografia
from src.modulos.sagas.infraestructura.pulsar_manager import PulsarManager
from src.seedwork.aplicacion.sagas import Transaccion
from src.seedwork.dominio.eventos import EventoDominio
from src.modulos.sagas.dominio.eventos.data_intake import DatosImportadosEvento, DatosImportadosFallidoEvento
from src.modulos.sagas.dominio.eventos.data_processor import DatosAnonimizadosEvento, DatosAnonimizadosFallidoEvento, DatosAgrupadosEvento, DatosAgrupadosFallidoEvento
from src.modulos.sagas.dominio.eventos.data_transformation import DataFramesGeneradosEvento, DataFramesGeneradosFallidoEvento
from src.modulos.sagas.dominio.eventos.medical_history import HistorialMedicoAlmacenadoEvento, HistorialMedicoFallidoEvento
from src.modulos.sagas.dominio.comandos.data_intake import DatosImportadosComando, RevertirDatosImportadosComando
from src.modulos.sagas.dominio.comandos.data_processor import AnonimizarDatosComando, AgruparDatosComando, RevertirAnonimizacionComando, RevertirAgrupamientoComando
from src.modulos.sagas.dominio.comandos.data_transformation import EjecutarModelosComando, RevertirEjecucionModelosComando
from src.modulos.sagas.dominio.comandos.medical_history import HistorialMedicoComando, RevertirHistorialMedicoComando
from src.modulos.sagas.infraestructura.despachadores import DespachadorComandosSagas
import pulsar
from pulsar.schema import AvroSchema
import logging
import inspect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAPA_TRANSACCIONES = [
    Transaccion(comando=DatosImportadosComando, evento=DatosImportadosEvento, error=DatosImportadosFallidoEvento, compensacion=RevertirDatosImportadosComando, topico="datos-importados"),
    Transaccion(comando=AnonimizarDatosComando, evento=DatosAnonimizadosEvento, error=DatosAnonimizadosFallidoEvento, compensacion=RevertirAnonimizacionComando, topico="anonimizar-datos"),
    Transaccion(comando=AgruparDatosComando, evento=DatosAgrupadosEvento, error=DatosAgrupadosFallidoEvento, compensacion=RevertirAgrupamientoComando, topico="mapear-datos"),
    Transaccion(comando=EjecutarModelosComando, evento=DataFramesGeneradosEvento, error=DataFramesGeneradosFallidoEvento, compensacion=RevertirEjecucionModelosComando, topico="ejecutar-modelos"),
    Transaccion(comando=HistorialMedicoComando, evento=HistorialMedicoAlmacenadoEvento, error=HistorialMedicoFallidoEvento, compensacion=RevertirHistorialMedicoComando, topico="crear-historial-medico"),
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
        self.despachador = DespachadorComandosSagas()

        # Consumidores para eventos de fallo con esquema correcto
        for topico in TOPICOS_EVENTOS:
            consumer = self.cliente_pulsar.subscribe(
                topico,  
                schema=AvroSchema(self.obtener_schema_para_topico(topico)),
                subscription_name="saludtech-sub-eventos"
            )
            self.consumidores.append(consumer)

    def obtener_schema_para_topico(self, topico):
        """Asocia un esquema Avro a cada tópico"""
        SCHEMAS_EVENTOS = {
            "datos-importados": EventoDatosImportados,
            "datos-anonimizados": EventoDatosAnonimizados,
            "datos-agrupados": EventoDatosAgrupados,
            "dataframes-generados": EventoDataFramesGenerados,
            "historial-almacenado": EventoHistorialMedicoAlmacenado,
        }
        return SCHEMAS_EVENTOS.get(topico)

    def inicializar_pasos(self):
        """Carga los pasos desde `MAPA_TRANSACCIONES`."""
        self.pasos = MAPA_TRANSACCIONES


    def publicar_comando(self, evento, comando):
        """Publica un comando de compensación en el mismo tópico donde se ejecutó el comando original."""
        logger.warning(f"⚠️ Activando compensación {comando.__name__} tras fallo en {type(evento).__name__}")

        # Buscar el paso correspondiente en MAPA_TRANSACCIONES
        for paso in self.pasos:
            if paso.compensacion == comando:
                topico_destino = paso.topico
                break
        else:
            logger.error(f"❌ No se encontró un tópico para {comando.__name__}")
            return

        # Obtener los atributos requeridos del comando mediante introspección
        parametros_comando = inspect.signature(comando).parameters
        datos_comando = {"id_saga": evento.id_saga}

        # Extraer los valores del evento que coincidan con los parámetros del comando
        for atributo in parametros_comando:
            if hasattr(evento, atributo):
                datos_comando[atributo] = getattr(evento, atributo)
            elif atributo != "id_saga":  # Excluimos id_saga porque ya se asignó antes
                logger.warning(f"⚠️ El evento {type(evento).__name__} no tiene el atributo requerido '{atributo}' para el comando {comando.__name__}")

        # Crear el comando de compensación con los datos correctos
        comando_compensacion = comando(**datos_comando)

        # Publicar el comando en el tópico correcto
        self.despachador.publicar_comando(comando_compensacion, topico_destino)
        logger.info(f"📤 Comando de compensación {comando.__name__} publicado en {topico_destino} con datos {datos_comando}")



    def persistir_en_saga_log(self, mensaje):
        """Guarda el estado de la Saga en una base de datos o log."""
        logger.info(f"📌 Persistiendo en Saga Log: {mensaje}")

    def construir_comando(self, evento: EventoDominio, tipo_comando: type):
        return None