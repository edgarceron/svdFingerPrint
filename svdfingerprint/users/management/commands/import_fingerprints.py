import os
from typing import Tuple
from PIL import Image
from django.core.management.base import BaseCommand
from numpy.lib.type_check import imag
from users.models import Users
from users.codelogic import utils

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
                user = Users()
                user.name = dirname
                onlyfiles = [f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder, f))]
                images = []
                for image in onlyfiles:
                    result = utils.getArrayImage(subfolder, image)
                    if result is not None: 
                        images.append(result)
                
                for i in range(len(images)):
                    fgp = images[i].flatten().tolist()
                    if i == 0:
                        user.figerprint1 = fgp
                    elif i == 1:
                        user.figerprint2 = fgp
                    elif i == 2:
                        user.figerprint3 = fgp
                    elif i == 3:
                        user.figerprint4 = fgp
                    elif i == 4:
                        user.figerprint5 = fgp
                
                user.save()
    
    @staticmethod
    def create_variations(subfolder, image):
        image_path = os.path.join(subfolder, image)


        names = ["rp5", "rm5", "tl5", "tr5"]
        variation = [
            [(.95, 1), (.05, 0), (10, 0)],
            [(.95, 1), (-.05, 0), (-10, 0)],
            [(1, .95), (0, -.1), (0, 10)],
            [(1, .95), (0, .1), (0, -10)],
            [(1.05, 1), (0, 0), (0, 0)],
            [(1, 1), (0, 0), (5, 0)],
            [(1, 1), (0, 0), (-5, 0)],
            [(1, 1), (.01, 0), (-5, 0)]
            [(.95, .95), (0, 0), (0, 0)],
            [(.95, .95), (0, 0), (5, 0)],
            [(.95, .95), (-.01, 0), (5, 0)],
            [(.95, .95), (0, 0), (-5, 0)],
            [(.95, .95), (.01, 0), (-5, 0)]
            [(.95, .95), (0, 0), (0, 5)],
            [(.95, .95), (0, 0), (0, -5)],
            [(.93, .93), (0, 0), (0, 0)],
            [(.93, .93), (0, 0), (5, 0)],
            [(.93, .93), (-.01, 0), (5, 0)],
            [(.93, .93), (0, 0), (-5, 0)],
            [(.93, .93), (.01, 0), (-5, 0)]
            [(.93, .93), (0, 0), (0, 5)],
            [(.93, .93), (0, 0), (0, -5)],
            [(1.04, .95), (0, 0), (0, 0)],
            [(1.04, .95), (0, 0), (5, 0)],
            [(1.04, .95), (-.01, 0), (5, 0)],
            [(1.04, .95), (0, 0), (-5, 0)],
            [(1.04, .95), (.01, 0), (-5, 0)]
            [(1.04, .95), (0, 0), (0, 5)],
            [(1.04, .95), (0, 0), (0, -5)],
            [(1.04, .93), (0, 0), (0, 0)],
            [(1.04, .93), (0, 0), (5, 0)],
            [(1.04, .93), (-.01, 0), (5, 0)],
            [(1.04, .93), (0, 0), (-5, 0)],
            [(1.04, .93), (.01, 0), (-5, 0)]
            [(1.04, .93), (0, 0), (0, 5)],
            [(1.04, .93), (0, 0), (0, -5)],
        ]
        try:
            with Image.open(infile) as im:
                
                im.save(outfile1)
        except OSError:
            print("cannot convert", infile)

    @staticmethod
    def apply_variation(image_path: str, strecth: Tuple, angle: Tuple, translate: Tuple):
        original_Image = Image.open(image_path)
        try:
            with Image.open(original_Image) as im:
                im.rotate(angle, fillcolor=255)
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
            print("cannot convert", infile)
            return None


    @staticmethod
    def check_user(name):
        try:
            Users.objects.get(name=name)
            return False
        except Users.DoesNotExist:
            return True