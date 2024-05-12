import cv2
import os
import numpy as np


def join_image(fragments, task_id):
    # Cargar los fragmentos de imagen
    fragment_images = [cv2.imread(os.path.join(
        os.getcwd(), "tmp", "fragments", fragment)) for fragment in fragments]

    # Obtener el tamaño de la primera imagen para crear la imagen final
    height, width, channels = fragment_images[0].shape
    num_fragments = len(fragments)

    # Crear una imagen vacía para unir los fragmentos
    joined_image = np.zeros(
        (height * num_fragments, width, channels), dtype=np.uint8)

    # Concatenar los fragmentos en la imagen final
    for i in range(num_fragments):
        fragment = fragment_images[i]
        joined_image[i*height: (i+1)*height, :] = fragment

    if not os.path.exists('tmp/results'):
        os.makedirs('tmp/results')

    path = os.path.join('tmp', "results", f"{task_id}.png")
    cv2.imwrite(path, joined_image)
