import os, numpy as np
from PIL.Image import Image
from django.core.management.base import BaseCommand
from matplotlib import pyplot as plt
from numpy.lib.type_check import imag
from skimage import io, color
from skimage.util import img_as_int
from users.models import Users

class Command(BaseCommand):
    help = 'Carga los usuarios desde la ruta especificada, cada subcarpeta dentro de la ruta sera un usuario'

    def add_arguments(self, parser):
        parser.add_argument('ruta', type=str, help='Ruta de la carpeta')

    def handle(self, *args, **kwargs):
        ruta = kwargs['ruta']
        list_subfolders = [ f.path for f in os.scandir(ruta) if f.is_dir()]
        for subfolder in list_subfolders:
            dirname = os.path.basename(subfolder)
            if Command.check_user(dirname):
                user = Users.objects.create(name=dirname)

                onlyfiles = [f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder, f))]
                images = []
                for image in onlyfiles:
                    filename, file_extension = os.path.splitext(image)
                    if file_extension == '.jpg':
                        images.append(img_as_int(io.imread(subfolder + '\\' +image, True)))
                
                for i in range(len(images)):
                    if i == 0:
                        user.figerprint1 = images[i].flatten()
                    elif i == 1:
                        user.figerprint2 = images[i].flatten()
                    elif i == 2:
                        user.figerprint3 = images[i].flatten()
                    elif i == 3:
                        user.figerprint4 = images[i].flatten()
                    elif i == 4:
                        user.figerprint5 = images[i].flatten()
                
                user.save()

    @staticmethod
    def check_user(name):
        try:
            Users.objects.get(name=name)
            return False
        except Users.DoesNotExist:
            return True