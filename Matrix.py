from abc import ABC, abstractmethod
import copy

class Matrix(ABC):

    def __init__(self, matrix):
        '''
        This initialises the matrix class. This class is the inherited from by the classes for the 2 by 2
        matrix and any size matrix class
        :param matrix: list
            A matrix in 2d list format
        '''
        self.matrix = matrix

    @abstractmethod
    def inverse(self):
        '''
        This will return the inverse of the matrix.
        This is an abstract method which must be implemented by subclasses.
        Different ways of implementation can be more efficient for matrices of different sizes.
        For smaller matrices a smaller method can be used, although larger matrices will require
        a more complex solution.
        :return: list
            A matrix that is the inverse of the matrix in the class in 2d List format
        '''
        pass

    def transpose(self):
        '''
        This method will return the transpose of the matrix in the matrix class
        :return matrix: list
            A 2d list which is the transpose of the matrix stored by the class
        '''
        matrix = []
        vertical = len(self.matrix)
        horizontal = len(self.matrix[0])

        #The following two loops create a matrix with the same number of rows as the original matrix had columns
        # and the same number of columns as the original matrix had rows
        for i in range(horizontal):
            addMatrix = []
            for j in range(vertical):
                addMatrix.append(0)
            matrix.append(addMatrix)

        # These two loops take each element from the original matrix and then put them into the new matrix but with their indices swapped
        for n in range(horizontal):
            for m in range(vertical):
                matrix[n][m] = self.matrix[m][n]

        return(matrix)

class Matrix2d(Matrix):

    def __init__(self, matrix):
        '''
        This initialises the matrix class for 2 by 2 matrices
        :param matrix: list
            A matrix in 2d list format
        '''
        super().__init__(matrix)


    def inverse(self):
        '''
        This returns the inverse of the matrix by multiplying the reciprocal and 1/determinant of the matrix
        :return: list
             A matrix which is the inverse of the matrix stored by the class in 2d List format
        '''
        multiplyConstant = 1/((self.matrix[0][0] * self.matrix[1][1]) - (self.matrix[0][1] * self.matrix[1][0]))  # This is 1/determinant of the matrix
        matrixToMultiply = [[self.matrix[1][1], -(self.matrix[0][1])], [-(self.matrix[1][0]), self.matrix[0][0]]]  # This is the reciprocal of the matrix
        return(matrixMultiply2(matrixToMultiply, multiplyConstant))  # The reciprocal and 1/determinant of multiplied and returned


class MatrixAny(Matrix):
    def __init__(self, matrix):
        '''
        This initialises the matrix class for matrices of any dimensions
        :param matrix: list
            A matrix in 2d list format
                '''
        super().__init__(matrix)

    def inverse(self):
        '''
        This returns the inverse of the matrix stored in the matrix using gauss jordan matrix inversion method
        :return inverseMatrix: list
            A matrix which is the inverse of the matrix stored by that class in 2d List format
        '''
        matrix = copy.deepcopy(self.matrix)
        length = len(matrix)

        # This creates an identity matrix in the same size as the matrix passed in
        identityMatrix = []
        for p in range(0, length):
            addMatrix = []
            for z in range(0, length):
                if p == z:
                    addMatrix.append(1)
                else:
                    addMatrix.append(0)
            identityMatrix.append(addMatrix)

        # This adds the identity matrix onto the matrix used so the algorithm can be used
        for i in range(length):
            matrix[i] += identityMatrix[i]

        # This ensures the pivot point is not 0
        for i in range(length):
            pivot = matrix[i][i]
            if pivot == 0:
                found = False
                for p in range(i + 1,
                               length):  # Below the pivot rows are checked for that include a point in the same column that is not zero.
                    # Once this is found the rows are swapped therefore the pivot will not be zero.
                    if matrix[p][i] != 0 and found == False:
                        matrixSave = copy.deepcopy(matrix[i])
                        matrix[i] = matrix[p]  # The two rows are swapped
                        matrix[p] = matrixSave
                        found = True

        # Making the pivot 1
        for i in range(length):
            pivot = matrix[i][i]
            for k in range(2 * length):  # This scales each row so that the pivot point is 1
                matrix[i][k] = matrix[i][k] / pivot

        # Making elements below the pivot 0
        for i in range(0, length - 1):  # This is the "horizontal" index of the matrix
            count = 1
            for j in range(0 + count, length):  # This is the "vertical" index of the matrix
                multiple = matrix[j][i]  # To make that point zero we must find out the value the pivot of the correct
                # column must be multiplied by to match that value
                for k in range(
                        2 * length):  # We then remove the row with the pivot in the correct column multiplied by the constant from that
                    # row, therefore making the intended point equal to 0
                    matrix[j][k] = matrix[j][k] - multiple * matrix[i][k]
            count += 1

        # Making elements above the pivot 0
        for i in range(1, length):  # This is the "horizontal" index of the matrix
            count = 1
            for j in range(0, count):  # This is the "vertical" index of the matrix
                multiple = matrix[j][i]  # To make the intended point zero we must just remove the pivot row multiplied by the value of that point.
                # This is because the pivot is one therefore this will make the intended point zero
                for k in range(
                        2 * length):  # We then remove the row with the pivot in the correct multiplied by the point we are eliminating from
                    # that row, making the intended point 0
                    matrix[j][k] = matrix[j][k] - multiple * matrix[i][k]
            count += 1

        # Getting the inverse Matrix from the created matrix
        # The inverse will be in the position that the identity matrix was put in.
        inverseMatrix = []
        # The below loops iterate through the matrix where the identity matrix was put in.
        # These elements are extracted and put into a new matrix in the same order. This will be the inverse.
        for z in range(length):
            addMatrix = []
            for r in range(length):
                addMatrix.append(matrix[z][r + length])
            inverseMatrix.append(addMatrix)
        return (inverseMatrix)

