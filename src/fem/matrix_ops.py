class AdditionError(Exception):
    pass


class MultiplicationError(Exception):
    pass


class Matrix(list):
    def dim(self):
        return len(self), len(self[0])


# TODO Cholesky, reversing, determinant

class MatrixOperations(object):
    def add(self, m_1, m_2):
        return self._add_or_subtract(m_1, m_2, sign=1, function=self.add)

    def subtract(self, m_1, m_2):
        return self._add_or_subtract(m_1, m_2, sign=-1, function=self.subtract)

    def transpose(self, matrix):
        t_1 = type(matrix)
        if t_1 == list:
            return Matrix([[i] for i in matrix])
        elif t_1 == Matrix:
            if len(matrix[0]) == 1:
                return [matrix[i][0] for i in range(len(matrix))]
            else:
                return Matrix([[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))])

    def multiply(self, m_1, m_2):
        """Performs multiplication of different types.
        :param m_1 can be numeric, list (vector) or matrix,
        :param m_2 can be list (vector) or matrix
        """
        t_1 = type(m_1)
        if t_1 in [int, float]:
            return self._scalar_multiplication(m_1, m_2)
        elif t_1 == list:
            return self._vector_multiplication(m_1, m_2)
        elif t_1 == Matrix:
            return self._matrix_multiplication(m_1, m_2)
        else:
            raise TypeError

    def cholesky_ldl(self, matrix):
        l_down = []
        diag = []
        dim = len(matrix)
        for i in range(dim):
            l_down.append([])
            diag.append([0]*i)
            for j in range(i):
                l_down[i].append(
                    (matrix[i][j] - sum([l_down[i][k] * l_down[j][k] * diag[k][k] for k in range(j)])) / diag[j][j]
                )
            l_down[i].append(1)
            diag[i].append(matrix[i][i] - sum((diag[k][k] * l_down[i][k] ** 2) for k in range(i)))
            for j in range(i, dim-1):
                l_down[i].append(0)
                diag[i].append(0)
        return {'l_down': Matrix(l_down), 'diag': Matrix(diag)}

    def reverse(self, matrix):
        pass

    @staticmethod
    def _check_if_matrix_is_square(matrix):
        return len(matrix) == len(matrix[0])

    @staticmethod
    def _scalar_multiplication(c, matrix):
        if type(matrix) == Matrix:
            return [[c * j for j in i] for i in matrix]
        elif type(matrix) == list:
            return [c * j for j in matrix]

    def _vector_multiplication(self, vector, m):
        self._check_vector_multiplication(vector, m)
        m_t = self.transpose(m)
        if type(m_t) == list:
            return sum([i * j for i, j in zip(vector, m_t)])
        else:
            return [sum([j * k for j, k in zip(vector, i)]) for i in m_t]

    def _matrix_multiplication(self, m_1, m_2):
        self._check_matrix_multiplication(m_1, m_2)
        m_2_t = self.transpose(m_2)
        return Matrix([[self._vector_multiplication(i, self.transpose(j)) for j in m_2_t] for i in m_1])

    @staticmethod
    def _check_vector_multiplication(vector, m):
        if len(vector) != len(m):
            raise MultiplicationError

    @staticmethod
    def _check_matrix_multiplication(m_1, m_2):
        if len(m_1[0]) != len(m_2):
            raise MultiplicationError

    def _add_or_subtract(self, m_1, m_2, sign, function):
        if self._check_add_matching(m_1, m_2, Matrix):
            return Matrix([function(m_1[i], m_2[i]) for i, _ in enumerate(m_1)])
        elif self._check_add_matching(m_1, m_2, list):
            return [i + j*sign for i, j in zip(m_1, m_2)]
        else:
            raise TypeError("You can add only matrices or vectors!")

    @staticmethod
    def _check_add_matching(m_1, m_2, control_type):
        if type(m_1) == type(m_2) == control_type:
            if len(m_1) == len(m_2):
                return True
            else:
                raise AdditionError("Matrices don't have the same dimensions!")
        # else: return False ! Not necessary
