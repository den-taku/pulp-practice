from time import time
import pulp

CPLEX_PATH="/Applications/CPLEX_Studio221/cplex/bin/x86-64_osx/cplex"
CPLEX_MSG = False
CPLEX_TIMELIM = 100

problem = pulp.LpProblem("example01", pulp.LpMaximize)

x1 = pulp.LpVariable("x1", lowBound=0, cat=pulp.LpContinuous)
x2 = pulp.LpVariable("x2", lowBound=0, cat=pulp.LpContinuous)
x3 = pulp.LpVariable("x3", lowBound=0, cat=pulp.LpContinuous)

problem.setObjective(3*x1 + 4*x2 + 2*x3)

problem += 2*x1 <= 4
problem += x1 + 2*x3 <= 8
problem += 3*x2 + x3 <= 6

print(problem)

CPLEX = pulp.CPLEX(path=CPLEX_PATH, msg=CPLEX_MSG, timeLimit=CPLEX_TIMELIM)

problem.solve(CPLEX)

print(pulp.value(problem.objective))
print(pulp.value(x1))
print(pulp.value(x2))
print(pulp.value(x3))