from abc import ABC, abstractmethod

class PuertoProcesarComandoImportarDatos(ABC):
    """
    Puerto de dominio para procesar el comando `Importar datos`.
    """
    @abstractmethod
    def procesar_comando_importar_datos(self, evento_a_fallar) -> str:
        """
        Procesa el comando de importacion de datos
        """
        ...

    @abstractmethod
    def procesar_comando_revertir_importacion(self, id_imagen_importada) -> str:
        """
        Procesa el comando de ejecución de modelos IA.
        """
        ...

