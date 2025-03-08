import os
import pulsar
import json
import logging
import threading
import uuid

from flask import Flask, jsonify, request
from src.config.config import Config

from src.modulos.ingesta.infraestructura.despachadores import Despachador
from src.modulos.ingesta.infraestructura.adaptadores.repositorios import RepositorioIngestaPostgres
from src.modulos.ingesta.aplicacion.servicios import ServicioAplicacionIngestaDatos
from src.modulos.ingesta.infraestructura.consumidores import ConsumidorComandoRevertirImportacionDatos
from src.modulos.ingesta.dominio.comandos import RevertirImportacionDatosComando
# Coordinador de Coreografía
from src.modulos.sagas.aplicacion.coordinadores.sagas_data_partnership import CoordinadorCoreografiaEventos

from src.config.db import Base, engine


# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))
config = Config()

# coordinador = CoordinadorCoreografiaEventos()
# threading.Thread(target=coordinador.escuchar_eventos, daemon=True).start()
# logger.info("✅ Coordinador Coreográfico inicializado y escuchando eventos.")

def comenzar_consumidor():
    """
    Inicia los consumidores en hilos separados.
    """
    if os.getenv("FLASK_ENV") == "test":
        logger.info("🔹 Saltando inicio de consumidores en modo test")
        return

    repositorio_ingesta = RepositorioIngestaPostgres()
    servicio_aplicacion = ServicioAplicacionIngestaDatos(repositorio_ingesta=repositorio_ingesta)
    
    consumidor_comandos_importar_datos_fallido = ConsumidorComandoRevertirImportacionDatos(servicio_aplicacion)
    threading.Thread(target=consumidor_comandos_importar_datos_fallido.suscribirse, daemon=True).start()

def create_app(configuracion=None):
    app = Flask(__name__, instance_relative_config=True)

    with app.app_context():
        if app.config.get('TESTING'):
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        Base.metadata.create_all(engine)

        if not app.config.get('TESTING'):
            comenzar_consumidor()
    

    @app.route("/health")
    def health():
        return {
            "status": "up",
            "application_name": config.APP_NAME,
            "environment": config.ENVIRONMENT
        }

    @app.route("/simular-ingesta-datos", methods=["POST"])
    def simular_ingesta_datos():
        """
        Endpoint para simular el envio de una imagen desde el proveedor
        """
        try:
            data = request.get_json()
            evento_a_fallar = data.get("evento_a_fallar", None)  # Si no se envía, será None

            repositorio_ingesta = RepositorioIngestaPostgres()
            servicio_aplicacion = ServicioAplicacionIngestaDatos(repositorio_ingesta=repositorio_ingesta)

            servicio_aplicacion.procesar_comando_importar_datos(evento_a_fallar)

            return jsonify({"message": "Datos ingestados correctamente", "failed_event": evento_a_fallar}), 200

        except Exception as e:
            logger.error(f"❌ Error al procesar la ingesta de datos: {e}")
            return jsonify({"error": "Error al procesar la ingesta de datos"}), 500
    

    @app.route("/simular-ingesta-comando-compensacion", methods=["POST"])
    def simular_comando_compensacion():
        """
        Endpoint para simular el envio de una imagen desde el proveedor
        """
        try:
            data = request.get_json()
            id_imagen_importada = data.get("id_imagen_importada", None)

            despachador = Despachador()

            comando_compensacion = RevertirImportacionDatosComando(
                id_imagen_importada = id_imagen_importada,
                es_compensacion = True
            )

            if not app.config.get('TESTING'):
                despachador.publicar_comando(comando_compensacion, "revertir-importacion-datos")

            return jsonify({"message": "Evento de compensacion publicado en `revertir-importacion-datos`"}), 200
        
        except Exception as e:
            logger.error(f"❌ Error al publicar evento de compensación en `revertir-importacion-datos`: {e}")
            return jsonify({"error": "Error al publicar evento de compensacion en `revertir-importacion-datos`"}), 500

    return app
