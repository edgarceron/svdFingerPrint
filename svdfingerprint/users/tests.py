import numpy as np
from django.test import TestCase
from users import compare
# Create your tests here.



class SvdTestCase(TestCase):

    def test_areas(self):

        PCACoordsTestA = np.array([
            np.array([x for x in range(100)]),
            np.array([x for x in range(100)])
        ])

        PCACoordsB = np.array([
            np.array([x for x in range(100)]),
            np.array([x for x in range(100)])
        ])

        areas = compare.create_areas(PCACoordsTestA)
        self.assertEqual(len(areas), 10)
        self.assertEqual(type(areas[0][0]), tuple)
        self.assertEqual(len(areas[0][0]), 2)
        self.assertEqual(type(areas[0][1]), list)
        self.assertEqual(type(areas[0][1][0]), tuple)
        self.assertEqual(len(areas[0][1][0]), 2)
        self.assertEqual(len(areas[0][1]), 10)
        
        pair_coords_a = compare.create_pair_list(PCACoordsTestA)

        self.assertEqual(len(pair_coords_a), 100)
        self.assertEqual(type(pair_coords_a[0]), tuple)

        result_a = compare.Areas('A', areas)
        compare.init_partition(pair_coords_a, result_a)
        total = 0
        for i in result_a.groups:
            total += result_a.groups[i]
        
        self.assertEqual(total, 100)

        #sim = compare.calculate_similarity(PCACoordsTestA, PCACoordsB)
        #self.assertEqual(sim, 100)

        PCACoordsTestC = np.array([
            np.array([x for x in range(100, 0, -1)]),
            np.array([x for x in range(100)])
        ])

        result_c = compare.Areas('C', areas)
        pair_coords_c = compare.create_pair_list(PCACoordsTestC)
        compare.init_partition(pair_coords_c, result_c)

        sim2 = compare.calculate_similarity(PCACoordsTestA, PCACoordsTestC)
        print(sim2)
        self.assertLessEqual(sim2, 20)


