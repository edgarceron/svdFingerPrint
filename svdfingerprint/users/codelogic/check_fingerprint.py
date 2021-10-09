import numpy as np
from django.conf import settings
from users.models import Users
from users.codelogic import svd, utils, compare


def check_all_fingerprints(image_relative):
    fingerprintB = utils.create_variations(settings.MEDIA_ROOT, image_relative, True)
    print(fingerprintB.shape)
    U, avgFingerprint= svd.getSvd()
    fingerprintB = fingerprintB - np.tile(avgFingerprint,(fingerprintB.shape[1],1)).T
    users = Users.objects.all().iterator()
    for person in users:
        fingerprints = get_user_fingerprints(person)
        for fingerprintA in fingerprints:
            fingerprintA = fingerprintA - np.tile(avgFingerprint,(fingerprintA.shape[1],1)).T
            similarity = compare.compare(U, fingerprintA, fingerprintB, [5,6])
            print(similarity)

def get_user_fingerprints(user: Users):
    fingerprints = [
        None if user.figerprints1 is None else np.array(user.figerprints1),
        None if user.figerprints2 is None else np.array(user.figerprints2),
        None if user.figerprints3 is None else np.array(user.figerprints3),
        None if user.figerprints4 is None else np.array(user.figerprints4),
        None if user.figerprints5 is None else np.array(user.figerprints5),
    ]
    return fingerprints