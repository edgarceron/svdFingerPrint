from re import U
import numpy as np
from django.conf import settings
from users.models import Users
from users.codelogic import svd, utils, compare

PCAMODES = [9,10]
SIMILARITY_MESSAGE = "Se encontro una similaridad de {:10.4f} con el dedo {} de la persona {}"

def check_all_fingerprints(image_relative: str) -> dict:
    image = utils.get_array_image(settings.MEDIA_ROOT, image_relative)
    if image is not None:
        fingerprintB = utils.create_variations(settings.MEDIA_ROOT, image_relative, image, True, utils.get_variation_qty())
        fingerprintB = np.transpose(np.array(fingerprintB))
        print(fingerprintB.shape)
        U, avgFingerprint= svd.getSvd()
        fingerprintB = fingerprintB - np.tile(avgFingerprint,(fingerprintB.shape[1],1)).T
        users = Users.objects.all().iterator()
        pca_coords_b = compare.get_pca_coords(U, fingerprintB, PCAMODES)
        for person in users:
            for i in range(5):
                fingerprintA = iterate_finger_prints(person, i)
                fingerprintA = fingerprintA - np.tile(avgFingerprint,(fingerprintA.shape[1],1)).T
                pca_coords_a = compare.get_pca_coords(U, fingerprintA, PCAMODES)
                similarity = compare.calculate_similarity(pca_coords_a, pca_coords_b)
                if(similarity > 80):
                    return {
                        "similarity": "{:10.4f}".format(similarity),
                        "message": SIMILARITY_MESSAGE.format(similarity, i, person.name)
                    }
        return {
            "similarity": 0,
            "message": "No se encontraron huellas con más de 80 porciento de smilitud"
        }
    return {
        "similarity": 0,
        "message": "La imagen debe ser jpg y de tamaño 200x200"
    }

def iterate_finger_prints(user: Users, i: int) -> np.ndarray:
    if i == 0:
        f = None if user.figerprints1 is None else user.figerprints1
    elif i == 1:
        f = None if user.figerprints2 is None else user.figerprints2
    elif i == 2:
        f = None if user.figerprints3 is None else user.figerprints3
    elif i == 3:
        f = None if user.figerprints4 is None else user.figerprints4
    else:
        f = None if user.figerprints5 is None else user.figerprints5
    return np.transpose(np.array(f))
