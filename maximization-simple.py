#!/usr/bin/env python3

from ortools.sat.python import cp_model

'''
Maximize 2x + 2y + 3z subject to the following constraints:
x + 7⁄2 y + 3⁄2 z	≤	25
3x - 5y + 7z	≤	45
5x + 2y - 6z	≤	37
x, y, z	≥	0
x, y, z integers
'''

model = cp_model.CpModel()

# because the first constraint is addition, and because x/y/z must all be nonnegative, x must be <= 25,
# y <= floor(2/7 * 25) = 7, z <= floor(2/3 * 25) = 16
x = model.NewIntVar(0, 25, 'x')
y = model.NewIntVar(0, 7, 'y')
z = model.NewIntVar(0, 16, 'z')

# in defining the equation based constraints, we must have all-integer coefficients, so the first equation
# transforms to 2x + 7y + 3z <= 50
model.Add((2 * x) + (7 * y) + (3 * z) <= 50)
model.Add((3 * x) - (5 * y) + (7 * z) <= 45)
model.Add((5 * x) + (2 * y) - (6 * z) <= 37)

model.Maximize((2 * x) + (2 * y) + (3 * z))

solver = cp_model.CpSolver()
status = solver.Solve(model)

print("status: {}, objective value = {}, x={}, y={}, z={}"
      .format(status, solver.ObjectiveValue(), solver.Value(x), solver.Value(y), solver.Value(z)))
