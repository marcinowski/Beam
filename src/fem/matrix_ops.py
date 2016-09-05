class AdditionError(Exception):
    pass


class MultiplicationError(Exception):
    pass


class Matrix(list):
    def dim(self):
        return len(self), len(self[0])


class MatrixOperations(object):
    def add(self, m_1, m_2):
        return self._add_or_subtract(m_1, m_2, sign=1, function=self.add)

    def subtract(self, m_1, m_2):
        return self._add_or_subtract(m_1, m_2, sign=-1, function=self.subtract)

    def transpose(self, m_1):
        t_1 = type(m_1)
        if t_1 == list:
            return Matrix([[i] for i in m_1])
        if t_1 == Matrix:
            # if len(m_1[0]) == 1:
            #     return [m_1[i][0] for i in range(len(m_1))]
            # else:
            return Matrix([[m_1[i][j] for i in range(len(m_1))] for j in range(len(m_1[0]))])

    def multiply(self, m_1, m_2):
        t_1, t_2 = type(m_1), type(m_2)
        self._check_multiply_matching(m_1, m_2, t_1, t_2)
        m_2_t = self.transpose(m_2)
        if t_1 in [int, float]:
            return self._scalar_multiplication(m_1, m_2_t)
        elif t_1 == list:
            return [sum([j*k for j, k in zip(m_1, i)]) for i in m_2_t]
        elif t_1 == Matrix:
            # pass
            # return Matrix([sum((j*k for j, k in zip(m, n))) for m, n in zip(m_1, m_2_t)])
            return Matrix([[self.multiply(i, self.transpose(j))[0] for j in m_2_t] for i in m_1])

    @staticmethod
    def _scalar_multiplication(m_1, m_2):
        if type(m_2) == Matrix:
            return [[m_1 * j for j in i] for i in m_2]
        elif type(m_2) == list:
            return [m_1 * j for j in m_2]

    @staticmethod
    def _check_multiply_matching(m_1, m_2, t_1, t_2):
        if t_1 == list and t_2 == Matrix:
            if len(m_1) != len(m_2):
                raise MultiplicationError
        elif t_1 == Matrix and t_2 == Matrix:
            if m_1.dim() != m_2.dim()[::-1]:
                raise MultiplicationError
        elif t_1 not in [Matrix, list, int, float] and t_2 not in [Matrix, list]:
            raise TypeError

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
