from unittest import TestCase
from src.fem.matrix_ops import Matrix
from src.fem.matrix_ops import MatrixOperations as MOps


class TestCholeskyLDL(TestCase):
    def test_cholesky_ldl(self):
        matrix = Matrix([[1, 1,  1,  1],
                         [1, 5,  5,  5],
                         [1, 5, 14, 14],
                         [1, 5, 14, 14]])
        l_down, diag = MOps().cholesky_ldl(matrix)
        l_up = MOps().transpose(l_down)
        ld = MOps().multiply(l_down, diag)
        ldl = MOps().multiply(ld, l_up)
        self.assertEqual(ldl, matrix)

    def test_cholesky_ldl_2(self):
        l_down = Matrix([[1, 0, 0],
                         [3, 1, 0],
                         [2, 3, 1]])
        diag = Matrix([[1, 0, 0],
                       [0, 4, 0],
                       [0, 0, 9]])
        l_up = MOps().transpose(l_down)
        output_ld = MOps().multiply(l_down, diag)
        output = MOps().multiply(output_ld, l_up)
        self.assertEqual(MOps().cholesky_ldl(output), (l_down, diag))

    def test_cholesky_ldl_3(self):
        matrix = Matrix([[4,    12, -16],
                         [12,   37, -43],
                         [-16, -43,  98]])
        expected = (
            Matrix([[1,  0, 0],
                    [3,  1, 0],
                    [-4, 5, 1]]),
            Matrix([[4, 0, 0],
                    [0, 1, 0],
                    [0, 0, 9]])
        )
        self.assertEqual(MOps().cholesky_ldl(matrix), expected)


class TestDeterminant(TestCase):
    pass


class TestSolvingTriangleEquations(TestCase):
    pass


class TestSolvingSquareEquations(TestCase):
    def test_equation_solving(self):
        matrix = Matrix([[1, 3, 5],
                         [3, 13, 27],
                         [5, 27, 77]])
        result = Matrix([[4], [24], [80]])
        solution = MOps().solve_ldl_equation(matrix, result)
        self.assertEqual(MOps().multiply(matrix, solution), result)


class TestCreateEmptyMatrix(TestCase):
    def test_empty_matrix(self):
        expected = Matrix([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        self.assertEqual(MOps().create_empty_matrix(3, 3), expected)

    def test_empty_matrix_2(self):
        expected = Matrix([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        self.assertEqual(MOps().create_empty_matrix(4, 3), expected)
