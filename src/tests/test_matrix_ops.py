from unittest import TestCase, main
from src.fem.matrix_ops import Matrix, AdditionError, MultiplicationError
from src.fem.matrix_ops import MatrixOperations as MOps


class TestAddingOperations(TestCase):
    def setUp(self):
        self.m_1 = Matrix([[1, 2],
                           [3, 4]])
        self.m_2 = Matrix([[1, 2],
                           [3, 4]])
        self.m_3 = Matrix([[1, 2, 3],
                           [2, 3, 4]])

    def test_adding_matrices(self):
        m_r = Matrix([[2, 4],
                      [6, 8]])
        m_check = MOps().add(self.m_1, self.m_2)
        self.assertIsInstance(m_check, Matrix)
        self.assertEqual(m_check, m_r)

    def test_substracting_matrices(self):
        m_r = Matrix([[0, 0],
                      [0, 0]])
        m_check = MOps().subtract(self.m_1, self.m_2)
        self.assertIsInstance(m_check, Matrix)
        self.assertEqual(m_check, m_r)

    def test_catching_errors(self):
        with self.assertRaises(TypeError):
            MOps().add(1, 2)
        with self.assertRaises(TypeError):
            MOps().add(self.m_1, [1, 2])
        with self.assertRaises(AdditionError):
            MOps().add(self.m_1, self.m_3)

    def test_adding_vectors(self):
        v_1 = [1, 2]
        v_2 = [1, 2]
        v_r = [2, 4]
        self.assertEqual(MOps().add(v_1, v_2), v_r)
        with self.assertRaises(TypeError):
            MOps().add(v_1, 'ad')


class TestTransposeOperation(TestCase):
    def setUp(self):
        self.m_1 = Matrix([[0, 1],
                           [1, 2],
                           [3, 4]])
        self.v_1 = [0, 2, 3]

    def test_vector_transposition(self):
        expected = Matrix([[0], [2], [3]])
        self.assertEqual(MOps().transpose(self.v_1), expected)
        self.assertEqual(MOps().transpose(expected), self.v_1)

    def test_matrix_transposition(self):
        expected = Matrix([[0, 1, 3],
                           [1, 2, 4]])
        self.assertEqual(MOps().transpose(self.m_1), expected)
        self.assertEqual(MOps().transpose(expected), self.m_1)


class TestMultiplicationOperation(TestCase):
    def setUp(self):
        self.m_1 = Matrix([[0, 1],
                           [2, 3]])
        self.m_2 = Matrix([[0, 1],
                           [2, 4]])
        self.m_3 = Matrix([[0, 1, 2],
                           [1, 2, 3]])
        self.m_4 = Matrix([[0, 1],
                           [2, 3],
                           [3, 5]])
        self.v_1 = [0, 2]
        self.v_2 = Matrix([[1], [3]])  # transposed vector

    def test_scalar_multiplication(self):
        self.assertEqual(MOps().multiply(2, self.v_1), [0, 4])
        expected = [[0, 2],
                    [4, 6]]
        self.assertEqual(MOps().multiply(2, self.m_1), expected)

    def test_vector_multiplication(self):
        self.assertEqual(MOps().multiply(self.v_1, self.v_2), 6)
        self.assertEqual(MOps().multiply(self.v_1, self.m_3), [2, 4, 6])
        with self.assertRaises(MultiplicationError):
            MOps().multiply(self.v_1, self.m_4)

    def test_matrix_multiplication(self):
        expected = Matrix([[2, 4],
                           [6, 14]])
        self.assertEqual(MOps().multiply(self.m_1, self.m_2), expected)
        expected = Matrix([[8, 13],
                           [13, 22]])
        self.assertEqual(MOps().multiply(self.m_3, self.m_4), expected)
        with self.assertRaises(MultiplicationError):
            MOps().multiply(self.m_2, self.m_4)


class TestCholeskyDecomposition(TestCase):
    def test_cholesky(self):
        matrix = Matrix([[1, 1, 1, 1],
                        [1, 5, 5, 5],
                        [1, 5, 14, 14],
                        [1, 5, 14, 14]])
        expected = Matrix([[1, 1, 1, 1],
                           [0, 2, 2, 2],
                           [0, 0, 3, 3],
                           [0, 0, 0, 1]])
        self.assertEqual(expected, MOps().cholesky(matrix))
