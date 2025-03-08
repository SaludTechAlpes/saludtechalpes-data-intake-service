from abc import ABC, abstractmethod
from src.seedwork.aplicacion.comandos import Comando
from src.seedwork.dominio.eventos import EventoDominio
from src.seedwork.aplicacion.sagas import CoordinadorSaga, Transaccion, Inicio, Fin
from dataclasses import dataclass
from .comandos import ejecutar_commando
import uuid
import datetime

class CoordinadorSaga(ABC):
    id_correlacion: uuid.UUID

    @abstractmethod
    def persistir_en_saga_log(self, mensaje):
        ...

    @abstractmethod
    def construir_comando(self, evento: EventoDominio, tipo_comando: type) -> Comando:
        ...

    def publicar_comando(self,evento: EventoDominio, tipo_comando: type):
        comando = construir_comando(evento, tipo_comando)
        ejecutar_commando(comando)

    @abstractmethod
    def inicializar_pasos(self):
        ...
    
    @abstractmethod
    def procesar_evento(self, evento: EventoDominio):
        ...

    @abstractmethod
    def iniciar():
        ...
    
    @abstractmethod
    def terminar():
        ...

class Paso():
    id_correlacion: uuid.UUID
    fecha_evento: datetime.datetime
    index: int

@dataclass
class Inicio(Paso):
    index: int = 0

@dataclass
class Fin(Paso):
    ...

@dataclass
class Transaccion(Paso):
    comando: Comando
    evento: EventoDominio
    error: EventoDominio
    compensacion: Comando
    exitosa: bool
    topico: str


@dataclass
class CoordinadorCoreografia(CoordinadorSaga, ABC):
    """Clase base para coordinadores de coreografía, maneja solo eventos de compensación"""
    pasos: list[Paso] = None

    def obtener_paso_dado_un_evento(self, evento: EventoDominio):
        """
        Retorna el paso de la transacción basado en el evento recibido.
        """
        for i, paso in enumerate(self.pasos):
            if isinstance(evento, paso.error):  # Solo manejar eventos de fallo
                return paso, i
        raise Exception("Evento no hace parte de la transacción")

    def procesar_evento(self, evento: EventoDominio):
        """
        Maneja eventos de fallo y activa compensaciones.
        """
        try:
            paso, index = self.obtener_paso_dado_un_evento(evento)

            # Activar la compensación del paso anterior
            if index > 0:
                comando_compensacion = self.pasos[index - 1].compensacion
                self.publicar_comando(evento, comando_compensacion)
        except Exception as e:
            print(f"⚠️ Evento recibido no corresponde a una transacción de compensación: {evento}")


    def publicar_comando(self, evento, comando):
        """Publica un comando de compensación en el mismo tópico del evento original."""
        evento_compensacion = comando(id_saga=evento.id_saga)
        evento_compensacion.es_compensacion = True  # Marcar como evento de reversión
        print(f"📤 Publicando evento de compensación {comando.__name__} en {evento.topico}")

    def iniciar(self):
        """Marca el inicio de la saga en el Saga Log."""
        self.persistir_en_saga_log(self.pasos[0])

    def terminar(self):
        """Marca la finalización de la saga en el Saga Log."""
        self.persistir_en_saga_log(self.pasos[-1])




class CoordinadorOrquestacion(CoordinadorSaga, ABC):
    pasos: list[Paso]
    index: int
    
    def obtener_paso_dado_un_evento(self, evento: EventoDominio):
        for i, paso in enumerate(pasos):
            if not isinstance(paso, Transaccion):
                continue

            if isinstance(evento, paso.evento) or isinstance(evento, paso.error):
                return paso, i
        raise Exception("Evento no hace parte de la transacción")
                
    def es_ultima_transaccion(self, index):
        return len(self.pasos) - 1

    def procesar_evento(self, evento: EventoDominio):
        paso, index = self.obtener_paso_dado_un_evento(evento)
        if es_ultima_transaccion(index) and not isinstance(evento, paso.error):
            self.terminar()
        elif isinstance(evento, paso.error):
            self.publicar_comando(evento, self.pasos[index-1].compensacion)
        elif isinstance(evento, paso.evento):
            self.publicar_comando(evento, self.pasos[index+1].compensacion)