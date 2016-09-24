from src.fem.matrix_ops import Matrix

LOCAL_MATRIX_MULTIPLIERS = Matrix([
    [ 1,   0,  0, -1,   0,  0],
    [ 0,  12,  6,  0, -12,  6],
    [ 0,   6,  4,  0,  -6,  2],
    [-1,   0,  0,  1,   0,  0],
    [ 0, -12, -6,  0,  12, -6],
    [ 0,   6,  2,  0,  -6,  4],
])

LOCAL_MATRIX_LENGTH_POWERS = Matrix([
    [1, 0, 0, 1, 0, 0],
    [0, 3, 2, 0, 3, 2],
    [0, 2, 1, 0, 2, 1],
    [1, 0, 0, 1, 0, 0],
    [0, 3, 2, 0, 3, 2],
    [0, 2, 1, 0, 2, 1],
])


def create_directional_matrix(c, s):
    return Matrix([
        [c, s, 0, 0, 0, 0],
        [-s,c, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, c, s, 0],
        [0, 0, 0,-s, c, 0],
        [0, 0, 0, 0, 0, 1]
    ])
