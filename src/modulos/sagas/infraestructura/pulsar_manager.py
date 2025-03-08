import pulsar
from src.config.config import Config

config = Config()

class PulsarManager:
    """Maneja una conexión única de Apache Pulsar para ser reutilizada en toda la aplicación"""
    _cliente = None

    @classmethod
    def obtener_cliente(cls):
        if cls._cliente is None:
            cls._cliente = pulsar.Client(f"pulsar://{config.BROKER_HOST}:{config.BROKER_PORT}")
        return cls._cliente

    @classmethod
    def cerrar_cliente(cls):
        if cls._cliente:
            cls._cliente.close()
            cls._cliente = None
