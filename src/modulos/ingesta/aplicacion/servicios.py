from src.modulos.ingesta.dominio.entidades import ImagenMedica, MetadatosImagenMedica
from src.modulos.ingesta.dominio.puertos.repositorios import RepositorioIngesta
from src.modulos.ingesta.infraestructura.despachadores import Despachador
from src.modulos.ingesta.dominio.eventos import DatosImportadosEvento, DatosImportadosFallidoEvento
from src.modulos.ingesta.dominio.puertos.procesar_comando_modelos import PuertoProcesarComandoImportarDatos
from datetime import datetime, timezone
import logging
import uuid


# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServicioAplicacionIngestaDatos(PuertoProcesarComandoImportarDatos):
    """
    Servicio de Aplicación que gestiona la generación de DataFrames.
    """
    def __init__(self, repositorio_ingesta: RepositorioIngesta):
        self.repositorio_ingesta = repositorio_ingesta
        self.despachador = Despachador()

    def procesar_comando_revertir_importacion(self, id_imagen_importada):
        try:
            imagen_medica = self.repositorio_ingesta.obtener_por_id(id_imagen_importada)

            if imagen_medica or evento_a_fallar == 'DatosImportados':
                self.repositorio_ingesta.eliminar(id_imagen_importada)

                logger.warning(f"🔄 Reversión ejecutada: Imagen médica {id_imagen_importada} eliminada.")
            else:
                logger.warning(f"⚠️ No se encontró la imagen médica {id_imagen_importada}, no hay nada que eliminar.")

        except Exception as e:
            evento = DatosImportadosFallidoEvento(
                id_imagen_importada=id_imagen_importada,
            )

            self.despachador.publicar_evento_fallido(evento, 'datos-importados-fallido')
            logger.error(f"❌ Error al importar la imagen y evento publicado al topico datos-importados-fallido: {e}")
            raise
        
        
    def procesar_comando_importar_datos(self, evento_a_fallar):
        try:
            id_imagen = str(uuid.uuid4())
            id_metadatos = str(uuid.uuid4())

            metadatos_imagen = MetadatosImagenMedica(
                id=id_metadatos,
                ruta_metadatos_importados=f"/ruta/fake/{id_imagen}_metadatos.dcm"
            )

            imagen_medica = ImagenMedica(
                id=id_imagen,
                ruta_imagen_importada=f"/ruta/fake/{id_imagen}.dcm",
                metadatos=metadatos_imagen
            )

            self.repositorio_ingesta.agregar(imagen_medica)

            evento = DatosImportadosEvento(
                id_imagen_importada=id_imagen,
                ruta_imagen_importada=imagen_medica.ruta_imagen_importada,
                ruta_metadatos_importados=metadatos_imagen.ruta_metadatos_importados,
                evento_a_fallar=evento_a_fallar
            )

            self.despachador.publicar_evento(evento, "datos-importados")

            logger.info(f"👉 Imagen médica {imagen_medica.id} almacenada y evento publicado en `datos-importados`: {evento}")

        except Exception as e:
            logger.error(f"❌ Error al generar el imagen médica: {e}")
            raise