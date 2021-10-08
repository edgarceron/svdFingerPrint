import os
from django.conf import settings
from skimage import io
from skimage.util import img_as_int

def getArrayImage(subfolder, image):
    filename, file_extension = os.path.splitext(image)
    if file_extension == '.jpg':
        if subfolder is not None:
            return img_as_int(io.imread(os.path.join(subfolder, image), True))
        return img_as_int(io.imread(image, True))
    return None

def image_path(image):
    return settings.MEDIA_ROOT + image