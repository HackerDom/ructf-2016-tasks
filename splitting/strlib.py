__all__ = ['find_intersect']


def _z(s):
    z = [0]*len(s)

    (l, r) = (0, 0)
    for i in range(1, len(s)):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])

        while i + z[i] < len(s) and s[z[i]] == s[i + z[i]]:
            z[i] += 1

        if i + z[i] - 1 > r:
            (l, r) = (i, i + z[i] - 1)

    return z


def find_intersect(first, second):
    s = second + first
    z = _z(s)

    for i in range(-min(len(first), len(second)), 0):
        if z[i] == -i:
            yield -i
