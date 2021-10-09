from typing import Union
import numpy as np

class Areas:
    def __init__(self, target, areas):
        self.groups = {}
        self.target = target
        self.areas = areas

def get_pca_coords(U, fingerprint, pca_modes):
    pca_coords = U[:, pca_modes - np.ones_like(pca_modes)].T @ fingerprint
    return pca_coords

def compare(U, fingerprintA, fingerprintB, pca_modes):
    pca_coordsA = U[:, pca_modes - np.ones_like(pca_modes)].T @ fingerprintA
    pca_coordsB = U[:, pca_modes - np.ones_like(pca_modes)].T @ fingerprintB

    similarity = calculate_similarity(pca_coordsA, pca_coordsB)
    return similarity

def calculate_similarity(pca_coordsA, pca_coordsB):
    areas = create_areas(pca_coordsA)
    pair_coords_a = create_pair_list(pca_coordsA)
    pair_coords_b = create_pair_list(pca_coordsB)
    result_a = Areas('A', areas)
    result_b = Areas('B', areas)
    init_partition(pair_coords_a, result_a)
    init_partition(pair_coords_b, result_b)
    similar = 0
    area = 0
    for i in result_a.groups.keys():
        if result_a.groups[i] > 0:
            area += result_a.groups[i]
            if result_b.groups[i] > result_a.groups[i]:
                similar += result_a.groups[i]
            else:
                similar += result_b.groups[i]
    return similar/area * 100


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

def partition(coords: list, pivots: list, axis: int, pointX: Union[object, tuple], result: Areas):
    if len(coords) == 0:
        if axis == 1:
            for pointY in pivots:
                result.groups[formatTuple(pointX) + "," + formatTuple(pointY)] = 0
    if len(pivots) == 1:
        if axis == 0:
            second_axis_partition(pivots[0], coords, result)
        else:
            pointY = pivots[0]
            result.groups[formatTuple(pointX) + "," + formatTuple(pointY)] = len(coords)
    else:
        first_half, second_half, pivot = get_pivot(pivots, axis)
        less_than, bigger_than = divide_coords(coords, pivot, axis)

        partition(less_than, first_half, axis, pointX, result)
        partition(bigger_than, second_half, axis, pointX, result)

def get_pivot(arr, axis):
    middle = len(arr) // 2
    first_half = arr[:middle]
    second_half = arr[middle:]
    if len(arr) == 2 and axis == 1:
        middle = 0
    return first_half, second_half, arr[middle]

def divide_coords(coords, pivot, axis):
    less_than = []
    bigger_than = []
    for i in coords:
        if i[axis] <= pivot[axis]:
            less_than.append(i)
        else:
            bigger_than.append(i)
    return less_than, bigger_than

def create_areas(pca_coordsA):
    maxX = max(pca_coordsA[0,:])
    maxY = max(pca_coordsA[1,:])
    minX = min(pca_coordsA[0,:])
    minY = min(pca_coordsA[1,:])

    classesX = int(np.floor(np.sqrt(len(pca_coordsA[0,:]))))
    classesY = int(np.floor(np.sqrt(len(pca_coordsA[1,:]))))

    classesX = 5
    classesY = 5

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

def formatTuple(tuple):
    return str( 
        (int(tuple[0]), int(tuple[1]))
    )