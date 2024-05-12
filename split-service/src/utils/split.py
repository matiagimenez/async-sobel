import uuid
import cv2
import os
import numpy as np


def generate_random_name(length=8):
    random_name = str(uuid.uuid4()) + '.png'
    return random_name


def split_image(image, fragments_count):
    width, height, _ = image.shape
    fragments = []

    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    # Dividir verticalmente
    fragment_width = width // fragments_count
    for i in range(fragments_count):
        fragment = image[i * fragment_width: (i + 1) * fragment_width, :]
        random_name = generate_random_name()
        path = os.path.join('tmp', random_name)
        cv2.imwrite(path, fragment)
        fragments.append(random_name)

    return fragments
