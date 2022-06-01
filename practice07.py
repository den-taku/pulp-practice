import pulp

CPLEX_PATH="/Applications/CPLEX_Studio221/cplex/bin/x86-64_osx/cplex"
CPLEX_MSG = False
CPLEX_TIMELIM = 100
CPLEX = pulp.CPLEX(path=CPLEX_PATH, msg=CPLEX_MSG, timeLimit=CPLEX_TIMELIM)

vertices = 7
edge = [(0, 1), (0, 5), (1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 6), (3, 5), (5, 6)]
# edge = [(i, j) for i in range(vertices) for j in range(vertices)]
color = 3

problem = pulp.LpProblem("example01", pulp.LpMaximize)

# x[i][c] = 1 => 頂点iに色cを割り当てる
x = [[pulp.LpVariable('x({},{})'.format(i, c), cat=pulp.LpBinary) for c in range(color)] for i in range(vertices)]

problem.setObjective(x[0][0])

# 各頂点は一つ以上色を割り当てられる
for i in range(color):
    problem += pulp.lpSum(x[i][c] for c in range(color)) >= 1

# 辺の端点は別の色
for (u, v) in edge:
    for c in range(color):
        problem += x[u][c] + x[v][c] <= 1

print(problem)

problem.solve(CPLEX)

# 実行可能解が存在する => 彩色可能
print(pulp.value(problem.objective))
