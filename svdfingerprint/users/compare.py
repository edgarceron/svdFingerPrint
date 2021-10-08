from _typeshed import NoneType
from typing import Union
import numpy as np
from users.svd import getAllFingerPrints, getAvgFingerPrint, calcSvd

IMAGE_SHAPE = (200, 200)

class Areas:
    def __init__(self, target, areas):
        self.groups = {}
        self.target = target
        self.areas = areas

def reshape(fingerprint1d):
    return fingerprint1d.reshape(IMAGE_SHAPE) 

def compare(fingerprintA, fingerPrintB, PCAModes: list):
    PCAmodes = PCAModes
    fingerprints_matrix = getAllFingerPrints()
    avgFingerprint = getAvgFingerPrint(fingerprints_matrix)
    U, S, VT = calcSvd(fingerprints_matrix, avgFingerprint)
    fingerprintA = fingerprintA - np.tile(avgFingerprint,(fingerprintA.shape[1],1)).T
    fingerPrintB = fingerPrintB - np.tile(avgFingerprint,(fingerPrintB.shape[1],1)).T

    PCACoordsA = U[:, PCAmodes - np.ones_like(PCAmodes)].T @ fingerprintA
    PCACoordsB = U[:, PCAmodes - np.ones_like(PCAmodes)].T @ fingerPrintB

    similarity = calculate_similarity(PCACoordsA, PCACoordsB)
    return similarity

def calculate_similarity(PCACoordsA, PCACoordsB):
    areas = create_areas(PCACoordsA)
    pair_coords_a = create_pair_list(PCACoordsA)
    pair_coords_b = create_pair_list(PCACoordsB)
    result_a = Areas('A', areas)
    result_b = Areas('B', areas)
    init_partition(pair_coords_a, result_a)
    init_partition(pair_coords_b, result_b)

    similar = len(pair_coords_a)
    for i in result_a.groups.keys():
        if i in result_b.groups:
            similar -= result_a.groups[i] - result_b.groups[i]

    return similar/len(pair_coords_a) * 100


def create_pair_list(coords):
    aux = []
    for i in range(len(coords[0])):
        aux.append((coords[0][i], coords[1][i]))
    return aux

def init_partition(coords: list, result: Areas):
    pivots = []
    for i in result.areas:
        pivots.append(i[0])
    partition(coords, pivots, 0, None, result)

def second_axis_partition(pointX: tuple, coords: list, result: Areas):
    for i in result.areas:
        if i[0] == pointX:
            partition(coords, i[1], 1, pointX, result)

def partition(coords: list, pivots: list(tuple), axis: int, pointX: Union[NoneType, tuple], result: Areas):
    if len(pivots) == 1:
        if axis == 0:
            second_axis_partition(pivots[0], coords, result)
        else:
            pointY = pivots[0]
            result.groups[str(pointX) + "," + str(pointY)] = len(coords)
    else:
        first_half, second_half, pivot = get_pivot(pivots)
        less_than, bigger_than = divide_coords(coords, pivot, axis)
        partition(less_than, first_half, axis, pointX, result)
        partition(bigger_than, second_half, axis, pointX, result)

def get_pivot(arr):
    middle = len(arr) // 2
    first_half = arr[:middle]
    second_half = arr[middle:]
    return first_half, second_half, arr[middle]

def divide_coords(coords, pivot, axis):
    less_than = []
    bigger_than = []
    for i in coords:
        if i[axis] <= pivot:
            less_than.append(i)
        else:
            bigger_than.append(i)
    return less_than, bigger_than

def create_areas(PCACoordsA):
    maxX = max(PCACoordsA[0,:])
    maxY = max(PCACoordsA[1,:])
    minX = min(PCACoordsA[0,:])
    minY = min(PCACoordsA[1,:])

    classesX = int(np.floor(np.sqrt(len(PCACoordsA[0,:]))))
    classesY = int(np.floor(np.sqrt(len(PCACoordsA[1,:]))))

    jumpsX = np.ceil((maxX-minX)/classesX)
    jumpsY = np.ceil((maxY-minY)/classesY)

    areas = []
    for x in range(1, classesX+1):
        pointA = ((minX + (jumpsX * (x-1))), (minX + (jumpsX * (x))))
        aux = []
        for y in range(1, classesY+1):
            pointB = ((minY + (jumpsY * (y-1))), (minY + (jumpsY * (y))))
            aux.append(pointB)
        areas.append([pointA, aux])
    return areas
