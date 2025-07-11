"""
Toma datos crudos desde la UI (imágenes, opciones del usuario) y los valida/preprocesa.
"""

from PIL import Image
import os


class Preprocessor:
    """
    Clase para preprocesar imágenes antes de la inferencia.
    """

    def __init__(self, data):
        self.data = data

        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_dir,'..','..','outputs','preprocessed_img')
        self.output_path = os.path.normpath(output_dir)
        os.makedirs(self.output_path, exist_ok=True)

    def perform(self, image_path):
        """
        Preprocesa una imagen: la convierte a PNG, redimensiona (si es necesario) y la guarda en un directorio específico.

        :param image_path: Ruta de la imagen a preprocesar.
        :return: Ruta de la imagen preprocesada.
        """
        for image_path in self.data:
            # Convertir a PNG
            png_path = self.__convert_to_png(image_path)
            # Redimensionar imagen
            resized_image = self.__resize_image(png_path)
            # Convertir a escala de grises
            grayscale_image = self.__convert_to_grayscale(resized_image)
            
            # Guardar imagen preprocesada
            filename = os.path.splitext(os.path.basename(image_path))[0] + ".png"
            save_path = os.path.join(self.output_path, filename)
            
            grayscale_image.save(save_path, format="PNG")
            
    @staticmethod
    def retrieve_valid_files(dir_path:str):
        valid_ext = {'.png', '.jpg', '.jpeg'}
        img_path = []

        for root, dirs, files in os.walk(dir_path):
            for fl in files:
                _, extension = os.path.splitext(fl)
                if extension.lower() in valid_ext:
                    ruta_completa = os.path.join(root, fl)
                    img_path.append(ruta_completa)

        return img_path

    def __convert_to_png(self, input_path):
        # Abrir imagen
        img = Image.open(input_path)

        # Convertir a RGB si tiene modo incompatible (como 'P' o 'RGBA')
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        return img

    def __resize_image(self, img, max_size=(640, 640)):
        img.thumbnail(max_size, Image.LANCZOS)  # LANCZOS = alta calidad de reescalado
        return img
    
    def __convert_to_grayscale(self, img):
        grayscale_img = img.convert("L")
        return grayscale_img

