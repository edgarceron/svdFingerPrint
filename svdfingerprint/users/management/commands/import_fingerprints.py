import os
from django.core.management.base import BaseCommand
from users.models import Users, Config
from users.codelogic import utils
from django.conf import settings


class Command(BaseCommand):
    help = 'Carga los usuarios desde la ruta especificada, cada subcarpeta dentro de la ruta sera un usuario'

    def add_arguments(self, parser):
        parser.add_argument('ruta', type=str, help='Ruta de la carpeta')
        parser.add_argument('variation_qty', type=int, help='Cantidad de variaciones para cada imagen, se sugiere un numero menor a 10. 5 <= variation_qty <= 36')

    def handle(self, *args, **kwargs):
        ruta = kwargs['ruta']
        variation_qty = kwargs['variation_qty']
        utils.create_update_variation_qty(variation_qty)
        list_subfolders = [ f.path for f in os.scandir(ruta) if f.is_dir()]
        for subfolder in list_subfolders:
            dirname = os.path.basename(subfolder)
            if Command.check_user(dirname):
                user = Users()
                user.name = dirname
                onlyfiles = [f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder, f))]

                for i in range(len(onlyfiles)):
                    image = utils.get_array_image(settings.MEDIA_ROOT, onlyfiles[i])
                    variations = utils.create_variations(settings.MEDIA_ROOT, onlyfiles[i], image, True, utils.get_variation_qty())

                    for j in range(len(variations)):
                        variations[j] = variations[j].tolist()
                    
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