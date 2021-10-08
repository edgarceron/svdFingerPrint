import os
import numpy as np
from django.conf import settings
from skimage import io
from skimage.util import img_as_int

IMAGE_SHAPE = (200, 200)

def getArrayImage(subfolder, image):
    filename, file_extension = os.path.splitext(image)
    if file_extension == '.jpg':
        if subfolder is not None:
            return img_as_int(io.imread(os.path.join(subfolder, image), True))
        return img_as_int(io.imread(image, True))
    return None

def image_path(image_relative):
    return getArrayImage(settings.MEDIA_ROOT, image_relative)

def reshape(fingerprint1d: np.ndarray):
    return np.array(fingerprint1d).reshape(IMAGE_SHAPE)
