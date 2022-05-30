import pandas as pd
import ttg
import logicmin

def get_matrix(n: int, k: int):
    matrix = [[0 for i in range(n)] for row in range(n)]
    for i in range(k):
        frm = int(input("Input from:"))
        to = int(input("Input to:"))
        matrix[frm - 1][to - 1] = 1
    return matrix

def matrix_to_knf(matrix: list, n: int):
    for i in range(n):
        matrix[i][i] = 1
    knf = []
    n = len(matrix)
    for i in range(n):
        tmp = []
        tmp.append(i)
        for j in range(n):
            if matrix[i][j] == 1:
                tmp.append(j)
        knf.append(tmp)
    return knf

def knf_to_str(knf: list):
    res = ''
    for i in range(len(knf)):
        tmp = ''
        for j in range(len(knf[i])):
            tmp += chr(97 + knf[i][j])
            if j != len(knf[i]) - 1:
                tmp += ' or '
        if i != len(knf) - 1:
            tmp = '(' + tmp + ') and '
        else:
            tmp = '(' + tmp + ')'
        res += tmp
    l = [res]
    return l

def get_names(n):
    ans = []
    for i in range(n):
        ans.append(chr(97 + i))
    return ans

def get_table(names: list, expression: list):
    table = ttg.Truths(names, expression).as_pandas()
    return table

def covert_table_to_logicmin(table: pd.DataFrame):
    names = table.columns[1:-1]
    f = table.columns[-1]
    print(str(table[table.columns[0]]))
    table['mark'] = table[table.columns[0]].map(str)
    for name in names:
        print(str(table[name]))
        table['mark'] += table[name].map(str)
    table[f] = table[f].map(str)
    return table[['mark', f]]

def get_min_dnf(table: pd.DataFrame, n: int):
    t = logicmin.TT(n, 1)
    f = table.columns[1]
    for index, row in table.iterrows():
        t.add(row['mark'], row[f])
    solve = t.solve()
    return solve

def main(matrix, n):
    knf = matrix_to_knf(matrix, n)
    print(knf)
    str_knf = knf_to_str(knf)
    print(str_knf)
    names = get_names(n)
    print(names)
    table = get_table(names, str_knf)
    print(table)
    marked = covert_table_to_logicmin(table)
    print(marked)
    solve = get_min_dnf(marked, n).printN(xnames=names)
    print(solve)
    return solve

if __name__ == '__main__':
    main()