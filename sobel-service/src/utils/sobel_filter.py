
import cv2
import numpy as np
import os


def filter_image(fragment):
    # Cargar la imagen desde la ruta proporcionada
    imagen = cv2.imread(os.path.join(os.getcwd(), "tmp", "pre", fragment))

    # Verificar si la imagen se ha cargado correctamente
    if imagen is None:
        print(f"Error al procesar la imagen")
        exit()

    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar el filtro de Sobel en la dirección X
    sobel_x = cv2.Sobel(imagen_gris, cv2.CV_64F, 1, 0, ksize=5)

    # Aplicar el filtro de Sobel en la dirección Y
    sobel_y = cv2.Sobel(imagen_gris, cv2.CV_64F, 0, 1, ksize=5)

    # Calcular la magnitud de los bordes
    magnitud = np.sqrt(sobel_x**2 + sobel_y**2)

    # Normalizar la magnitud para escalar los valores a un rango de 0 a 255
    magnitud = np.uint8(255 * magnitud / np.max(magnitud))

    # Guardar la imagen con los bordes detectados
    if not os.path.exists('tmp/post'):
        os.makedirs('tmp/post')

    path = os.path.join(os.getcwd(), "tmp", "post", fragment)
    cv2.imwrite(path, magnitud)
