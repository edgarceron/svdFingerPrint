import os
from django.core.management.base import BaseCommand
from numpy.lib.type_check import imag
from users.models import Users
from users import utils

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
    def check_user(name):
        try:
            Users.objects.get(name=name)
            return False
        except Users.DoesNotExist:
            return True