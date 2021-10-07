import time
import numpy as np
from users.models import Users

def getAllFingerPrints():
    users = Users.objects.all()
    fingerprints_matrix = []
    for user in users:
        for i in range(1,6):
            aux = None
            if i == 1:
                aux = user.figerprint1
            elif i == 2:
                aux = user.figerprint2
            elif i == 3:
                aux = user.figerprint3
            elif i == 4:
                aux = user.figerprint4
            elif i == 5:
                aux = user.figerprint5
            
            if aux is not None:
                fingerprints_matrix.append(aux)
    
    return np.transpose(np.array(fingerprints_matrix))

def getAvgFingerPrint(fingerprints_matrix):
    avgFingerprint = np.mean(fingerprints_matrix, axis=1)
    return avgFingerprint

def calcSvd(fingerprints_matrix, avgFingerprint):
    X = fingerprints_matrix - np.tile(avgFingerprint,(fingerprints_matrix.shape[1],1)).T
    U, S, VT = np.linalg.svd(X,full_matrices=0)
    return U, S, VT

def getSvd():
    start = time.time()
    fingerprints_matrix = getAllFingerPrints()
    avgFingerprint = getAvgFingerPrint(fingerprints_matrix)
    U, S, VT = calcSvd(fingerprints_matrix, avgFingerprint)
    end = time.time()
    print(end - start)
    print(len(U))

def detect(fingerprints_matrix):
    for i in fingerprints_matrix:
        if not(type(i) == np.ndarray):
            print(type(i))
            break