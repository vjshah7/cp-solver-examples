#!/usr/bin/env python3

from ortools.sat.python import cp_model


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        for ind in range(len(self.__variables)):
            print("Queen {}: {},{}".format(ind, self.Value(self.__variables[ind]), ind))

        print()

    def solution_count(self):
        return self.__solution_count


'''
How can N queens be placed on an NxN chessboard so that no two of them attack each other?

Find all possible solutions
'''

model = cp_model.CpModel()
board_size = 8

# model/constraints:
# a piece's place on a chessboard can be specified by a row (x) coordinate and a column (y) coordinate.
# in order to simplify the model, the number of each queen identifies its column, as we know each queen must
# be in different columns. the value for each queen will repesent the row.
# coordinates must always be between 1 and <board_size> inclusive

queens = list()
for ii in range(1, board_size + 1):
    queens.append(model.NewIntVar(1, board_size, "Q{}-X".format(ii)))

model.AddAllDifferent(queens)

# no two queens can be on the same diagonal... trickier constraint
# observation - if 2 queens are in the same '\' line, then their x&y coordinates are different by the same constant.
# e.g. (3,2) and (5,4) are in the same '\' diagonal... 5-3=2 and 4-2=2. we can capture this constraint by saying that
# no two queen coordinate pairs can have the same (y-x) value.
# if two queens are in the same '/' line, then as you traverse up and to the right along the diagonal, the x coordinate
# gets incremented by one and the y coordinate gets decremented by one, therefore, the sum of the x & y coordinates
# stay constant along the diagonal. the sum of x&y coordinates is also distinct on every diagonal.
diag_ul_lr = list()
diag_ll_ur = list()
for ii in range(board_size):
    derived_value_1 = model.NewIntVar(-board_size, board_size, "diag_ul_lr_{}".format(ii))
    model.Add(derived_value_1 == queens[ii] - ii)
    diag_ul_lr.append(derived_value_1)
    derived_value_2 = model.NewIntVar(0, 2 * board_size, "diag_ll_ur_{}".format(ii))
    model.Add(derived_value_2 == queens[ii] + ii)
    diag_ll_ur.append(derived_value_2)

model.AddAllDifferent(diag_ul_lr)
model.AddAllDifferent(diag_ll_ur)

# model.AddAllDifferent(queens[ii] + ii for ii in range(board_size))
# model.AddAllDifferent(queens[ii] - ii for ii in range(board_size))

solver = cp_model.CpSolver()
printer = SolutionPrinter(queens)
solver.parameters.enumerate_all_solutions = True
status = solver.Solve(model, printer)

print("status: {}, num solutions: {}, time: {} ms"
      .format(solver.StatusName(status), printer.solution_count(), solver.WallTime()))
