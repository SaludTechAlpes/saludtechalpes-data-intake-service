from enum import Enum

class EtiquetaPatologica(Enum):
    NORMAL = "Normal"
    ANORMAL = "Anormal"
    BENIGNO = "Benigno"
    MALIGNO = "Maligno"
    NEUMONIA = "Neumonía"
    INFARTO = "Infarto"
    FRACTURA = "Fractura"
    TUMOR = "Tumor"
    ARTRITIS = "Artritis"
    INFECCION = "Infección"
    ANOMALIA_CONGENITA = "Anomalía congénita"
    DEFAULT = "Default"

class Modalidad(Enum):
    RAYOS_X = "Rayos X"
    TOMOGRAFIA = "Tomografía"
    RESONANCIA_MAGNETICA = "Resonancia Magnética"
    ULTRASONIDO = "Ultrasonido"
    MAMOGRAFIA = "Mamografía"
    ESCANEO_TEP = "Escaneo TEP"
    HISTOPATOLOGIA = "Histopatología"
    DEFAULT = "Default"

class RegionAnatomica(Enum):
    CEREBRO = "Cerebro"
    TORAX = "Tórax"
    ABDOMEN = "Abdomen"
    MUSCULOESQUELETICO = "Musculoesquelético"
    PELVIS = "Pélvis"
    CUERPO_COMPLETO = "Cuerpo Completo"
    DEFAULT = "Default"
