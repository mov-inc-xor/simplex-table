from fractions import Fraction
from functools import reduce


def map_fraction(obj):
    if not isinstance(obj, list):
        return Fraction(obj)
    return [map_fraction(el) for el in obj]


class SimpleSimplexTable:
    def __init__(self, a, b, z, basis_vars, var_name='x', func_name='z'):
        self._a = map_fraction(a)
        self._b = map_fraction(b)
        self._z = map_fraction(z)

        self._basis_vars = basis_vars.copy()
        self._var_name = var_name
        self._func_name = func_name

        self._z = [self._z[0]] + list(map(lambda x: -x, self._z[1:]))

        self.to_basic_form()

    def __str__(self):
        m = len(self._z) - 1
        w = 10

        def fmt(row):
            return [f'{str(el) : >{w}}' for el in row]

        def rdc(row):
            return reduce(lambda a, b: str(a) + str(b), row) + '\n'

        table_head = ['БП', 'СЧ'] + [f'{self._var_name}{i}' for i in range(1, m + 1)]
        table_head = rdc(fmt(table_head))

        table_main = str()

        for (basis_var, ai, bi) in zip(self._basis_vars, self._a, self._b):
            table_row = [f'{self._var_name}{basis_var + 1}', str(bi)] + [str(el) for el in ai]
            table_main += rdc(fmt(table_row))

        table_body = rdc(fmt([f'{self._func_name}'] + self._z))
        return table_head + table_main + table_body

    def to_basic_form(self):
        for (i, v) in enumerate(self._basis_vars):
            self.swap(i, v)

    def solved(self):
        return not list(filter(lambda x: x < 0, self._z[1:]))

    def select_resolution_element(self):
        j = None
        for (ind, el) in enumerate(self._z[1:]):
            if el < 0:
                j = ind
                break
        i = None
        min_ratio = None
        for ind in range(len(self._a)):
            if self._a[ind][j] > 0:
                if not min_ratio or min_ratio > abs(self._b[ind] / self._a[ind][j]):
                    i = ind
                    min_ratio = abs(self._b[ind] / self._a[ind][j])
        return i, j

    def swap(self, i, j):
        el = self._a[i][j]
        self._a[i] = list(map(lambda x: x / el, self._a[i]))
        self._b[i] /= el

        for ind in range(len(self._a)):
            if ind == i:
                continue
            k = self._a[ind][j]
            for ind1 in range(len(self._a[ind])):
                self._a[ind][ind1] -= k * self._a[i][ind1]
            self._b[ind] -= k * self._b[i]

        k = self._z[j + 1]
        for ind1 in range(len(self._a[i])):
            self._z[ind1 + 1] -= k * self._a[i][ind1]
        self._z[0] -= k * self._b[i]

        self._basis_vars[i] = j

    def solution(self):
        return self._z[0]

    def point(self):
        p = [0] * (len(self._z) - 1)
        for (i, basis_var) in enumerate(self._basis_vars):
            p[basis_var] = self._b[i]
        return p
