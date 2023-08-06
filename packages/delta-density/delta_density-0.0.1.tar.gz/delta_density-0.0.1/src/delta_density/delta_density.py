
def max_edges(n: int) -> float:
    return n * (n - 1) / 2


def delta_density(n: int, m: int, delta: float) -> float:
    return (aritmet(m, delta) / (aritmet(m, delta) + max_edges(n) - m))


def aritmet(m: int, delta: float) -> float:
    return m * (2 + delta * (1 + m)) / 2


def delta_param(n: int, k: float, d: float) -> float:
    return 4 * (d * n - d - k) / ((1 - d) * k * (k * n + 2))
