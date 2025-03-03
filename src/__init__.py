import os
import pulsar
import json
import logging
import threading

from flask import Flask, jsonify
from src.config.config import Config

# Modulo de ingesta (Mock)
from src.modulos.ingesta.infraestructura.despachadores import Despachador
from src.modulos.ingesta.dominio.eventos import DatosImportadosEvento

from src.config.db import Base, engine

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))
config = Config()

pulsar_cliente = None
if os.getenv("FLASK_ENV") != "test":
    pulsar_cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:{config.BROKER_PORT}')

def comenzar_consumidor():
    """
    Inicia el consumidor en un hilo separado, pasando el servicio de aplicación.
    """

    if os.getenv("FLASK_ENV") == "test":
        logger.info("🔹 Saltando inicio de consumidores en modo test")


def create_app(configuracion=None):
    global pulsar_cliente

    app = Flask(__name__, instance_relative_config=True)

    with app.app_context():
        if app.config.get('TESTING'):
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        Base.metadata.create_all(engine) 
        if not app.config.get('TESTING'):
            comenzar_consumidor()

    despachador_ingesta = Despachador()

    

    @app.route("/health")
    def health():
        return {
            "status": "up",
            "application_name": config.APP_NAME,
            "environment": config.ENVIRONMENT
        }

    @app.route("/simular-ingesta-evento", methods=["GET"])
    def simular_ingesta_evento():
        """
        Endpoint para probar la publicación de comandos en Pulsar.
        """
        try:
            datos_importados = DatosImportadosEvento(
                ruta_imagen="/ruta/fake/imagen.dcm",
                ruta_metadatos="/ruta/fake/metadatos.pdf",
            )

            if not app.config.get('TESTING'):
                despachador_ingesta.publicar_evento(datos_importados, "datos-importados")

            return jsonify({"message": "Evento publicado en `datos-importados`"}), 200
        except Exception as e:
            logger.error(f"❌ Error al publicar evento de prueba: {e}")
            return jsonify({"error": "Error al publicar evento a Pulsar"}), 500

    

    # Cerrar Pulsar cuando la aplicación termina
    @app.teardown_appcontext
    def cerrar_pulsar(exception=None):
        global pulsar_cliente
        if pulsar_cliente:
            pulsar_cliente.close()
            logger.info("Cliente Pulsar cerrado al detener Flask.")

    return app
