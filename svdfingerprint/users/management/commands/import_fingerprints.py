import os
from django.core.management.base import BaseCommand
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

                for i in range(len(onlyfiles)):
                    variations = utils.create_variations(subfolder, onlyfiles[i])

                    for j in range(len(variations)):
                        variations[j] = variations[j].flatten().tolist()
                    
                    if i == 0:
                        user.figerprints1 = variations
                    elif i == 1:
                        user.figerprints2 = variations
                    elif i == 2:
                        user.figerprints3 = variations
                    elif i == 3:
                        user.figerprints4 = variations
                    elif i == 4:
                        user.figerprints5 = variations

                    variations = []
                user.save()
    
    @staticmethod
    def check_user(name):
        try:
            Users.objects.get(name=name)
            return False
        except Users.DoesNotExist:
            return True