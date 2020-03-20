# JetBrains Academy/Python Developer
# Project: Numeric Matrix Processor
# Stage 1/6: Addition
# Stage 2/6: Multiplication by number
# Stage 3/6: Matrix by matrix multiplication
# Stage 4/6: Transpose
# Stage 5/6: Determined!
# Stage 6/6: Inverse matrix



class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.__n = len(self.matrix)
        self.__m = len(self.matrix[0])

    def __str__(self):
        """Overriding __str__.
        Returns a string of the format we need"""
        if any([any([bool(abs(item) % 1) for item in row]) for row in self.matrix]):
            #  float matrix
            return '\n'.join(' '.join(str(round(cell, 2)) for cell in row) for row in self.matrix)
        else:
            #  int matrix
            return '\n'.join(' '.join(str(cell)[:-2] for cell in row) for row in self.matrix)

    def __add__(self, other):
        """Overriding __add__.
        Returns the result of adding two matrices as new instance of class Matrix."""
        return Matrix([[self.matrix[n][m] + other.matrix[n][m] for m in range(self.__m)] for n in range(self.__n)])

    def __mul__(self, other):
        """Overriding __mul__.
        Returns the result of multiply by matrix or scalar as new instance of class Matrix."""
        # matrix multiplication (a surprise for those who copied my code from Stage 2/6 =))
        if type(other) == Matrix:
            m1 = self.matrix
            m2 = [[other.matrix[j][i] for j in range(len(other.matrix))]  # transpose matrix
                  for i in range(len(other.matrix[0]))]
            m3 = []
            for n in range(len(m1)):  # the result will have the same number of rows as the 1st matrix
                m3.append([])
                for m in range(len(m2)):  # and the same number of columns as the 2nd matrix
                    m3[n].append(sum([m1_item * m2_item for m1_item, m2_item in zip(m1[n], m2[m])]))
            return Matrix(m3)
        # multiply by a scalar
        else:
            return Matrix([[self.matrix[n][m] * other for m in range(self.__m)] for n in range(self.__n)])

    def transpose(self, method='main'):
        """Transposes itself into a matrix according to the requested transpose method.
        Takes a parameter "method" like 'main', 'side', 'vertical' and 'horizontal'.
        'main' - transposition along the main diagonal
        'side' - transposition along the side diagonal
        'vertical' - transposition along the vertical line
        'horizontal' - transposition along the horizontal line
        Returns matrix as new instance of class Matrix."""
        if method == 'side':
            return Matrix([[self.matrix[n][m] for n in reversed(range(len(self.matrix)))]
                           for m in reversed(range(len(self.matrix[0])))])
        elif method == 'vertical':
            return Matrix([[self.matrix[m][n] for n in reversed(range(len(self.matrix)))]
                           for m in range(len(self.matrix[0]))])
        elif method == 'horizontal':
            return Matrix([[self.matrix[m][n] for n in range(len(self.matrix))]
                           for m in reversed(range(len(self.matrix[0])))])
        else:  # main default method
            return Matrix([[self.matrix[n][m] for n in range(len(self.matrix))]
                           for m in range(len(self.matrix[0]))])

    def determinant(self, _matrix=None):
        """Returns the determinant of the passed matrix.
        If the matrix has not been passed to the function, it returns the determinant of the matrix of the instance."""
        if _matrix is None:
            _matrix = self.matrix
        if len(_matrix) == 1:
            return _matrix[0][0]
        if len(_matrix) == 2:  # for 2x2 matrix
            return _matrix[0][0] * _matrix[1][1] - _matrix[0][1] * _matrix[1][0]
        determinant = 0
        for c in range(len(_matrix)):
            determinant += ((-1) ** c) * _matrix[0][c] * \
                           self.determinant([row[:c] + row[c + 1:] for row in (_matrix[:0] + _matrix[1:])])
        return determinant

    def inverse(self):
        """Returns the inverse of the instance matrix as new instance of class Matrix."""
        determinant = self.determinant()
        if determinant == 0:
            return "This matrix doesn't have an inverse."
        # for 2x2 matrix
        if len(self.matrix) == 2:
            return [[self.matrix[1][1] / determinant, -1 * self.matrix[0][1] / determinant],
                    [-1 * self.matrix[1][0] / determinant, self.matrix[0][0] / determinant]]
        # find matrix of cofactors
        cofactors = []
        for row in range(len(self.matrix)):
            cofactor_row = []
            for col in range(len(self.matrix)):
                minor = [row[:col] + row[col + 1:] for row in (self.matrix[:row] + self.matrix[row + 1:])]  # get minor
                cofactor_row.append(((-1) ** (row + col)) * self.determinant(minor))
            cofactors.append(cofactor_row)
        cofactors = list(map(list, zip(*cofactors)))  # transpose matrix
        for row in range(len(cofactors)):
            for col in range(len(cofactors)):
                cofactors[row][col] = cofactors[row][col] / determinant
        return Matrix(cofactors)


