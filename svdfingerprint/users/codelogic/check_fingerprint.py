import numpy as np
from users.models import Users
from users.codelogic import svd, utils, compare


def check_all_fingerprints(image_relative):
    fingerprintB = utils.image_path(image_relative).flatten()
    U, avgFingerprint= svd.getSvd()
    print(str(avgFingerprint.shape))
    print(str((fingerprintB.shape)))
    fingerprintB = fingerprintB - avgFingerprint.T
    users = Users.objects.all()
    for person in users:
        fingerprints = get_user_fingerprints(person)
        for fingerprintA in fingerprints:
            fingerprintA = fingerprintA - avgFingerprint.T
            similarity = compare.compare(U, fingerprintA, fingerprintB, [5,6])
            print(similarity)

def get_user_fingerprints(user: Users):
    fingerprints = [
        None if user.figerprint1 is None else np.array(user.figerprint1),
        None if user.figerprint2 is None else np.array(user.figerprint2),
        None if user.figerprint3 is None else np.array(user.figerprint3),
        None if user.figerprint4 is None else np.array(user.figerprint4),
        None if user.figerprint5 is None else np.array(user.figerprint5),
    ]
    return fingerprints