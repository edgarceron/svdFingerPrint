import os, string
import numpy as np
from typing import Tuple
from PIL import Image
from django.conf import settings
from numpy.core.fromnumeric import var
from skimage import io
from skimage.util import img_as_int

IMAGE_SHAPE = (200, 200)
LETTERS = string.ascii_lowercase
TRANSFOMS = [
    [(.95, 1), (.05, 0), (10, 0)],
    [(.95, 1), (-.05, 0), (-10, 0)],
    [(1, .95), (0, -.1), (0, 10)],
    [(1, .95), (0, .1), (0, -10)],
    [(1.05, 1), (0, 0), (0, 0)],
    [(1, 1), (0, 0), (5, 0)],
    [(1, 1), (0, 0), (-5, 0)],
    [(1, 1), (.01, 0), (-5, 0)],
    [(.95, .95), (0, 0), (0, 0)],
    [(.95, .95), (0, 0), (5, 0)],
    [(.95, .95), (-.01, 0), (5, 0)],
    [(.95, .95), (0, 0), (-5, 0)],
    [(.95, .95), (.01, 0), (-5, 0)],
    [(.95, .95), (0, 0), (0, 5)],
    [(.95, .95), (0, 0), (0, -5)],
    [(.93, .93), (0, 0), (0, 0)],
    [(.93, .93), (0, 0), (5, 0)],
    [(.93, .93), (-.01, 0), (5, 0)],
    [(.93, .93), (0, 0), (-5, 0)],
    [(.93, .93), (.01, 0), (-5, 0)],
    [(.93, .93), (0, 0), (0, 5)],
    [(.93, .93), (0, 0), (0, -5)],
    [(1.04, .95), (0, 0), (0, 0)],
    [(1.04, .95), (0, 0), (5, 0)],
    [(1.04, .95), (-.01, 0), (5, 0)],
    [(1.04, .95), (0, 0), (-5, 0)],
    [(1.04, .95), (.01, 0), (-5, 0)],
    [(1.04, .95), (0, 0), (0, 5)],
    [(1.04, .95), (0, 0), (0, -5)],
    [(1.04, .93), (0, 0), (0, 0)],
    [(1.04, .93), (0, 0), (5, 0)],
    [(1.04, .93), (-.01, 0), (5, 0)],
    [(1.04, .93), (0, 0), (-5, 0)],
    [(1.04, .93), (.01, 0), (-5, 0)],
    [(1.04, .93), (0, 0), (0, 5)],
    [(1.04, .93), (0, 0), (0, -5)],
]

def get_array_image(subfolder, image):
    filename, file_extension = os.path.splitext(image)
    if file_extension == '.jpg':
        if subfolder is not None:
            return img_as_int(io.imread(os.path.join(subfolder, image), True))
        return img_as_int(io.imread(image, True))
    return None

def reshape(fingerprint1d: np.ndarray):
    return np.array(fingerprint1d).reshape(IMAGE_SHAPE)

def create_variations(subfolder: str, image: str, flat=False) -> np.ndarray:
    image_path = os.path.join(subfolder, image) 
    name = str(os.path.splitext(image)[0])
    variations = [get_array_image(subfolder, image).flatten()]

    for i in range(len(TRANSFOMS)):
        im = apply_variation(image_path, *TRANSFOMS[i])
        folder_path = os.path.join(subfolder,name)
        os.makedirs(folder_path) if not os.path.exists(folder_path) else None
        new_image_path = os.path.join(folder_path, str(i) + '.jpg')
        im.save(new_image_path)
        im_array = img_as_int(io.imread(new_image_path, True))
        variation = im_array.flatten() if flat else im_array
        variations.append(variation)

    return np.transpose(np.array(variations))

def apply_variation(image_path: str, strecth: Tuple, angle: Tuple, translate: Tuple) -> Image.Image:
    try:
        with Image.open(image_path) as im:
            im = im.transform(
                im.size, 
                Image.AFFINE, 
                (
                    strecth[0], 
                    angle[0], 
                    translate[0], 
                    angle[1], 
                    strecth[1], 
                    translate[1]
                ), 
                fillcolor=(255,255,255)
            )
            return im
    except OSError:
        print("cannot convert")
        return None