class Menu:
    def __init__(self):
        self.__print_main_menu()
        self.choice = input('Your choice: ').strip()
        if self.choice == '4':  # transpose matrix
            self.__print_transpose_menu()
            self.choice += ('.' + input('Your choice: '))  # create a subparagraph (as 4.1, 4.2, etc.)

    @staticmethod
    def __print_main_menu():
        print('1. Add matrices')
        print('2. Multiply matrix by a constant')
        print('3. Multiply matrices')
        print('4. Transpose matrix')
        print('5. Calculate a determinant')
        print('6. Inverse matrix')
        print('0. Exit')

    @staticmethod
    def __print_transpose_menu():
        print('1. Main diagonal')
        print('2. Side diagonal')
        print('3. Vertical line')
        print('4. Horizontal line')


class Processor:
    def __init__(self):
        self.__created_matrices = 0
        self._result = None
        self.run()

    def __matrix_from_input(self):
        """Creates a matrix from user input."""
        ordinal = 'first' if self.__created_matrices == 0 else 'second'
        __n, __m = map(int, input(f'Enter size of {ordinal} matrix: ').split())
        self.__created_matrices += 1
        print(f'Enter {ordinal} matrix:')
        return [list(map(float, input().split())) for i in range(__n)]

    def __check_matrices(self, m1, m2, func):
        """Checks if the matrices obtained are suitable for performing certain mathematical operations on them.
        "m1" is the first Matrix, "m2" is the second Matrix, "func" is the type of mathematical operation (add, mul).
        Returns True if the matrices meet the requirements of a specific operation, otherwise False.."""
        if func == 'add':
            # matrices should be equal in the number of rows and columns
            return True if len(m1.matrix) == len(m2.matrix) and len(m1.matrix[0]) == len(m2.matrix[0]) else False
        elif func == 'mul':
            # the number of columns of the 1st matrix must equal the number of rows of the 2nd matrix.
            return True if len(m1.matrix[0]) == len(m2.matrix) else False

    def run(self):
        while True:
            menu = Menu()
            # add matrices
            if menu.choice == '1':
                m1 = Matrix(self.__matrix_from_input())
                m2 = Matrix(self.__matrix_from_input())
                if self.__check_matrices(m1, m2, 'add'):
                    self._result = m1 + m2
                else:
                    print('The operation cannot be performed. Try again.')
                    continue
            # multiply matrix by a constant
            elif menu.choice == '2':
                m1 = Matrix(self.__matrix_from_input())
                m2 = float(input('Enter constant: '))
                self._result = m1 * m2
            # multiply matrices
            elif menu.choice == '3':
                m1 = Matrix(self.__matrix_from_input())
                m2 = Matrix(self.__matrix_from_input())
                if self.__check_matrices(m1, m2, 'mul'):
                    self._result = m1 * m2
                else:
                    print('The operation cannot be performed. Try again.')
                    continue
            # transpose matrix
            elif menu.choice.startswith('4.'):
                if menu.choice == '4.1':  # main diagonal
                    m = Matrix(self.__matrix_from_input())
                    self._result = m.transpose('main')
                elif menu.choice == '4.2':  # side diagonal
                    m = Matrix(self.__matrix_from_input())
                    self._result = m.transpose('side')
                elif menu.choice == '4.3':  # vertical line
                    m = Matrix(self.__matrix_from_input())
                    self._result = m.transpose('vertical')
                elif menu.choice == '4.4':  # horizontal line
                    m = Matrix(self.__matrix_from_input())
                    self._result = m.transpose('horizontal')
            # calculate a determinant
            elif menu.choice == '5':
                m = Matrix(self.__matrix_from_input())
                result = m.determinant()
                self._result = ''.join(str('%.0f' % result) if str(result).endswith('.0')
                                       else str(int(result * 100) / 100))
            # inverse matrix
            elif menu.choice == '6':
                m = Matrix(self.__matrix_from_input())
                self._result = m.inverse()
            # exit
            elif menu.choice == '0':
                break
            else:
                print('Error selecting menu item. Try again.')
                continue
            # print result
            print('The result is:')
            print(self._result)


if __name__ == '__main__':
    processor = Processor()
