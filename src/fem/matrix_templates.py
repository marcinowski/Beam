from src.fem.matrix_ops import Matrix

SINGLE_LOCAL_MATRIX_MULTIPLIERS = Matrix([
    [ 1,   0,  0, -1,   0,  0],
    [ 0,  12,  6,  0, -12,  6],
    [ 0,   6,  4,  0,  -6,  2],
    [-1,   0,  0,  1,   0,  0],
    [ 0, -12, -6,  0,  12, -6],
    [ 0,   6,  2,  0,  -6,  4],
])

SINGLE_LOCAL_MATRIX_POWERS_IN_DENOMINATOR = Matrix([
    [1, 0, 0, 1, 0, 0],
    [0, 3, 2, 0, 3, 2],
    [0, 2, 1, 0, 2, 1],
    [1, 0, 0, 1, 0, 0],
    [0, 3, 2, 0, 3, 2],
    [0, 2, 1, 0, 2, 1],
])
