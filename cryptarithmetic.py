#!/usr/bin/env python3

from ortools.sat.python import cp_model


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print("{} = {}".format(v, self.Value(v)))
        print()

    def solution_count(self):
        return self.__solution_count


'''
cryptarithmetic puzzle - find solutions for equation
      CP
+     IS
+    FUN
--------
=   TRUE

where every letter represents a distinct integer
'''

model = cp_model.CpModel()

# c, i, f, t must be > 0 as they are leading digits. all other characters can be any base 10 integer
c = model.NewIntVar(1, 9, 'C')
p = model.NewIntVar(0, 9, 'P')
i = model.NewIntVar(1, 9, 'I')
s = model.NewIntVar(0, 9, 'S')
f = model.NewIntVar(1, 9, 'F')
u = model.NewIntVar(0, 9, 'U')
n = model.NewIntVar(0, 9, 'N')
t = model.NewIntVar(1, 9, 'T')
r = model.NewIntVar(0, 9, 'R')
e = model.NewIntVar(0, 9, 'E')

# each letter must have a different value
letters = [c, p, i, s, f, u, n, t, r, e]
model.AddAllDifferent(letters)
model.Add(((c * 10) + p) +
          ((i * 10) + s) +
          ((f * 100) + (u * 10) + n) ==
          ((t * 1000) + (r * 100) + (u * 10) + e))

solver = cp_model.CpSolver()
printer = SolutionPrinter(letters)
solver.parameters.enumerate_all_solutions = True
status = solver.Solve(model, printer)

print("status: {}, time: {} ms".format(solver.StatusName(status), solver.WallTime()))
