import os, time
import numpy as np
from django.conf import settings
from users.models import Users

def get_all_fingerPrints(force=False):
    if not force:
        try:
            fingerprints_matrix = np.load(os.path.join(settings.MEDIA_ROOT,'all.npy'))
            return fingerprints_matrix
        except IOError:
            print("Hubo un error al tratar de leer el archivo all")

    users = Users.objects.all().iterator()
    fingerprints_matrix = []
    for user in users:
        for i in range(1,6):
            aux = None
            if i == 1:
                aux = user.figerprints1
            elif i == 2:
                aux = user.figerprints2
            elif i == 3:
                aux = user.figerprints3
            elif i == 4:
                aux = user.figerprints4
            elif i == 5:
                aux = user.figerprints5
            
            for j in range(5):
                fingerprints_matrix.append(aux[j])

    fingerprints_matrix = np.transpose(np.array(fingerprints_matrix))
    np.save(os.path.join(settings.MEDIA_ROOT,'all.npy'), fingerprints_matrix)
    return fingerprints_matrix

def get_avg_fingerPrint(fingerprints_matrix, force=False):
    if not force:
        try:
            avgFingerprint = np.load(os.path.join(settings.MEDIA_ROOT,'avg.npy'))
        except IOError:
            print("Hubo un error al tratar de leer el archivo avg.npy")
    avgFingerprint = np.mean(fingerprints_matrix, axis=1)
    np.save(os.path.join(settings.MEDIA_ROOT,'avg.npy'), avgFingerprint)
    return avgFingerprint

def calcSvd(fingerprints_matrix, avgFingerprint, force=False):
    if not force:
        try:
            U = np.load(os.path.join(settings.MEDIA_ROOT,'svd.npy'))
            return U
        except IOError:
            print("Hubo un error al tratar de leer el archivo svd.npy")
    X = fingerprints_matrix - np.tile(avgFingerprint,(fingerprints_matrix.shape[1],1)).T
    U, S, VT = np.linalg.svd(X,full_matrices=0)
    return U

def getSvd(force=False) -> tuple[np.ndarray, np.ndarray]:

    start = time.time()
    print("Start of allFgp calc")
    fingerprints_matrix = get_all_fingerPrints(force)
    print("End of allFgp calc", time.time() - start)
    print(fingerprints_matrix.shape)
    start = time.time()
    print("Start of avg calc")
    avgFingerprint = get_avg_fingerPrint(fingerprints_matrix, force)
    print("End of avg calc", time.time() - start)

    start = time.time()
    print("Start of svd calc")
    U = calcSvd(fingerprints_matrix, avgFingerprint, force)
    print("End of svd calc", time.time() - start)
    np.save(os.path.join(settings.MEDIA_ROOT,'svd.npy'), U)
    
    return U, avgFingerprint
