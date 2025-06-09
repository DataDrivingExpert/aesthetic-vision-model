"""
Carga el modelo (si no está cargado) y ejecuta inferencias con datos preprocesados.
"""

from ultralytics import YOLO
import torch

class InferenceRunner(object):
    """
    Clase para cargar el modelo y ejecutar inferencias.
    """

    def __init__(self, model_path: str):
        """
        Inicializa la clase con la ruta del modelo.

        :param model_path: Ruta del modelo.
        """
        self.model_path = model_path
        self.model = YOLO(self.model_path)

    
    def __get_device(self):
        if torch.cuda.is_available():
            return 'cuda'
        else:
            return 'cpu'


    def predict(self, image_path):
        """
        Realiza la inferencia en una imagen o en un lote de imágenes 
        y devuelve los resultados.

        :param image_path: Ruta de la/s imagen/imágenes.
        :return: Resultados de la inferencia.
        """
        results = self.model.predict(
            iou=0.01,
            conf=0.25,
            device=self.__get_device(),
            agnostic_nms=True,
            source=image_path,
            save=True,
            project='outputs',
            name='predictions/images',
            exist_ok=True,
            verbose=False
            )

        return results