import numpy as np
from django.test import TestCase
from users import compare
# Create your tests here.



class SvdTestCase(TestCase):

    def test_areas(self):

        PCACoordsA = np.array([
            np.array([x for x in range(100)]),
            np.array([x for x in range(100)])
        ])

        PCACoordsB = np.array([
            np.array([x for x in range(100)]),
            np.array([x for x in range(100)])
        ])

        areas = compare.create_areas(PCACoordsA)
        self.assertEqual(len(areas), 10)
        self.assertEqual(type(areas[0][0]), tuple)
        self.assertEqual(len(areas[0][0]), 2)
        self.assertEqual(type(areas[0][1]), list)
        self.assertEqual(type(areas[0][1][0]), tuple)
        self.assertEqual(len(areas[0][1][0]), 2)
        self.assertEqual(len(areas[0][1]), 10)
        print(areas)

        


