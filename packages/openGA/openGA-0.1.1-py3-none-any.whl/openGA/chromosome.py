"""
chromosome for genetic algorithm
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

from __future__ import annotations
import logging
import numpy as np
from typing import Union, List, Tuple
from .utils import limit, GENE_MIN, GENE_MAX

logger = logging.getLogger('openGA')


def get_crossover_coef(eta: Union[int, float] = 20) -> float:
    u = np.random.uniform()
    k = 1 / (eta + 1)
    if u <= 0.5:
        rlt = (2 * u) ** k
    else:
        rlt = (2 * (1 - u)) ** -k
    return rlt


def get_mutation_coef(eta: Union[int, float] = 20) -> float:
    u = np.random.uniform()
    k = 1 / (eta + 1)
    if u < 0.5:
        rlt = (2 * u) ** k - 1
    else:
        rlt = 1 - (2 * (1 - u)) ** k
    return rlt


class Chromosome(object):
    """
    create chromosome with gene in [0,1]
    """

    def __init__(self, gene_names: List[str], check: bool = True) -> None:
        self._check = check
        self._gene_num = len(gene_names)
        self._gene_names = gene_names.copy()
        self._gene_values = np.zeros(self._gene_num)

    @property
    def check(self):
        return self._check

    @check.setter
    def check(self, active: bool):
        self._check = active

    @property
    def gene_values(self):
        return self._gene_values.copy()

    def _update(self, value: float, index: int):
        if not GENE_MIN <= value <= GENE_MAX and self._check:
            value_set = limit(value)
            logger.warning(
                'get out of boundary value [%6.4f], limit to [%6.4f]' % (value, value_set))
        else:
            value_set = value
        self._gene_values[index] = value_set

    def is_couple(self, couple: Chromosome) -> bool:
        if self._gene_num != couple._gene_num:
            logger.info('Not couple for unbalance gene number')
            return False
        for i in range(self._gene_num):
            if self._gene_names[i] != couple._gene_names[i]:
                logger.info('Not couple for unmatch gene name at [%d]: [%s]-[%s]' % (
                    i, self._gene_names[i], couple._gene_names[i]))
                return False
        return True

    def random(self) -> None:
        for i in range(self._gene_num):
            self._update(np.random.uniform(GENE_MIN, GENE_MAX), i)

    def crossover(self, couple: Chromosome, eta: Union[int, float] = 20) -> Tuple[Chromosome, Chromosome]:
        if self._check:
            if not self.is_couple(couple):
                raise ValueError('couple unmatch, can not crossover')
        offspring_0 = Chromosome(self._gene_names, self._check)
        offspring_1 = Chromosome(self._gene_names, self._check)
        for i in range(self._gene_num):
            p0_gene_val = self._gene_values[i]
            p1_gene_val = couple.gene_values[i]
            beta = get_crossover_coef(eta)
            a = 1 - beta
            b = 1 + beta
            c0_gene_val = limit(0.5 * (a * p0_gene_val + b * p1_gene_val))
            c1_gene_val = limit(0.5 * (b * p0_gene_val + a * p1_gene_val))
            offspring_0._update(c0_gene_val, i)
            offspring_1._update(c1_gene_val, i)
        return offspring_0, offspring_1

    def mutate(self, eta: Union[int, float] = 20) -> Chromosome:
        offspring = Chromosome(self._gene_names)
        for i in range(self._gene_num):
            p_gene_val = self._gene_values[i]
            theta = get_mutation_coef(eta)
            c_gene_val = limit(p_gene_val + theta)
            offspring._update(c_gene_val, i)
        return offspring

    def copy(self) -> Chromosome:
        twin = Chromosome(self._gene_names, self._check)
        for i in range(self._gene_num):
            twin._update(self._gene_values[i], i)
        return twin
