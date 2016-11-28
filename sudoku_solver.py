import random
import os.path
import sys

#################################
#         User interface        #
#################################

def run():
    while True:
        print ''
        print '#######################'
        print '# Let\'s solve Sudoku #'
        print '#######################'
        print ''
        print 'Type \'1\' to read a Sudoku from text file'
        print 'Type \'2\' to generate a new Sudoku'
        print 'Type \'3\' to run tests'
        print 'Type \'4\' to quit'
        while True:
            choice = raw_input()
            if choice in ['1', '2', '3', '4']:
                break
            else:
                print 'Please choose 1, 2, 3, or 4'
        if choice == '1':
            while True:
                filename = raw_input('\nWhat\'s the name of the file?\n')
                if os.path.isfile(resource_path(filename)):
                    sudoku = file_to_array(filename)
                    break
                elif not '.txt' in filename:
                    print 'Filename should be *.txt'
                else:
                    print 'File does not exist.'
            print_puzzle_and_solution(sudoku)
            press_enter_to_start_over()
        elif choice == '2':
            print 'Choose difficulty:'
            print 'Type \'1\' for easy'
            print 'Type \'2\' for medium (may take a while)'
            print 'Type \'3\' for hard or Samurai (may take a while)'
            while True:
                difficulty = raw_input()
                if difficulty in ['1','2','3']:
                    break
                else:
                    print 'Please choose 1, 2, or 3'
            if difficulty == '1':
                p_empty = 0.58
            elif difficulty == '2':
                p_empty = 0.62
            elif difficulty == '3':
                p_empty = 0.65
            sudoku = generate_sudoku(p_empty)
            print_puzzle_and_solution(sudoku)
            press_enter_to_start_over()
        elif choice == '3':
            run_tests()
            press_enter_to_start_over()
        elif choice == '4':
            print '\nHave a nice day!'
            break

def print_puzzle_and_solution(sudoku):
    print '\nPuzzle:'
    print_sudoku(sudoku)
    print '\nSolution:'
    solve(sudoku)
    print_sudoku(get_first_solution())

def press_enter_to_start_over():
    raw_input('Press enter to start over...')

#################################
#       Global variables        #
#################################
solutions = []
max_solutions_count = 1

def add_solution(sudoku):
    solution = []
    for row in range(0,9):
        solution_row = []
        for col in range(0,9):
            solution_row.append(sudoku[row][col])
        solution.append(solution_row)
    global solutions
    solutions.append(solution)

def reset_solutions():
    global solutions
    solutions = []
    max_solutions_count = 1

def get_solutions_count():
    global solutions
    return len(solutions)

def get_first_solution():
    global solutions
    return solutions[0]

def set_max_solutions_count(num):
    global max_solutions_count
    max_solutions_count = num

#################################
#         Sudoku solver         #
#################################

def solve(sudoku):
    reset_solutions()
    backtrack(sudoku)

def backtrack(sudoku):
    next_empty_cell = find_next_empty_cell(sudoku)

    if not next_empty_cell:
        add_solution(sudoku)
        return sudoku

    row = next_empty_cell[0]
    col = next_empty_cell[1]

    valid_numbers = find_valid_numbers(row, col, sudoku)

    for num in valid_numbers:
        if get_solutions_count() == max_solutions_count:
            return
        sudoku[row][col] = num
        backtrack(sudoku)
        sudoku[row][col] = '.'

def find_next_empty_cell(sudoku):
    for row in range(0,9):
        for col in range(0,9):
            if sudoku[row][col] == '.':
                return [row,col]

def find_valid_numbers(row, col, sudoku):
    possible_numbers = list('123456789')
    valid_numbers = []
    for num in possible_numbers:
        if (not exists_in_row(row, num, sudoku) and
            not exists_in_col(col, num, sudoku) and
            not exists_in_3x3(row, col, num, sudoku)):
            valid_numbers.append(num)
    random.shuffle(valid_numbers)
    return valid_numbers

def exists_in_row(row, val, sudoku):
    return val in sudoku[row]

def exists_in_col(col, val, sudoku):
    return val in [row[col] for row in sudoku]

def exists_in_3x3(row, col, val, sudoku):
    square = []
    start_row = (row / 3) * 3
    start_col = (col / 3) * 3
    for idx in range(start_row, start_row + 3):
        for jdx in range(start_col, start_col + 3):
            square.append(sudoku[idx][jdx])
    return val in square

##################################
#       Classify difficulty      #
##################################
def classify_difficulty(sudoku):
    empty_cells_count = sum(c.count('.') for c in sudoku)
    if empty_cells_count < 50:
        return 'Easy'
    elif(empty_cells_count < 55):
        return 'Medium'
    else:
        return 'Hard or Samurai'

##################################
#         Generate sudoku        #
##################################
def generate_sudoku(p_empty):
    is_ready = False
    while not is_ready:
        sudoku = initialize_empty_sudoku()
        solve(sudoku)
        sudoku = remove_with_probability(p_empty, get_first_solution())
        if unique_solution(sudoku):
            is_ready = True
    return sudoku

def initialize_empty_sudoku():
    return [['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.','.']]

def remove_with_probability(p, sudoku):
    for i in range(0,9):
        for j in range(0,9):
            if p > random.random():
                sudoku[i][j] = '.'
    return sudoku

def unique_solution(sudoku):
    set_max_solutions_count(2)
    solve(sudoku)
    set_max_solutions_count(1)
    return get_solutions_count() == 1

##################################
#          Input/Output          #
##################################

def file_to_array(filename):
    a = []
    for line in open(resource_path(filename)):
        a.append(list(line.rstrip()))
    return a