def matrixMultiply(matrix1, matrix2):
    '''
    This returns the matrix that comes when two matrices are multiplied
    :param matrix1: list
        One of the matrices to be multiplied in 2d list format
    :param matrix2: list
        One of the matrices to be multiplied in 2d list format
    :return finalMatrix: list
        The resulting matrix when two matrices are multiplied in 2d list format
    '''
    finalMatrix = []
    # The two loops below create a matrix of the size that multiplying the two inputted matrices would result in
    for i in range(0, len(matrix1)):
        addMatrix = []
        for n in range(0, len(matrix2[0])):
            addMatrix.append(0)
        finalMatrix.append(addMatrix)
    # The three below loops iterate through the two inputted matrices, multiplying the correct elements by each other and
    # summing the multiplications when needed. This results in the value of multiplying the two matrices
    for x in range(0, len(matrix1)):
        for y in range(0, len(matrix2[0])):
            for z in range(0, len(matrix2)):
                finalMatrix[x][y] += matrix1[x][z] * matrix2[z][y]
    return(finalMatrix)

def matrixMultiply2(matrix, num):
    '''
    This multiplies a matrix by a constant and returns the result
    :param matrix: list
        The matrix to be multiplied
    :param num: float
        The number to multiply the matrix by
    :return matrix: list
        The resulting matrix of multiplying the number and the matrix
    '''
    # The two for loops below iterate through each element in the matrix, multiplying each one by a constant
    for i in range(0, len(matrix)):
        for x in range(0,len(matrix[i])):
            matrix[i][x] = matrix[i][x] * num
    return(matrix)

def LinearRegression2d(yMatrix, xMatrix):
    '''
    This is the algorithm to calculate the coefficients between x and y when provided with two
    matrices with their values stored. This is the algorithm when it is only one factor compared to price
    :param yMatrix: list
        The matrix full of price values in 2d list format
    :param xMatrix: list
        The matrix full of the other factors values e.g. date at those price values in 2d list format
    :return coefficients: list
        The coefficients relating x to y in matrix in 2d list format
    '''
    for i in range(0, len(xMatrix.matrix)):
        xMatrix.matrix[i].insert(0, 1)
    XT = xMatrix.transpose()
    matrixToInverse = matrixMultiply(XT, xMatrix.matrix)
    inverseMatrix = Matrix2d(matrixToInverse)
    inverseMatrix = inverseMatrix.inverse()
    multiplyMatrix = matrixMultiply(inverseMatrix, XT)
    coefficients = matrixMultiply(multiplyMatrix, yMatrix.matrix)
    return(coefficients)


def LinearRegressionAny(yMatrix, xMatrix):
    '''
        This is the algorithm to calculate the coefficients between x and y when provided with two matrices
        with their values stored. This is the algorithm when all five factors are compared to price
        :param yMatrix: list
            The matrix full of price values in 2d list format
        :param xMatrix: list
            The matrix full of the other factors values e.g. date at those price values in 2d list format
        :return coefficients: list
            The coefficients relating x to y in matrix in 2d list format
        '''
    for i in range(0, len(xMatrix.matrix)):
        xMatrix.matrix[i].insert(0, 1)
    XT = xMatrix.transpose()
    matrixToInverse = matrixMultiply(XT, xMatrix.matrix)
    inverseMatrix = MatrixAny(matrixToInverse)
    inverseMatrix = inverseMatrix.inverse()
    multiplyMatrix = matrixMultiply(inverseMatrix, XT)
    coefficients = matrixMultiply(multiplyMatrix, yMatrix.matrix)
    return(coefficients)
