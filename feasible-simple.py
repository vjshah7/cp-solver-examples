#!/usr/bin/env python3

from ortools.sat.python import cp_model

model = cp_model.CpModel()

num_vals = 3
x = model.NewIntVar(0, num_vals - 1, 'x')
y = model.NewIntVar(0, num_vals - 1, 'y')
z = model.NewIntVar(0, num_vals - 1, 'z')

model.Add(x != y)

solver = cp_model.CpSolver()
status = solver.Solve(model)

print("status: {}, x={}, y={}, z={}".format(status, solver.Value(x), solver.Value(y), solver.Value(z)))
