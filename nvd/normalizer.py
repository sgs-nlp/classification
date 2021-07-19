def vec_scale_vec(vec: list):
    import numpy
    _vec = []
    for i in vec:
        _vec.append(_scale2zero_one(i))
    return numpy.array(_vec)


def matrix_scale_matrix(matrix):
    import numpy
    _matrix = numpy.array([vec_scale_vec(matrix[0])])

    for vec in matrix[1:]:
        _matrix = numpy.append(_matrix, [vec_scale_vec(vec)], axis=0)
    return _matrix


def _sin_scale(x: float) -> float:
    from math import sin
    return (sin(x) + 1) / 2


def _scale2zero_one(x):
    res = 0
    if x < -1:
        res = -2 + 1 / abs(x)
    if -1 <= x <= 1:
        res = x
    if 1 < x:
        res = 2 - 1 / x
    return (res + 2) / 4
