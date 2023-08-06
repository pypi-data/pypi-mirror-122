"""
test cases for individual
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import unittest

from openGA import Individual, Chromosome


class TestIndividual(unittest.TestCase):

    def setUp(self) -> None:
        gene_name = ['a', 'b', 'c', 'd']
        plasm_0 = Chromosome(gene_name, check=False)
        plasm_0.random()
        plasm_0._update(0.1, 0)
        plasm_1 = plasm_0.copy().mutate()
        self.idv_0 = Individual(0, 0, plasm=plasm_0)
        self.idv_1 = Individual(0, 1, plasm=plasm_1)

    def test_init(self):
        self.assertEqual(self.idv_0.gen_id, 0)
        self.assertEqual(self.idv_0.idv_id, 0)
        self.idv_1.gen_id = 2
        self.idv_1.idv_id = 5
        self.assertEqual(self.idv_1.gen_id, 2)
        self.assertEqual(self.idv_1.idv_id, 5)
        with self.assertRaises(ValueError):
            self.idv_0.fittness
        self.assertIs(self.idv_0._fittness, None)


if __name__ == "__main__":
    unittest.main()
