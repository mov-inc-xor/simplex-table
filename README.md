# Симплекс-таблица
Класс симплекс-таблицы для решения задачи линейного программирования в каноническом виде.

![Симплекс-таблица](https://i.imgur.com/e6vTptH.png)

## Использование
``` python
from simplex import SimpleSimplexTable


if __name__ == '__main__':

    # Задача в канонической форме
    # a - матрица коэффициентов
    # b - столбец свободных членов
    # z - коэффициенты целевой ф-ии, начиная с нулевого

    a = [[1, 0, 0, 1, -2],
         [0, 1, 0, -2, 1],
         [0, 0, 1, 3, 1]]

    b = [1, 2, 3]

    z = [0, 0, 0, 0, -1, 1]

    basis_vars = [4, 1, 3]

    table = SimpleSimplexTable(a, b, z, basis_vars)
    print(table)

    has_solution = True

    while not table.solved():
        i, j = table.select_resolution_element()
        if i is None or j is None:
            has_solution = False
            break
        print(f'Выводится элемент x{i + 1}, вводится x{j + 1}.')
        table.swap(i, j)
        print(table)

    if has_solution:
        print('Решение:', table.solution())
        print('Точка:', *table.point())
    else:
        print('Решений нет.')
```