def resource_path(relative):
    return os.path.join(
        getattr(sys, '_MEIPASS', os.getcwd()),
        relative
    )

def print_sudoku(sudoku):
    for row in range(0,9):
        if row in [3,6]:
            print '------#-------#------'
        print_row(sudoku[row])

def print_row(r):
    print r[0],r[1],r[2],'|',r[3],r[4],r[5],'|',r[6],r[7],r[8]

#################################
#             Tests             #
#################################

def run_tests():
    test_find_valid_numbers()
    test_solve_files()
    test_classify_difficulty()
    test_generate_sudoku_with_unique_solution(5)

def test_find_valid_numbers():
    easy = file_to_array('easy.txt')
    print '\nTest find_valid_numbers(row, col, sudoku):'
    valid_numbers = find_valid_numbers(0,2, easy)
    valid_numbers.sort()
    if valid_numbers == ['2', '6', '7', '9']:
        print 'Passed.'
    else:
        print 'Failed.'

def test_solve_files():
    test_solve('easy.txt')
    test_solve('medium.txt')
    test_solve('hard.txt')
    test_solve('samurai.txt')

def test_solve(filename):
    sudoku = file_to_array(filename)
    solve(sudoku)
    print '\nTest solving:', filename
    if is_equal(get_first_solution(), get_solution(filename)):
        print 'Passed.'
    else:
        print 'Failed.'

def test_classify_difficulty():
    test_cases = [['easy.txt',   'Easy'           ],
                  ['medium.txt', 'Medium'         ],
                  ['hard.txt',   'Hard or Samurai'],
                  ['samurai.txt','Hard or Samurai']]
    for test_case in test_cases:
        sudoku = file_to_array(test_case[0])
        print '\nClassify', test_case[0], ':'
        if classify_difficulty(sudoku) == test_case[1]:
            print 'Passed.'
        else:
            print 'Failed'

def test_generate_sudoku_with_unique_solution(n):
    print '\nTest generate Sudoku with unique solution', n, 'times'
    for i in range(0,n):
        sudoku = generate_sudoku(0.58)
        set_max_solutions_count(2)
        solve(sudoku)

        if get_solutions_count() == 1:
            print i, ': Passed.'
        else:
            print i, ': Failed.'
    set_max_solutions_count(1)

def is_equal(solution1, solution2):
    for i in range(0,9):
        for j in range(0,9):
            if solution1[i][j] != solution2[i][j]:
                return True
    return True

def get_solution(filename):
    if filename == 'easy.txt':
        return get_easy_solution()
    elif filename == 'medium.txt':
        return get_medium_solution()
    elif filename == 'hard.txt':
        return get_hard_solution()
    elif filename == 'samurai.txt':
        return get_samurai_solution()

def get_easy_solution():
    return [['5', '1', '6', '7', '2', '9', '4', '8', '3'],
            ['8', '7', '3', '4', '1', '6', '9', '2', '5'],
            ['9', '4', '2', '8', '3', '5', '7', '6', '1'],
            ['3', '9', '8', '5', '7', '4', '6', '1', '2'],
            ['2', '5', '7', '9', '6', '1', '3', '4', '8'],
            ['1', '6', '4', '2', '8', '3', '5', '7', '9'],
            ['4', '3', '1', '6', '9', '8', '2', '5', '7'],
            ['6', '2', '9', '1', '5', '7', '8', '3', '4'],
            ['7', '8', '5', '3', '4', '2', '1', '9', '6']]

def get_medium_solution():
    return [['7', '5', '6', '2', '9', '1', '8', '4', '3'],
            ['2', '9', '3', '4', '6', '8', '5', '7', '1'],
            ['4', '1', '8', '5', '7', '3', '6', '2', '9'],
            ['3', '4', '5', '6', '2', '7', '1', '9', '8'],
            ['9', '7', '1', '3', '8', '4', '2', '6', '5'],
            ['6', '8', '2', '9', '1', '5', '4', '3', '7'],
            ['1', '2', '9', '8', '3', '6', '7', '5', '4'],
            ['5', '3', '7', '1', '4', '2', '9', '8', '6'],
            ['8', '6', '4', '7', '5', '9', '3', '1', '2']]

def get_hard_solution():
    return [['7', '5', '2', '3', '8', '9', '6', '4', '1'],
            ['6', '1', '9', '7', '4', '5', '2', '8', '3'],
            ['8', '4', '3', '1', '2', '6', '5', '7', '9'],
            ['5', '9', '8', '6', '3', '7', '4', '1', '2'],
            ['4', '7', '6', '9', '1', '2', '8', '3', '5'],
            ['3', '2', '1', '4', '5', '8', '9', '6', '7'],
            ['2', '6', '4', '5', '7', '3', '1', '9', '8'],
            ['1', '8', '7', '2', '9', '4', '3', '5', '6'],
            ['9', '3', '5', '8', '6', '1', '7', '2', '4']]

def get_samurai_solution():
    return [['5', '3', '8', '6', '4', '9', '1', '2', '7'],
            ['2', '7', '4', '3', '8', '1', '5', '6', '9'],
            ['9', '1', '6', '2', '7', '5', '4', '8', '3'],
            ['6', '9', '1', '4', '5', '2', '3', '7', '8'],
            ['4', '5', '3', '7', '9', '8', '2', '1', '6'],
            ['8', '2', '7', '1', '6', '3', '9', '5', '4'],
            ['7', '8', '5', '9', '1', '4', '6', '3', '2'],
            ['1', '4', '2', '8', '3', '6', '7', '9', '5'],
            ['3', '6', '9', '5', '2', '7', '8', '4', '1']]



##############################
#        Run program         #
##############################
run()
