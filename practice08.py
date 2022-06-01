import pulp

CPLEX_PATH="/Applications/CPLEX_Studio221/cplex/bin/x86-64_osx/cplex"
CPLEX_MSG = False
CPLEX_TIMELIM = 100
CPLEX = pulp.CPLEX(path=CPLEX_PATH, msg=CPLEX_MSG, timeLimit=CPLEX_TIMELIM)

row = 4
column = 4
values = 4

preassigned = [(0, 0, 0), (0, 3, 3), (2, 2, 1), (3, 1, 2)]

problem = pulp.LpProblem("example01", pulp.LpMaximize)

# x[i][j][k] = 1 => i行j列に値kを割り当てる
x = [[[pulp.LpVariable('x({},{}, {})'.format(i, j, k), cat=pulp.LpBinary) for k in range(values)] for j in range(column)] for i in range(row)]

problem.setObjective(pulp.lpSum(x[i][j][k] for i in range(row) for j in range(column) for k in range(values)))

# 初期条件
for (i, j, k) in preassigned:
    problem += x[i][j][k] == 1
    for l in range(values):
        if l == k:
            continue
        else:
            problem += x[i][j][l] == 0

# 各行は重複しない
for i in range(row):
    for k in range(values):
        problem += pulp.lpSum(x[i][j][k] for j in range(column)) <= 1

# 各列は重複しない
for j in range(column):
    for k in range(values):
        problem += pulp.lpSum(x[i][j][k] for i in range(row)) <= 1

# 各箱は重複しない
# ad hoc code
for a in range(2):
    for b in range(2):
        for k in range(values):
            problem += x[0 + a * 2][0 + b * 2][k] + x[0 + a * 2][1 + b * 2][k] + x[1 + a * 2][0 + b * 2][k] + x[1 + a * 2][1 + b * 2][k] <= 1

print(problem)

problem.solve(CPLEX)

if pulp.value(problem.objective) == row * column:
    print("Solution found")
    for i in range(row):
        for j in range(column):
            for k in range(values):
                if pulp.value(x[i][j][k]):
                    print(k + 1, end=' ')
        print()
