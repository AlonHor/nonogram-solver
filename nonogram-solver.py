# -*- coding: utf-8 -*-

import numpy as np
from itertools import product
from datetime import datetime

row_constraints = ([7,2], [5,1], [3], [15], [2], [15], [1], [1], [13], [3,1,1,1], [1,3,1,3], [1,3,3], [1,1,1], [1,1,1],\
               [1,6], [1,8,1], [1,2,2,1], [2,2,2], [4,3], [14])
column_constraints = ([8], [6,1,1], [4,1,2,4,2], [2,1,1,3,5], [2,1,1,1,1,3], [1,1,1,1,2,2,2], [1,1,1,1,3,3,1], \
                   [1,1,3,3,1], [1,1,1,2,1,1], [1,1,1,2,1,1], [1,1,3,3,1], [1,1,1,2,3,1], [1,1,1,2,2,2], [1,1,1,1,2,3], [2,1,1,3,5])



def is_valid_solution(new_solution, list_of_cols_to_check, list_of_rows_to_check, col_or_row):

    if col_or_row == 'row':
        for col in list_of_cols_to_check:
            arr = new_solution[:, col]
            if get_list_of_strip_sizes(arr, 20) != column_constraints[col]:
                return False
    else:
        for row in list_of_rows_to_check:
            arr = new_solution[row, :]
            if get_list_of_strip_sizes(arr, 15) != row_constraints[row]:
                return False

    return True


def get_list_of_strip_sizes(arr, length):
    list_of_strips = []
    i = 0
    while i < length:
        while i < length and arr[i] == 0:
            i += 1

        if i == length:
            return list_of_strips

        strip_length = 0
        while i < length and arr[i] == 1:
            i += 1
            strip_length += 1

        list_of_strips.append(strip_length)

        if i == length:
            return list_of_strips


def is_legal_product_setting(potentially_legal_line, constraints):
    for index in range(1, len(potentially_legal_line)):
        if(potentially_legal_line[index] <= potentially_legal_line[index-1] + constraints[index-1]):
            return False
    return True



def create_lines_with_constraints(length=15, constraints=[]):
    list_of_ranges = []
    min_value = 0
    max_value = length - sum(constraints) - len(constraints) + 1
    for constraint in constraints:
        list_of_ranges.append(range(min_value, max_value + 1))
        min_value += constraint + 1
        max_value += constraint + 1

    list_of_legal_lines = []
    for potentially_legal_line in product(*list_of_ranges):

        # skip illegal products
        if is_legal_product_setting(potentially_legal_line, constraints) == False:
            continue

        # get blanks
        line = np.zeros(length)
        for index, start_position in enumerate(potentially_legal_line):
            for cell in range(start_position, start_position + constraints[index]):
                line[cell] = 1

        list_of_legal_lines.append(line)

    return list_of_legal_lines


def add_new_line(col_or_row, index, line_length, constraint, list_of_cols_to_check, list_of_rows_to_check, list_of_potential_solutions):
    new_list_of_valid_solutions = []

    potential_new_lines = create_lines_with_constraints(length=line_length, constraints=constraint)

    for solution in list_of_potential_solutions:
        
        for potential_new_line in potential_new_lines:

            if col_or_row == 'col':
                before = np.reshape(solution[:, 0:index], (20, index))
                inject = np.reshape(potential_new_line, (20, 1))
                after_dim = 15 - index - 1
                after = np.reshape(solution[:, index + 1:], (20, after_dim))
                new_solution = np.concatenate([before, inject, after], axis=1)
            else:
                before = np.reshape(solution[0:index, :], (index, 15))
                inject = np.reshape(potential_new_line, (1, 15))
                after_dim = 20 - index - 1
                after = np.reshape(solution[index + 1:, :], (after_dim, 15))
                new_solution = np.concatenate([before, inject, after], axis=0)

            if is_valid_solution(new_solution, list_of_cols_to_check, list_of_rows_to_check, col_or_row):
                new_list_of_valid_solutions.append(new_solution)

    return new_list_of_valid_solutions

def main():
    # initial solution a solution is a matrix

    list_of_potential_solutions = [np.zeros((20, 15), dtype=int)]

    list_of_cols_to_check = []
    list_of_rows_to_check = []
    list_of_lines_to_check = [('row', 3), ('col', 0), ('row', 5), ('col', 1), 
                              ('row', 8), ('col', 2), ('row', 19), ('col', 3), 
                              ('row', 15), ('col', 10), ('row', 0), ('col', 14), 
                              ('row', 10), ('col', 6), ('row', 4), ('col', 5), 
                              ('row', 1), ('col', 13), ('row', 9), ('col', 4), 
                              ('row', 7), ('col', 7), ('row', 11), ('col', 12), 
                              ('row', 18), ('col', 11), ('row', 2), ('col', 8), 
                              ('row', 17), ('col', 9), 
                              ('row', 16), ('row', 13), ('row', 12), ('row', 14), ('row', 6)]
    for cell in list_of_lines_to_check:

        if (cell[0]=='col'):
            col_index = cell[1]
            list_of_cols_to_check.append(col_index)
            list_of_potential_solutions = add_new_line('col', col_index, 20, column_constraints[col_index], list_of_cols_to_check, list_of_rows_to_check, list_of_potential_solutions)
        else:
            row_index = cell[1]
            list_of_rows_to_check.append(row_index)
            list_of_potential_solutions = add_new_line('row', row_index, 15, row_constraints[row_index], list_of_cols_to_check, list_of_rows_to_check, list_of_potential_solutions)

        print([cell, len(list_of_potential_solutions), datetime.now().hour, datetime.now().minute, datetime.now().second])

    print(list_of_potential_solutions)



if __name__ == "__main__":
    main()
