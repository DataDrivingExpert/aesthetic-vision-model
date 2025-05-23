from PIL import Image
import os
import random

def unir_imagenes_horizontal_centrado(lista_rutas, ancho_final=640, altura_final=360, ancho_maximo_imagen=640/2):
    """
    Crea una imagen de dimensiones específicas con una secuencia de imágenes centradas horizontalmente,
    sin espacio entre ellas, y centradas verticalmente.

    Args:
        lista_rutas: Una lista de strings con las rutas a los archivos de imagen.
        ancho_final: El ancho deseado para la imagen final.
        altura_final: La altura deseada para la imagen final.
        ancho_maximo_imagen: El ancho máximo permitido para cada imagen individual.

    Returns:
        Una instancia de la clase Image representando la imagen combinada, o None si la lista está vacía.
    """
    if not lista_rutas:
        return None

    imagenes = [Image.open(ruta) for ruta in lista_rutas]
    imagenes_redimensionadas = []
    ancho_total_imagenes = 0
    altura_maxima_imagen = 0

    for img in imagenes:
        ancho_original, alto_original = img.size
        if ancho_original > ancho_maximo_imagen:
            proporcion = ancho_maximo_imagen / ancho_original
            nuevo_ancho = int(ancho_original * proporcion)
            nuevo_alto = int(alto_original * proporcion)
            img_redimensionada = img.resize((nuevo_ancho, nuevo_alto))
        else:
            img_redimensionada = img
        imagenes_redimensionadas.append(img_redimensionada)
        ancho_total_imagenes += img_redimensionada.width
        altura_maxima_imagen = max(altura_maxima_imagen, img_redimensionada.height)

    imagen_final = Image.new('RGB', (ancho_final, altura_final), (255, 255, 255)) # Fondo blanco

    x_offset = (ancho_final - ancho_total_imagenes) // 2  # Centrado horizontal del grupo
    #y_offset = (altura_final) // 2  # Centrado vertical de cada imagen

    for index,img in enumerate(imagenes_redimensionadas):
        rand_y = random.randint(0, altura_final - img.height)
        imagen_final.paste(img, (x_offset, rand_y))
        x_offset += img.width

    return imagen_final

# Ejemplo de uso:
directorio = "Abstract"
# nombres_imagenes = [f for f in os.listdir(directorio) if os.path.isfile(os.path.join(directorio, f))]
nombres_imagenes = ['left 2.png','right 03.png']

for i in range(17):
    random.shuffle(nombres_imagenes)
    imagen_resultante = unir_imagenes_horizontal_centrado([directorio + "/" + nombre for nombre in random.sample(nombres_imagenes, k=2)])

    if imagen_resultante:
        imagen_resultante.save(f"datasets/HLM/images/train_nuevas/{250+i}_abstract_secuence.png")
        print("Secuencia de imágenes unida y guardada")
    else:
        print("No se proporcionaron rutas de imágenes.")
        print(imagen_resultante)