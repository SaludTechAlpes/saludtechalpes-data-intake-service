from abc import ABC, abstractmethod

class Consumidor(ABC):
    """
    Clase abstracta base para consumidores de eventos en DDD.
    Define la estructura básica para cualquier consumidor de eventos.
    """

    def __init__(self, topico: str, suscripcion: str):
        """
        Inicializa el consumidor con su tópico y suscripción.
        """
        self.topico = topico
        self.suscripcion = suscripcion

    @abstractmethod
    def suscribirse(self):
        """
        Método abstracto que las implementaciones deben definir para manejar la suscripción.
        """
        pass

    @abstractmethod
    def procesar_mensaje(self, mensaje):
        """
        Método abstracto para procesar el mensaje recibido.
        """
        pass

    @abstractmethod
    def cerrar(self):
        """
        Método abstracto para cerrar la conexión con el sistema de mensajería.
        """
        pass
